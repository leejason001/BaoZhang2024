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
    if 'GET' == request.method:
        theTrouble = models.troubles.objects.get(id=nid)
        theTroubleDetail = models.troubleDetail.objects.get(id=theTrouble.detail.id)
        return render(request, 'backend/trouble_editTrouble.html', {'tabs': tabs, 'trouble_id': nid,
                                                                    'troubleEditForm': myForms.TroubleMaker(data={'title':theTrouble.title,
                                                                                                                  'summary':theTrouble.summary,
                                                                                                                  'detail': theTroubleDetail.detailContent})})
    elif 'POST' == request.method:
        editTroubleForm = myForms.TroubleMaker(request.POST)
        if editTroubleForm.is_valid():
            theTrouble       = models.troubles.objects.filter(id=nid, status=0)
            if theTrouble:
                theTroubleDetail = models.troubleDetail.objects.filter( id=theTrouble[0].detail.id )
                theTroubleDetail.update( detailContent=editTroubleForm.cleaned_data.pop( 'detail' ) )
                editTroubleForm.cleaned_data.update( {'detail': theTroubleDetail} )
                theTrouble.update(
                    title=editTroubleForm.cleaned_data['title'],
                    summary=editTroubleForm.cleaned_data['summary'],
                    detail=theTroubleDetail[0]
                )

                return redirect( '/backend/trouble/showTrouble.html' )
            else:
                return HttpResponse(u"已接单，不能修改")
        else:
            return render(request, 'backend/trouble_editTrouble.html', {'tabs': tabs, 'trouble_id': nid,
                                                                        'troubleEditForm': myForms.TroubleMaker(request.POST)})
