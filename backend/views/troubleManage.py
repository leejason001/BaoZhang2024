#coding:utf8

from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from repository import models

def showTroubleList(request, tabs):
    myTroubles = models.troubles.objects.filter(thePoser=request.session['id_login'])
    return render(request, 'backend/troubleList.html', {'tabs':tabs, 'troubles':myTroubles})