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
        theTrouble = models.troubles.objects.filter(id=nid, status=0).only('id', 'title', 'summary').first()
        if not theTrouble:
            return HttpResponse(u'已接单，不能修改')
        theTroubleDetail = models.troubleDetail.objects.get(id=theTrouble.detail.id)
        return render(request, 'backend/trouble_editTrouble.html', {'tabs': tabs, 'trouble_id': nid,
                                                                    'troubleEditForm': myForms.TroubleMaker(data={'title':theTrouble.title,
                                                                                                                  'summary':theTrouble.summary,
                                                                                                                  'detail': theTroubleDetail.detailContent})})
    elif 'POST' == request.method:
        editTroubleForm = myForms.TroubleMaker(request.POST)
        if editTroubleForm.is_valid():

            theTroubleDetail = models.troubleDetail.objects.filter( id=models.troubles.objects.get(id=nid).detail.id )
            v = models.troubles.objects.filter(id=nid, status=0).update(
                title=editTroubleForm.cleaned_data['title'],
                summary=editTroubleForm.cleaned_data['summary'],
                detail=theTroubleDetail[0]
            )
            if 0 == v:
                return HttpResponse( u"已接单，不能修改" )
            else:
                theTroubleDetail.update( detailContent=editTroubleForm.cleaned_data.pop( 'detail' ) )
                return redirect( '/backend/trouble/showTrouble.html' )
        else:
            return render(request, 'backend/trouble_editTrouble.html', {'tabs': tabs, 'trouble_id': nid,
                                                                        'troubleEditForm': editTroubleForm})

def showTroubleKillList(request, tabs):
    from django.db.models import Q
    troubles = models.troubles.objects.filter(Q(thePoser_id=request.session['id_login'])|Q(status=0)).only('title', 'status', 'ctime', 'thePoser').order_by('status')
    return render(request, 'backend/troubleKillList.html', {'troubles':troubles, 'tabs':tabs})

def robTrouble(request, nid, tabs):
    print(nid)
    print(models.troubles.objects.filter(id=nid, status=0))
    rowNumber = models.troubles.objects.filter(id=nid, status=0).update(status=1, theProcesser_id=request.session['id_login'])
    if not rowNumber:
        return HttpResponse('手速太慢了')
    return render(request, 'backend/trouble_solveTrouble.html', {'tabs': tabs,
                                                                 'solutionForm': myForms.solveTroubleForm(),
                                                                 'trouble':models.troubles.objects.get(id=nid)})

def solveTrouble(request, nid, tabs):
    theTrouble = models.troubles.objects.get( id=nid, status=1, theProcesser_id=request.session['id_login'] )
    if 'GET' == request.method:
        if not theTrouble:
            return HttpResponse('单子已被别人抢走')
        else:
            return render(request, 'backend/trouble_solveTrouble.html', {'tabs':tabs,
                                                                         'solutionForm': myForms.solveTroubleForm(),
                                                                         'trouble':theTrouble})
    elif 'POST' == request.method:
        if not theTrouble:
            return HttpResponse('去你妈的')
        theSolutionForm = myForms.solveTroubleForm(request.POST)
        if theSolutionForm.is_valid():
            lineNumber = models.troubles.objects.filter(id=nid, status=1).update(status=2, solution=theSolutionForm.cleaned_data['solution'], ptime=datetime.now())
            if not lineNumber:
                return HttpResponse('修改失败')
            return redirect('/backend/trouble/trouble-killList.html')
        else:
            return render(request, 'backend/trouble_solveTrouble.html', {'tabs':tabs,
                                                                         'solutionForm': theSolutionForm,
                                                                         'trouble':theTrouble})

def seekTheSolution(request, nid, tabs):
    theTrouble = models.troubles.objects.get(id=nid, thePoser=request.session['id_login'])
    if not theTrouble:
        return HttpResponse('你无权查看')
    if 'GET' == request.method:
        data={'marks': theTrouble.mark} if theTrouble.mark else {'marks': 3}
        return render(request, 'backend/seekTheSolution.html', {'tabs':tabs, 'trouble': theTrouble, 'seekTroubleSolutionForm': myForms.seekTroubleSolutionForm(
            data=data
        )})
    elif 'POST' == request.method:
        theForm = myForms.seekTroubleSolutionForm(request.POST)
        if theForm.is_valid():
            theTrouble.mark = theForm.cleaned_data['marks']
            theTrouble.save()
            return redirect('/backend/trouble/trouble-killList.html')
        else:
            return render(request, 'backend/seekTheSolution.html', {'tabs':tabs, 'trouble': theTrouble, 'seekTroubleSolutionForm': theForm})
