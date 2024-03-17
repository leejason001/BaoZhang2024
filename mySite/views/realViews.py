# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.utils.safestring import mark_safe
from django.urls import reverse

from repository import models
from utils import pagination

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
