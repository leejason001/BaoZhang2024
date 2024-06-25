#coding:utf8

from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime

from repository import models
from utils import myForms

def showTroubleList(request, tabs):
    myTroubles = models.troubles.objects.filter(thePoser=request.session['id_login'])
    return render(request, 'backend/troubleList.html', {'tabs':tabs, 'troubles':myTroubles})

def createNewTrouble(request, tabs):
    if 'GET' == request.method:
        return render(request, 'backend/trouble_createNewTrouble.html', {'tabs':tabs, 'troubleMakerForm': myForms.TroubleMaker()})
    elif 'POST' == request.method:
        newTroubleData = myForms.TroubleMaker(request.POST)
        if newTroubleData.is_valid():
            detailObj = models.troubleDetail.objects.create(
                detailContent = newTroubleData.cleaned_data.pop('detail')
            )
            newTroubleData.cleaned_data.update({'detail':detailObj, 'thePoser_id':request.session['id_login'], 'ctime':datetime.now()})
            models.troubles.objects.create(**newTroubleData.cleaned_data)
            return redirect('/backend/trouble/showTrouble.html')
        else:
            return render(request, 'backend/trouble_createNewTrouble.html',
                          {'tabs':tabs, 'troubleMakerForm': myForms.TroubleMaker(request.POST), 'newTroubleData':newTroubleData})

def editTrouble(request, nid, tabs):
    return HttpResponse(nid)