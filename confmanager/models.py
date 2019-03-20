# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# 创建多对多关系表
class KeyList(models.Model):
    typed = models.CharField(max_length=32)
    envtype = models.CharField(max_length=32)
    projectName=models.CharField(max_length=128)
    serverName=models.CharField(max_length=32)
    vhosts=models.CharField(max_length=128)
    keyname=models.CharField(max_length=128)
    confText=models.TextField()

    class Meta:
        db_table = 'omds_keylist'

class Servers(models.Model):
    servearip = models.CharField(max_length=32)
    keylist = models.ManyToManyField(KeyList,through='HostAlias')

    class Meta:
        db_table = 'omds_servers'

class HostAlias(models.Model):
    kid= models.ForeignKey(KeyList)
    sid= models.ForeignKey(Servers)
    
    class Meta():
         db_table = 'omds_hostalias'



# 用户表
class users(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=128)
    last_login=models.DateTimeField()
    email=models.EmailField(max_length=128)
    is_active=models.BooleanField()
    pic=models.ImageField()
 
    roles= models.ManyToManyField(verbose_name='具有的所有角色',to="Role",blank=True)
    class Meta():
        db_table = 'omds_users'

# 角色表
class Role(models.Model):
    name=models.CharField(max_length=32)
    permissions = models.ManyToManyField(verbose_name='具有的所有权限',to='Permission',blank=True)

    class Meta():
        db_table = 'omds_role'

# 权限表
class Permission(models.Model):
    permissions_id=models.CharField(max_length=50)
    group =models.ForeignKey(verbose_name='所属组',to='Group',null=True,blank=True) 
    class Meta():
        db_table = 'omds_permissions'

# 用户组
class Group(models.Model):
    name = models.CharField(max_length=24, verbose_name='用户组名', unique=True)
    class Meta:
        db_table = 'omds_group'