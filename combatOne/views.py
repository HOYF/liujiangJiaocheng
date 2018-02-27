# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from .forms import UserForm
from .forms import RegisterForm
import hashlib
import datetime
from django.conf import settings

# Create your views here.

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode()) # update方法只接受bytes类型
    return h.hexdigest()

# 该方法接收两个参数，分别是注册的邮箱和前面生成的哈希值
def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自www.liujiangblog.com的注册确认邮件'
    text_content = '''感谢注册www.liujiangblog.com，这里是饕餮鱼的博客和教程站点，专注于Python和Django技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是饕餮鱼的博客和教程站点，专注于Python和Django技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[email])
    msg.attach_alternative(html_content,"text/html")
    msg.send()

# 创建确认码对象 方法
def make_confirm_string(user):
    # 该方法接收一个用对象作为参数
    # 首先利用datetime模块生产一个当前时间的字符串now
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 再调用我们前面编写的hash_code()方法以用户名为基础，now为'盐',生成一个独一无二的哈希值
    code = hash_code(user.name, now)
    # 在调用ConfirmString模型的create()方法，生产并保存一个确认码对象
    models.ConfirmString.objects.create(code=code, user=user,)
    # 最后返回这个哈希值
    return code


def index(request):
    pass
    return render(request, 'login/index.html')

def login(request):
    # 通过下面if语句，我们不允许重复登录
    if request.session.get('is_login',None):
        return redirect("/index/")

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容!"
        # 使用表单类自带的 is_valid() 方法一步完成数据验证工作
        if login_form.is_valid():
            # 验证成功后可以从表单对象的 cleaned_data 数据字典中获取表单的具体值
            # 如果验证不通过，则返回一个包含先前数据的表单给前端页面，方便用户修改。也就是说，它会帮你保留先前填写的数据内容，而不是返回一个空表！
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if not user.has_confirmed:
                    message = "该用户还未通过邮件确认！"
                    return render(request, 'login/login.html', locals())
                if user.password == hash_code(password): #哈希值和数据库内的值进行比对
                    # 通过下面语句，我们往session字典内写入用户状态和数据
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确!"
            except:
                message = "用户不存在!"
        # locals() 函数返回当前所有的本地变量字典，我们可以偷懒的将这作为render函数的数据字典参数值
        # 就不用费劲去构造一个形如{'message':message, 'login_form':login_form}的字典了
        return render(request,'login/login.html',locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login',None):
        # 登录状态不允许注册
        return redirect('/index/')
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():#获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2: #判断两次密码是否相同
                message = "两次输入的密码不同!"
                return render(request,'login/register.html',locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user: #用户名唯一
                    message = '用户名已经存在，请从新选择用户名'
                    return render(request,'login/register.html',locals())
                same_name_user = models.User.objects.filter(email=email)
                if same_name_user:#邮箱地址唯一
                    message = "该邮箱地址已被注册，请使用别的邮箱!"
                    return render(request,'login/register.html',locals())
                # 当下一切都ok的情况下，创建新用户
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password  = hash_code(password1) # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)
                message = '请前往注册邮箱，进行邮件确认！'
                # 跳转到等待邮件确认页面
                return render(request, 'login/confirm.html',locals())
                # return redirect('/login/') #自动跳转到登录页面
    register_form = RegisterForm()
    return render(request,'login/register.html',locals())



def logout(request):
    if not request.session.get('is_login',None):
        #如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    # flush()方法是比较安全的一种做法，而且一次性将sesstion中的所有内容全部清空，确保不留后患。
    # 但也有不好的地方，那就是如果你在session中夹带了一点"私货"，会被一并删除
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/index/')
    # pass
    # 当登出时，页面重定向到 index 首页
    # return redirect('/index/')


# 添加一个User_confirm试图
def user_confirm(request):
    # 通过该代码，从请求的url地址中获取确认码
    code = request.GET.get('code',None)
    message = ''
    try:
        # 然后去数据库内查询是否有对应的确认码
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        # 如果没有，返回confirm.html页面，并提示
        message = '无效的确认请求!'
        return render(request,'login/confirm.html',locals())
    # 如果有，获取注册的时间
    c_time = confirm.c_time
    now = datetime.datetime.now()
    # 然后用注册的时间 + 设置过期的天数
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        # 如果时间已经超期，删除注册的用户，同时注册码也会一并删除，然后返回confirm.html页面，并提示
        confirm.user.delete()
        message = '您的邮件已经过期，请重新注册！'
        return render(request, 'login/confirm.html',locals())
    else:
        # 如果未超期，修改用户的has_confirmed字段未True，并保存，表示通过确认了。然后删除注册码，但不删除用户本身
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账号登录！'
        # 最后返回confirm.html页面
        return render(request, 'login/confirm.html', locals())


''' 1
# request该参数封装了当前请求的所有数据
if request.method == "POST":
    # get('username',None) 确保当数据请求中没有username键时不会抛出异常，而是返回一个我们指定都默认值None;
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)
    # 确保用户名和密码都不为空
    if username and password:
        # 通过 strip() 方法，将用户名前后无效都空格剪除
        username = username.strip()
        # 用户名字字符合法性验证
        # 密码长度验证
        # 更多都其他验证。。。
        # print(username,password)
        # 网页重定向到index
        # 使用try异常机制，防止数据库查询失败都异常
        try:
            # models.User.objects.get(name=username) 是Django提供到最常用到数据查询API
            user = models.User.objects.get(name=username)
            if user.password == password:
                return redirect('/index/')
            else:
                message = "密码不正确！"
        except:
            # 如果未匹配到用户，则执行except中到语句
            message = "用户名不存在！"
    return render(request,'login/login.html',{"message":message})
        # 密码比对，成功则跳转到index页面，失败则什么都不做
        # if user.password == password:
        #     return redirect('/index/')
return render(request, 'login/login.html')
'''
