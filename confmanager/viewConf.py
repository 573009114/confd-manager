# -*- coding: utf-8 -*-
from models import KeyList,Servers,HostAlias,VersionId,Groups

from django.core import serializers
import json
 

class viewsConf:
    def __init__(self,typed):
        self.typed=typed
      
 
    def envConf(self):
        data=KeyList.objects.filter(envtype='%s' %self.typed).values('id','projectName','vhosts','serverName','envtype','typed','group__groupname') 
        return data 

    def envAll(self):
        data=KeyList.objects.all().values('id','projectName','vhosts','serverName','envtype','typed','group__groupname')
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
        self.keyrewrite=kwargs.get('keyrewrite')
        self.keyngx=kwargs.get('keyngx')
        self.confContent=kwargs.get('confContent')
        self.serverip=kwargs.get('serverip')
        self.version=kwargs.get('version')
        self.rewrite=kwargs.get('rewrite')
        self.groupid=kwargs.get('groupid')
        self.groupname=kwargs.get('groupname')
        self.serverconfig=kwargs.get('config')

    # 默认初始配置
    def defaultProJectConf(self):
        default_host=[]
        default_content=[]

        domain=KeyList.objects.filter(id=self.id).values('vhosts').first()
        version=VersionId.objects.filter(kid_id=self.id).values('version').order_by('-version')[:5]
        try:
           config=VersionId.objects.filter(kid_id=self.id).values('confText','rewrite').latest('version')
        except:
           config=''
        return config,domain,version


    # 添加项目
    def addProJectConf(self):
        ChkKey=KeyList.objects.filter(keyhost=self.keyname).values('id')
        if ChkKey:
            return bool(False)
        else:
            response=KeyList.objects.create(typed=self.typed,envtype=self.env_type,
                                            projectName=self.projectName,serverName=self.serverName,
                                            vhosts=self.vhost,keyhost=self.keyname,keyrewrite=self.keyrewrite,group_id=self.groupid)
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
        response=list(KeyList.objects.filter(id=self.id).values('keyhost','keyrewrite'))
        keyName=response[0]['keyhost']  
        rewrite=response[0]['keyrewrite']
        result={'keyName':keyName,'keyrewrite':rewrite}
        return result
    

    # Servers 表数据录入
    def addServer(self):
        response=Servers.objects.create(servearip=self.serverip,group_id=self.groupid)
        response.save()
        return response.id

    # 删除IP
    def delServer(self):
        Servers.objects.filter(id=self.id).delete()
        return bool(True)
    # 查找server表id
    def findServer(self):
        serverid=Servers.objects.filter(group_id=self.groupid).values('id')
        return serverid 



    # 查找group id
    def findGroupid(self):
        response=list(Groups.objects.filter(id=self.id).values('keyngx','serverconfig')).pop()
        return response

    # 添加分组
    def addGroup(self):
        response=Groups.objects.create(groupname=self.groupname,keyngx=self.keyngx)
        response.save()
        return response.id
    # 分组删除
    def delGroup(self):
        Groups.objects.filter(id=self.id).delete()
        return bool(True)


    # 默认主配置文件
    def defaultSetGroup(self):
        response=Groups.objects.filter(id=self.id).values('serverconfig','groupname')
        return response

    # 更新分组主配置文件
    def editGroup(self):
        response=Groups.objects.filter(id=self.id).update(serverconfig=self.serverconfig)
        return response

    # 版本创建
    def CreateVersion(self):
        response=VersionId.objects.create(version=self.version,kid_id=self.id,confText= self.confContent,rewrite=self.rewrite)
        return response

    # 历史配置查询
    def HistoryConf(self):
        response=VersionId.objects.filter(kid_id=self.id).values('confText','rewrite')
        return response

    # 回滚版本.此处修改。
    def rollback(self):
        try:
            viewconfig=VersionId.objects.filter(version=self.version).values('kid_id','confText','rewrite')
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
# 备注 : group__groupname 外键查询 group是server表里的外键字段，groupname是Group表里的字段，中间是双下划线
def viewsServer():
    serverinfo=Servers.objects.all().values('id','servearip','group__groupname')
    return serverinfo

def viewGroup():
    response=Groups.objects.all().values('id','groupname')
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

# 根据关联kid查sid
def selectSid(pid):
    serverip=HostAlias.objects.filter(kid_id=pid).values('sid__servearip')
    return serverip
 
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
