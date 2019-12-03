from django.db import models


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    Username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    Password = models.CharField(verbose_name='密码', max_length=16)
    Alias = models.CharField(verbose_name='昵称', max_length=32, null=True, blank=True)
    role = models.ManyToManyField(verbose_name='用户角色', to='Role', related_name='UserProfile')
    IsAdmin = models.BooleanField(verbose_name='超级管理员', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(verbose_name='角色标签', max_length=64, unique=True)
    permissions = models.ManyToManyField(verbose_name='角色权限', to='Permission', related_name='Role')


class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(verbose_name='权限标签', max_length=64)
    url_path = models.CharField(verbose_name='路由路径', max_length=256)
    url_name = models.CharField(verbose_name='路由命名', max_length=128)
    menu_root = models.ForeignKey(verbose_name='所属一级菜单', to='MenuRoot', related_name='Permission', null=True, blank=True, on_delete=models.SET_NULL)
    menu_parent = models.ForeignKey(verbose_name='所属二级菜单', to='self', related_name='Children', null=True, blank=True, on_delete=models.SET_NULL)


class MenuRoot(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(verbose_name='根菜单标签', max_length=64)
    icon = models.CharField(verbose_name='根菜单图标', max_length=64, null=True, blank=True)
    weight = models.IntegerField(verbose_name='根菜单排序权重', default=142857)

