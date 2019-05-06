# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from viewConf import *


def dashboard(req):
    env={'name':'系统主页'}
    response={
    'data1':TotalIndex().select_ipcount(),
    'data2':TotalIndex().select_pronum(),
    'data3':TotalIndex().select_groupnum(),
    }
    return render(req,'index.html',{'response':response,'env':env})