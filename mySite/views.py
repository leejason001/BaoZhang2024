# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.utils.safestring import mark_safe

from repository import models
from utils import pagination

# Create your views here.
def index(request):
    navigationClassContent = models.articles.type_choices
    siteArticles           = models.articles.objects.all()
    try:
        currentPageNum         = int(request.GET.get('currentPageNum'))
    except:
        currentPageNum         = 1
        print 111111
    paginationHrefPrefix   = "/site/index.html"
    paginations, startItemNum, endItemNum            = pagination.returnPaginations(currentPageNum, siteArticles.count(), paginationHrefPrefix)
    # print startItemNum, endItemNum
    # print siteArticles[startItemNum:endItemNum]
    return render(request, "mySite/mySite_index.html", {'articleTypes':navigationClassContent, 'siteArticles': siteArticles[startItemNum:endItemNum], 'paginations':mark_safe(paginations)})
