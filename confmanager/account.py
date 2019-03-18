# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth

# 登录模块
def login(req):
    if req.method == 'GET':
        return render(req,'login.html')
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user and user.is_active:
            auth.login(req,user)
            req.session['username'] = username
            return HttpResponseRedirect('/config/project/')
        else:
            return render(req,'login.html',{"msg":"用户名不存在，或者密码错误！"}) 

# 注销模块
def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/login/')
    