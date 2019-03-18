# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render

def dashboard(req):
    return HttpResponse('index')