# -*- coding: utf-8 -*-
from models import KeyList,Servers,HostAlias

from django.core import serializers
import json


class viewsConf:
    def __init__(self,typed):
        self.typed=typed

    def envConf(self):
        data=KeyList.objects.filter(envtype='%s' %self.typed).values('id','projectName','confText','vhosts','serverName','envtype','typed')
        return data 
    def envAll(self):
        data=KeyList.objects.all().values('id','projectName','confText','vhosts','serverName','envtype','typed')
        return data


class projectConf:
    def __init__(self,**kwargs):
        self.id=kwargs.get('pid')
        self.typed=kwargs.get('typed')
        self.env_type=kwargs.get('env_type')
        self.projectName=kwargs.get('projectName')
        self.serverName=kwargs.get('serverName')
        self.vhost=kwargs.get('vhost')
        self.keyname=kwargs.get('keyname')
        self.confContent=kwargs.get('confContent')
        self.serverip=kwargs.get('serverip')

    def defaultProJectConf(self):
        default=[]
        response=KeyList.objects.filter(id=self.id).values('confText','vhosts')
        for k in response:
            default.append(k)
        return default

    def channgeProJectConf(self):
        KeyList.objects.filter(id=self.id).update(confText= self.confContent)
        response='配置修改完成'
        return response

    def addProJectConf(self):
        response=KeyList.objects.create(typed=self.typed,envtype=self.env_type,projectName=self.projectName,serverName=self.serverName,vhosts=self.vhost,keyname=self.keyname)
        response.save()
        return response.id

    def delProJectConf(self):
        KeyList.objects.filter(id=self.id).delete()
        return bool(True)

    def findProjectConf(self):
        response=list(KeyList.objects.filter(id=self.id).values('confText','keyname')).pop()
        keyName=response['keyname']
        confText=response['confText']
        result={'keyName':keyName,'confText':confText}
        return result

    # Servers 表操作
    def addServer(self):
        response=Servers.objects.create(servearip=self.serverip)
        response.save()
        return response.id

    def delServer(self):
        Servers.objects.filter(id=self.id).delete()
        return bool(True)


def viewsServer():
    response=Servers.objects.all().values('id','servearip')
    return response

# HostAlias 表操作
def addHostid(sid,kid):
    try:
        for s in sid:
           response=HostAlias.objects.create(sid_id=s,kid_id=kid)
           response.save()
    except:
        response='执行失败'
    return response


if __name__ == '__main__':
    editProject(1111,2222,'1234213fewef').defaultProJectConf()