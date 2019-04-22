# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from viewConf import *

@login_required
def serverList(req):
    env={'name':'IP列表'}
    if req.method == 'GET':
        response=viewsServer()
        return render(req,'server-list.html',{'response':response,'env':env})

@login_required
def serverAdd(req):
    env={'name':'IP添加'}
    groupname=viewGroup()

    if req.method == 'POST':
        serverip=req.POST.get('serverip')
        groupid=req.POST.get('group_id')
   
        try:
            response=projectConf(serverip=serverip,groupid=groupid).addServer()
            msg=HttpResponse('<script type="text/javascript">alert("添加完成");location.href="/config/server/"</script>')
        except:
            msg=HttpResponse('<script type="text/javascript">alert("IP已存在，添加失败");location.href="/config/server/"</script>')
        return msg
    return render(req,'server-add.html',{'env':env,'group':groupname})


@login_required
def serverDel(req):
    id=req.GET.get('pid')
    response=projectConf(pid=id).delServer()
    return HttpResponse('<script type="text/javascript">alert("记录删除");location.href="/config/server/"</script>')

