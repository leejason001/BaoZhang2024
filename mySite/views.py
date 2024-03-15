# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.utils.safestring import mark_safe

from repository import models
from utils import pagination

# Create your views here.
classficiationChoosen = None

def index(request):
    navigationClassContent = models.articles.type_choices
    global classficiationChoosen

    if classficiationChoosen == None or request.GET.get( 'classficiationChoosen' ) != None:
        classficiationChoosen = request.GET.get( 'classficiationChoosen' )
    if None == classficiationChoosen or 'all' == classficiationChoosen.strip():
        siteArticles = models.articles.objects.all()
    else:
        siteArticles = models.articles.objects.filter(articleType=int(classficiationChoosen))
    try:
        currentPageNum         = int(request.GET.get('currentPageNum'))
    except:
        currentPageNum         = 1
    paginationHrefPrefix   = "/site/index.html"
    paginations, startItemNum, endItemNum            = pagination.returnPaginations(currentPageNum, siteArticles.count(), paginationHrefPrefix)
    # print startItemNum, endItemNum
    # print siteArticles[startItemNum:endItemNum]
    return render(request, "mySite/mySite_index.html", {'articleTypes':navigationClassContent, 'siteArticles': siteArticles[startItemNum:endItemNum], 'paginations':mark_safe(paginations)})
