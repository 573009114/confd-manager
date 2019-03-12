# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class projectList(models.Model):
    typed = models.CharField(max_length=50)
    envtype = models.CharField(max_length=50)
    projectName=models.CharField(max_length=200)
    serverName=models.CharField(max_length=100)
    vhosts=models.CharField(max_length=100)
    keyname=models.CharField(max_length=100)
    confText=models.TextField()
    class Meta:
        db_table = "omds_projectList"
