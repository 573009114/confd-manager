# -*- coding: utf-8 -*-
from models import projectList
from django.http import JsonResponse,HttpResponse

import json

def viewProConf():
    data=projectList.objects.filter(envtype='product').values('id','projectName','confText','vhosts','serverName','envtype','typed')
    return data

def viewDevConf():
    data=projectList.objects.filter(envtype='develop').values('id','projectName','confText','vhosts','serverName','envtype','typed')
    response=HttpResponse(json.dumps(list(data), default=lambda obj: obj.__dict__), content_type='application/json')
    return data

def viewTestConf():
    data=projectList.objects.filter(envtype='test').values('id','projectName','confText','vhosts','serverName','envtype','typed')
    response=HttpResponse(json.dumps(list(data), default=lambda obj: obj.__dict__), content_type='application/json')
    return data

# 增、删、改
def defaultProJectConf(pid):
    default=[]
    response=projectList.objects.filter(id=pid).values('confText','vhosts')
    for k in response:
        default.append(k)
    return default

def addProJectConf(typed,env_type,projectName,serverName,vhost,keyname):
    response=projectList.objects.create(typed=typed,envtype=env_type,projectName=projectName,serverName=serverName,vhosts=vhost,keyname=keyname)
    response.save()
    return bool(True)

def delProJectConf(pid):
    projectList.objects.filter(id=pid).delete()
    return bool(True)

def channgeProJectConf(pid,confContent):
    projectList.objects.filter(id=pid).update(confText=confContent)
    response='配置修改完成'
    return response

def findProjectConf(pid):
    response=list(projectList.objects.filter(id=pid).values('confText','keyname')).pop()
    keyName=response['keyname']
    confText=response['confText']
    result={'keyName':keyName,'confText':confText}
    return result
