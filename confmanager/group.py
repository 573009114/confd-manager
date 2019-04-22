# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from viewConf import *
from etcdConf import *

import time

@login_required
def groupList(req):
    env={'name':'组列表'}
    if req.method == 'GET':
        response=viewGroup()
        return render(req,'group-list.html',{'response':response,'env':env})

@login_required
def addGroup(req):
    timer=int(time.time())
    env={'name':'组添加'}
    if req.method == 'POST':
        groupname=req.POST.get('groupname')
        keyngx=req.POST.get('keyngx')
        label='/server/'+keyngx+str(timer)
        try:
            response=projectConf(groupname=groupname,keyngx=label).addGroup()
            msg='组添加完成!'
        except:
            msg="添加失败，字段内容重复！"
        return HttpResponse('<script type="text/javascript">alert("%s");location.href="/config/group/"</script>' %msg)
    return render(req,'group-add.html',{'env':env})
    
@login_required
def delGroup(req):
    id=req.GET.get('pid')
    group_response=projectConf(pid=id).findGroupid()
    ngxkey=group_response['keyngx']
    try:
        response=projectConf(pid=id).delGroup()
        etcdClient().delKey(ngxkey)
        msg='分组删除成功'
    except TypeError:
        msg='删除失败！'
    return HttpResponse('<script type="text/javascript">alert("%s");location.href="/config/group/"</script>' %msg)

@login_required
def pushGroupKey(req):
    id=req.GET.get('pid')
    group_response=projectConf(pid=id).findGroupid()
    ngxkey=group_response['keyngx']
    ngxconf=group_response['serverconfig']
    try:
        etcdClient().writeValue(ngxkey,ngxconf)
        msg='推送成功'
    except TypeError:
         msg='推送失败'
    return HttpResponse('<script type="text/javascript">alert("%s");location.href="/config/group/"</script>' %msg)


@login_required
def setGroupConfig(req):
    id=req.GET.get('pid')

    if req.method  == 'POST':
        config=req.POST.get('serverconf')
        projectConf(pid=id,config=config).editGroup()
        msg=HttpResponse('<script type="text/javascript">alert("主配置保存成功");location.href="/config/group/"</script>')
        return msg
    else:
        defaultContent=projectConf(pid=id).defaultSetGroup()
        return render(req,'group-content.html',{'response':defaultContent})


