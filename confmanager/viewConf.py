# -*- coding: utf-8 -*-
from models import KeyList,Servers,HostAlias,VersionId

from django.core import serializers
import json


class viewsConf:
    def __init__(self,typed):
        self.typed=typed
      
 
    def envConf(self):
        data=KeyList.objects.filter(envtype='%s' %self.typed).values('id','projectName','vhosts','serverName','envtype','typed')
        return data 

    def envAll(self):
        data=KeyList.objects.all().values('id','projectName','vhosts','serverName','envtype','typed')
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
        self.version=kwargs.get('version')

    # 默认初始配置
    def defaultProJectConf(self):
        default_host=[]
        default_content=[]

        domain=KeyList.objects.filter(id=self.id).values('vhosts').first()
        version=VersionId.objects.filter(kid_id=self.id).values('version').order_by('-version')[:5]
        try:
           config=VersionId.objects.filter(kid_id=self.id).values('confText').latest('version')
        except:
           config=''
        return config,domain,version


    # 添加项目
    def addProJectConf(self):
        ChkKey=KeyList.objects.filter(keyname=self.keyname).values('id')
        if ChkKey:
            return bool(False)
        else:
            response=KeyList.objects.create(typed=self.typed,envtype=self.env_type,projectName=self.projectName,serverName=self.serverName,vhosts=self.vhost,keyname=self.keyname)
            response.save()
            return response.id

    # 更新项目
    def updateProJectConf(self):
        response=KeyList.objects.filter(id=self.id).values('id')
        return response

    # 删除项目
    def delProJectConf(self):
        KeyList.objects.filter(id=self.id).delete()
        return bool(True)

    # 查找项目keyname
    def findProjectConf(self):
        response=list(KeyList.objects.filter(id=self.id).values('keyname')).pop()
        keyName=response['keyname']  
        result={'keyName':keyName}
        return result
    

    # Servers 表操作
    def addServer(self):
        response=Servers.objects.create(servearip=self.serverip)
        response.save()
        return response.id

    # 删除IP
    def delServer(self):
        Servers.objects.filter(id=self.id).delete()
        return bool(True)

   
    
    # 版本创建
    def CreateVersion(self):
        response=VersionId.objects.create(version=self.version,kid_id=self.id,confText= self.confContent)
        return response

    # 历史配置查询
    def HistoryConf(self):
        response=VersionId.objects.filter(kid_id=self.id).values('confText')
        return response

    # 回滚版本.此处修改。
    def rollback(self):
        try:
            viewconfig=VersionId.objects.filter(version=self.version).values('kid_id','confText')
        except:
            viewconfig='回滚失败'
        return viewconfig

    # 指定版本
    def fixedVersion(self):
        VersionId.objects.filter(version=self.version).values('kid_id','confText')

class EditConf:
    def __init__(self,pid):
        self.id=pid

    def projectconfig(self):
        data=KeyList.objects.filter(id=self.id).values('id','projectName','vhosts','serverName','envtype','typed').first()
        return data




# 服务IP列表
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

# HostAlias 关联ip操作
def updateHostid(sid,kid):
    try:
        find_id=HostAlias.objects.filter(kid_id=kid).values('kid_id','sid_id')
        for k_id in find_id:
            HostAlias.objects.filter(kid_id=k_id['kid_id']).delete()
        for serializers in sid:
            response=HostAlias.objects.create(sid_id=serializers,kid_id=kid)
    except:
        for serializers in sid:
            response=HostAlias.objects.create(sid_id=serializers,kid_id=kid)
    return response