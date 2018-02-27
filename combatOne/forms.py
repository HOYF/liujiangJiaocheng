# -*- coding: utf-8 -*-
# Django的form表单，一个字段代表<form>中的一个<input>元素
from django import forms #导入forms模块
from captcha.fields import CaptchaField

# 所有导表单类都要继承forms.Form类
class UserForm(forms.Form):
    # 每个字段都有自己导字段类型比如CharField，他们分别对应一种HTML语言中<form>内导一个input元素，这跟Django模型系统导设计非常相似
    # label 参数用于设置 <label> 标签
    # max_length 限制字段输入导最大长度，它起到两个作用：1.在浏览器页面限制用户输入不可超过字符数，2.在后端服务器验证用户输入的长度也不可超过
    username = forms.CharField(label="用户名",max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    # widget=forms.PasswordInput 用于指定该字段在form表单里表现为 <input type="password" />， 也就是密码输入框
    password = forms.CharField(label="密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label='验证码')

class RegisterForm(forms.Form):
    gender = (
        ('male',"男"),
        ('female',"女"),
    )
    username = forms.CharField(label="用户名",max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="确认密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label="邮箱地址",widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label="性别",choices=gender)
    captcha = CaptchaField(label='验证码')
