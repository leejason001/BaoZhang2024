# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from repository import models


# Create your views here.
def index(request):
    navigationClassContent = models.articles.type_choices
    siteArticles           = models.articles.objects.all()

    return render(request, "mySite/mySite_index.html", {'articleTypes':navigationClassContent, 'siteArticles': siteArticles})
