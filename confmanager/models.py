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
    keyname=models.CharField(max_length=128,unique=True)

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

class VersionId(models.Model):
    version=models.CharField(max_length=128)
    confText=models.TextField()
    kid= models.ForeignKey(KeyList)
    class Meta():
        db_table = 'omds_version'
    