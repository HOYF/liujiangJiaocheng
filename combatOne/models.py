# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class User(models.Model):
    gender = (
        ('male','男'),
        ('female','女'),
    )
    # 用户名必填，长度不超过128个字符，并且唯一【即不能有相同的用户名】
    name = models.CharField(max_length=128, unique=True)
    # 必填，长度不超过256个字符
    password = models.CharField(max_length=256)
    # email，使用django内置的邮箱类型，并且唯一
    email = models.EmailField(unique=True)
    # 性别使用一个choices，只能选择男或女，默认为男
    sex = models.CharField(max_length=32,choices=gender,default='男')
    # 元数据里定义用户按创建时间的反序列排列，也就是最近的最先显示
    c_time = models.DateTimeField(auto_now_add=True)
    # 是否进行邮件注册，默认未进行邮件注册
    has_confirmed = models.BooleanField(default=False)

    # 使用 __str__帮助人性化显示对象信息
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


# ConfirmString模型保存了用户和注册吗之间的关系，一对一的形式
class ConfirmString(models.Model):
    # code字段是哈希后的注册码
    code = models.CharField(max_length=256)
    # user是关联的一对一用户
    user = models.OneToOneField('User')
    # 是注册的提交时间
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ": " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"