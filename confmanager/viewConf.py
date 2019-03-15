# -*- coding: utf-8 -*-
from models import KeyList,Servers,HostAlias
from django.http import JsonResponse,HttpResponse
import json

def viewProConf():
    data=KeyList.objects.filter(envtype='product').values('id','projectName','confText','vhosts','serverName','envtype','typed')
    return data

def viewDevConf():
    data=KeyList.objects.filter(envtype='develop').values('id','projectName','confText','vhosts','serverName','envtype','typed')
    response=HttpResponse(json.dumps(list(data), default=lambda obj: obj.__dict__), content_type='application/json')
    return data

def viewTestConf():
    data=KeyList.objects.filter(envtype='test').values('id','projectName','confText','vhosts','serverName','envtype','typed')
    response=HttpResponse(json.dumps(list(data), default=lambda obj: obj.__dict__), content_type='application/json')
    return data

# 增、删、改
def defaultProJectConf(pid):
    default=[]
    response=KeyList.objects.filter(id=pid).values('confText','vhosts')
    for k in response:
        default.append(k)
    return default

def addProJectConf(typed,env_type,projectName,serverName,vhost,keyname):
    response=KeyList.objects.create(typed=typed,envtype=env_type,projectName=projectName,serverName=serverName,vhosts=vhost,keyname=keyname)
    response.save()
    return response.id

def delProJectConf(pid):
    KeyList.objects.filter(id=pid).delete()
    return bool(True)

def channgeProJectConf(pid,confContent):
    KeyList.objects.filter(id=pid).update(confText=confContent)
    response='配置修改完成'
    return response

def findProjectConf(pid):
    response=list(KeyList.objects.filter(id=pid).values('confText','keyname')).pop()
    keyName=response['keyname']
    confText=response['confText']
    result={'keyName':keyName,'confText':confText}
    return result


# Servers 表操作
def addServer(serverip):
    response=Servers.objects.create(servearip=serverip)
    response.save()
    return response.id

def viewsServer():
    response=Servers.objects.all().values('id','servearip')
    return response

def delServer(pid):
    Servers.objects.filter(id=pid).delete()
    return bool(True)


# HostAlias 表操作
def addHostid(sid,kid):
    try:
        for s in sid:
           response=HostAlias.objects.create(sid_id=s,kid_id=kid)
           response.save()
    except:
        response='执行失败'
    return response
