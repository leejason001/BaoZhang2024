# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

from repository import models
# Create your views here.

def articleManager(request, tabs):
    try:
        theBlog = models.blogs.objects.filter(owner_id=request.session['id_login'])
        classifications = models.classifications.objects.filter(owner=theBlog)
        labels          = models.labels.objects.filter(toBlog=theBlog)
        articles        = models.articles.objects.filter(ownerBlog=theBlog)
        return render(request, 'backend/articleManager.html', {'tabs': tabs, 'theTabCaption': u'文章管理', 'crumbs': [u'文章列表'], 'classifications': classifications, 'labels':labels, 'articles': articles})
    except:
        return HttpResponse(u'请先登录')
