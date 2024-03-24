#coding:utf8
from __future__ import unicode_literals
from django.shortcuts import HttpResponse, redirect, render

def index(request, *args, **kwargs):
    print kwargs
    return HttpResponse(kwargs)