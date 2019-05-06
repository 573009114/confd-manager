# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from viewConf import *

@login_required
def dashboard(req):
    env={'name':'系统主页'}
    response={
    'data1':TotalIndex().select_ipcount(),
    'data2':TotalIndex().select_pronum(),
    'data3':TotalIndex().select_groupnum(),
    }
    return render(req,'index.html',{'response':response,'env':env})