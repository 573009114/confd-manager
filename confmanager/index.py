# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from viewConf import *
from etcdConf import *
from django.contrib.auth.decorators import login_required
import json

#@login_required
def dashboard(req):
    return HttpResponse('默认首页，还没想好放点啥~')

def serverList(req):
    if req.method == 'GET':
        response=viewsServer()
        return render(req,'server-list.html',{'response':response})

def serverAdd(req):
    if req.method == 'POST':
        serverip=req.POST.get('serverip')
        response=addServer(serverip)
        return HttpResponse('<script type="text/javascript">alert("添加完成");location.href="/config/server/"</script>')
    return render(req,'server-add.html')

def serverDel(req):
    id=req.GET.get('pid')
    response=delServer(pid=id)
    return HttpResponse('<script type="text/javascript">alert("记录删除");location.href="/config/server/"</script>')


########################################################
#@login_required
def viewConfig(req):
    if req.method == 'GET':
        typed=req.GET.get('typed')
        if typed == 'product':
            response=viewProConf()
            env='线上环境'
        elif typed == 'develop':
            response=viewDevConf()
            env='研发环境'
        else:
            response=viewTestConf()
            env='测试环境'
        return render(req,'project-type.html',{'response':response,'env':env})


#@login_required
def projectEdit(req):
    id=req.GET.get('pid')
    env='项目编辑'
    if req.method == 'GET':
        defaultContent=defaultProJectConf(pid=id)
        response=list(defaultContent)
    elif req.method == 'POST':
        confContent=req.POST.get('configText')
        channgeContent=channgeProJectConf(id,confContent)
        return HttpResponse('<script type="text/javascript">alert("信息修改完成");location.href="javascript:history.back(-1);"</script>')
    return render(req,'project-content.html',{'response':response,'env':env})


#@login_required
def confPush(req):
    id=req.GET.get('pid')
    response=findProjectConf(pid=id)
    keyName=response['keyName']
    value=response['confText']
    etcdClient().writeValue(keyName,value)
    return HttpResponse('<script type="text/javascript">alert("推送完成");location.href="javascript:history.back(-1);"</script>')

#@login_required
def projectAdd(req):
     response=''
     env='新增项目'
     serverlist=viewsServer()

     if req.method == 'POST':
         typed=req.POST.get('type')
         env_type=req.POST.get('envtype')
         projectName=req.POST.get('projectname')
         serverName=req.POST.get('servername')
         vhost=req.POST.get('domain')
         cluster=req.POST.get('cluster')
         sid=req.POST.getlist('sid[]')
         keyname=('/%s/%s/%s/%s' %(env_type,serverName,cluster,vhost))
         kid=addProJectConf(typed,env_type,projectName,serverName,vhost,keyname)
         addHostid(sid,kid)
         return HttpResponse('<script type="text/javascript">alert("项目添加完成");location.href="/config/project/add"</script>')
     return render(req,'project-add.html',{'env':env,'serverlist':serverlist})


#@login_required
def projectDel(req):
    id=req.GET.get('pid')
    obtainKey=findProjectConf(pid=id)
    try:
        keyName=obtainKey['keyName']
        delEtcd=etcdClient().delKey(keyName)
        response=delProJectConf(pid=id)
    except:
        response=delProJectConf(pid=id)
    return HttpResponse('<script type="text/javascript">alert("记录删除");location.href="/config/project/"</script>')

