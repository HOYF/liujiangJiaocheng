# -*- coding: utf-8 -*-

import os
from django.core.mail import send_mail #发送普通消息模版
from django.core.mail import EmailMultiAlternatives #发送HTML邮件
from django.conf import settings



# 由于我们是单独运行send_mail.py文件，所以无法使用Django环境，需要通过os模块对环境变量进行设置
os.environ['DJANGO_SETTINGS_MODULE'] = 'liujiangJiaocheng.settings'

''' 发送普通内容邮件
if __name__ == '__main__':
    # 发件人 已经写在配置中 直接从配置中获取
    from_who = settings.EMALL_FROM
    # 收件人 是一个列表
    to_who = '449120275@qq.com'
    # 发送的主题
    subject = '来自heyifunobug@163.com的测试邮件'
    # 发送的消息，发送普通的消息时用message
    # 佛昂一个html消息，需要指定
    message = '欢迎访问www.heyifunobgu.com,这里是发送内容'
    send_mail(
        subject,message,from_who,[to_who]
    )
'''

# 发送HTML邮件
if __name__ == '__main__':
    subject,from_email,to = '来自heyifunobug@163.com的测试邮件',settings.EMALL_FROM,'449120275@qq.com'
    text_content = '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！'
    html_content = '<p>欢迎访问<a href="http://www.liujiangblog.com" target=blank>www.liujiangblog.com</a>，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>'
    msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
    msg.attach_alternative(html_content,"text/html")
    msg.send()

    # send_mail() 第一个参数是邮件主题subject；第二个参数是邮件具体内容；第三个参数是邮件发送方，需要和你settings中的一致，第四个参数是接收方的邮件地址列表