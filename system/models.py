from django.db import models
from django.contrib.auth.models import AbstractUser, Group, User


class Users(AbstractUser):
    """
    基于django表  添加字段 , 如有需要调用user的情况,请使用此表
    """
    position = models.CharField(max_length=64, verbose_name='职位信息', blank=True, null=True)
    avatar = models.CharField(max_length=256, verbose_name='头像', blank=True, null=True)
    mobile = models.CharField(max_length=11, verbose_name='手机', blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Test(models.Model):
    date = models.CharField(max_length=96, verbose_name='日期', blank=True, null=True, )
    name = models.CharField(max_length=96, verbose_name='姓名', blank=True, null=True, )
    address = models.CharField(max_length=96, verbose_name='地址', blank=True, null=True, )

    # c_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', blank=True)
    # u_time = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间', blank=True)

    class Meta:
        db_table = "test"
        verbose_name = "测试"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
