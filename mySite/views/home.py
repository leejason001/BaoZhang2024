#coding:utf8
from __future__ import unicode_literals
from django.shortcuts import HttpResponse, redirect, render

def index(request, *args, **kwargs):

    return render(request, 'mySite/home.html', {'themeCS_Navigator':''})