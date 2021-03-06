# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm


# 登录模块
def login(req):
    if req.method == "POST":
        form = AuthenticationForm(req, data=req.POST)
        if form.is_valid():
            auth.login(req, form.get_user())
            return HttpResponseRedirect('/')
        else:
            return render(req,'login.html',{"msg":"用户名不存在，或者密码错误！"})
    else:
        form = AuthenticationForm(req)

    kwargs = {
        'form': form,
    }
    return render(req, 'login.html', kwargs)


# 注销模块
def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/login/')

# 修改密码模块
def channgePwd(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        old_password=req.POST.get('oldpassword')
        new_password1=req.POST.get('newpassword')
        repeat_password=req.POST.get('repeatpassword')
        response={}
        if repeat_password != new_password1:
            response['data']='您的确认密码和新密码不匹配'
        else:
            new_password=new_password1
            if len(new_password)>8:
                user = auth.authenticate(username=username, password=old_password)
                if user is not None and user.is_active:
                    user.set_password(new_password)
                    user.save()
                    response['data']='密码修改成功'     
                else:
                    response['data']='原密码错误'
            else:
                response['data']='密码长度小于8位'
        return render(req,'channge.html',{'response':response})
    else:
        return render(req,'channge.html')
    
