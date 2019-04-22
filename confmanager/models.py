# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# omds 关系表

class Groups(models.Model):
    groupname=models.CharField(max_length=128,unique=True)
    serverconfig=models.TextField()
    keyngx=models.CharField(max_length=32,unique=True)

    class Meta():
        db_table= 'omds_groups'
        
class KeyList(models.Model):
    typed = models.CharField(max_length=32)
    envtype = models.CharField(max_length=32)
    projectName=models.CharField(max_length=128)
    serverName=models.CharField(max_length=32)
    vhosts=models.CharField(max_length=128)
    keyhost=models.CharField(max_length=128)
    keyrewrite=models.CharField(max_length=128)
    group = models.ForeignKey(Groups)

    class Meta:
        db_table = 'omds_keylist'


class Servers(models.Model):
    group = models.ForeignKey(Groups)
    servearip = models.CharField(max_length=32,unique=True)
    keylist = models.ManyToManyField(KeyList,through='HostAlias')
    

    class Meta:
        db_table = 'omds_servers'

class HostAlias(models.Model):
    kid= models.ForeignKey(KeyList)
    sid= models.ForeignKey(Servers)
    
    class Meta():
        db_table = 'omds_hostalias'

class VersionId(models.Model):
    version=models.CharField(max_length=32)
    confText=models.TextField()
    rewrite=models.TextField()
    kid= models.ForeignKey(KeyList)

    class Meta():
        db_table = 'omds_version'