# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,render_to_response
from viewConf import *
from etcdConf import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json,etcd
import datetime

def global_env():
    Version=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return Version

@login_required
def serverList(req):
    if req.method == 'GET':
        response=viewsServer()
        return render(req,'server-list.html',{'response':response})

@login_required
def serverAdd(req):
    if req.method == 'POST':
        serverip=req.POST.get('serverip')
        response=projectConf(serverip=serverip).addServer()
        return HttpResponse('<script type="text/javascript">alert("添加完成");location.href="/config/server/"</script>')
    return render(req,'server-add.html')


@login_required
def serverDel(req):
    id=req.GET.get('pid')
    response=projectConf(pid=id).delServer()
    return HttpResponse('<script type="text/javascript">alert("记录删除");location.href="/config/server/"</script>')


########################################################
@login_required
def viewConfig(req):
    if req.method == 'GET':
        typed=req.GET.get('typed')
        id=req.GET.get('id')
      
        if typed == 'product':
            response=viewsConf(typed).envConf()
      
            env={'name':'线上环境'}
        elif typed == 'develop':
            response=viewsConf(typed).envConf()
       
            env={'name':'研发环境'}
        elif typed == 'test':
            response=viewsConf(typed).envConf()
      
            env={'name':'测试环境'}
        else:
            response=viewsConf(typed).envAll()
            env={'name':'所有环境'}
        return render(req,'project-type.html',{'response':response,'env':env})

# 编辑配置
@login_required
def projectEdit(req):
    id=req.GET.get('pid')
    serverlist=viewsServer()
    env={'name':'项目编辑','version':global_env()}
    if req.method == 'GET':
        defaultContent=projectConf(pid=id).defaultProJectConf()
        response={'DEFAULT':defaultContent}
    elif req.method == 'POST':
        confContent=req.POST.get('configText')
        creatVersion=projectConf(pid=id,version=global_env(),confContent=confContent).CreateVersion()
        return HttpResponse('<script type="text/javascript">alert("配置修改完成");location.href="javascript:history.back(-1);"</script>')
    return render(req,'project-content.html',{'response':response,'env':env,'serverlist':serverlist})

# 推送配置到etcd
@login_required
def confPush(req):
    id=req.GET.get('pid')
    response=projectConf(pid=id).findProjectConf()
    keyName=response['keyName']
    value=projectConf(pid=id).defaultProJectConf()[0]['confText']
    try:
        etcdClient().writeValue(keyName,value)
    except etcd.EtcdConnectionFailed,e:
        return HttpResponse('etcd 连接失败，请检查服务是否正常')
    return HttpResponse('<script type="text/javascript">alert("推送完成");location.href="javascript:history.back(-1);"</script>')

# 项目新增
@login_required
def projectAdd(req):
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
        kid=projectConf(typed=typed,env_type=env_type,projectName=projectName,serverName=serverName,vhost=vhost,keyname=keyname).addProJectConf()
        # 关联keyid与serverid
        addHostid(sid,kid)
        return HttpResponse('<script type="text/javascript">alert("项目添加完成");location.href="/config/project/add"</script>')
    return render(req,'project-add.html',{'env':env,'serverlist':serverlist})

# 项目删除
@login_required
def projectDel(req):
    id=req.GET.get('pid')
    obtainKey=projectConf(pid=id).findProjectConf()
    try:
        keyName=obtainKey['keyName']
        delEtcd=etcdClient().delKey(keyName)
        response=projectConf(pid=id).delProJectConf()
    except:
        response=projectConf(pid=id).delProJectConf()
    return HttpResponse('<script type="text/javascript">alert("记录删除");location.href="/config/project/"</script>')

# 项目配置回滚
@login_required
def projectRollback(req):
    historyVersions=req.GET.get('versions')
    env={'name':'项目回滚编辑'}
    config=projectConf(version=historyVersions).rollback()
    pid=config[0]['kid_id'] 

    if req.method == 'GET':  
        domain=projectConf(pid=pid).defaultProJectConf()   
        response={'VERSION':domain,'DEFAULT':config}
        return render(req,'project-rollback.html',{'response':response,'env':env})
    elif req.method == 'POST':
        confContent=req.POST.get('configText')
        response=projectConf(pid=pid,version=global_env(),confContent=confContent).CreateVersion()
        return HttpResponse('<script type="text/javascript">alert("配置回滚完成，并生成新的版本号");location.href="/config/project/"</script>')
    
