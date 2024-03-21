# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse

from repository import models
from utils import pagination, myForms


# Create your views here.


def index(request, *args, **kwargs):
    if kwargs:
        paginationHrefPrefix = reverse('mySiteIndex', kwargs=kwargs)
    else:
        paginationHrefPrefix = '/'

    siteArticles = models.articles.objects.filter(**kwargs)

    try:
        currentPageNum         = int(request.GET.get('currentPageNum'))
    except:
        currentPageNum         = 1

    paginations, startItemNum, endItemNum            = pagination.returnPaginations(currentPageNum, siteArticles.count(), paginationHrefPrefix)

    return render(request, "mySite/mySite_index.html", {'articleTypes':models.articles.type_choices, 'siteArticles': siteArticles[startItemNum:endItemNum], 'paginations':mark_safe(paginations)})


def doRegisterForm(request):
    if 'GET' == request.method:
        return render( request, "mySite/register.html", {'registerForm': myForms.registerForm()} )
    elif 'POST' == request.method:
        registerForm = myForms.registerForm(request.POST)
        if registerForm.is_valid():
            registerData = registerForm.clean()
            models.users.objects.create(username=registerData['username'], password=registerData['password'], email=registerData['email'], headPicture_path=registerData['headPicture_path'])
            return redirect('/')
        else:
            return render(request, "mySite/register.html", {'registerForm': registerForm})


