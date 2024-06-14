# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

from repository import models
from utils import myForms
# Create your views here.

def createArticle(request, tabs):
    return render(request, 'backend/createArticle.html', {'tabs':tabs, 'theTabCaption': u'文章管理', 'crumbs': [u'创建文章'], 'articleForm':myForms.articleForm(request)})



def articleManager(request, tabs, one, two):
    try:
        theBlog = models.blogs.objects.filter(owner_id=request.session['id_login'])
    except:
        return HttpResponse( u'请先登录' )


    request.session['blog_id'] = theBlog.first().id

    classifications = models.classifications.objects.filter(owner=theBlog)
    labels          = models.labels.objects.filter(toBlog=theBlog)
    if one!='' and two!='':
        articles        = models.articles.objects.filter(ownerBlog=theBlog, classification_id=int(one), labelarticlerelationship__label__id=int(two))
    elif one != '':
        articles        = models.articles.objects.filter(ownerBlog=theBlog, classification_id=int(one))
    elif two != '':
        articles        = models.articles.objects.filter(ownerBlog=theBlog, labelarticlerelationship__label__id=int(two))
    else:
        articles = models.articles.objects.filter( ownerBlog=theBlog )

    flat = {"one":one, "two": two}

    return render(request, 'backend/articleManager.html', {'tabs': tabs, 'theTabCaption': u'文章管理', 'crumbs': [u'文章列表'], 'classifications': classifications, 'labels':labels, 'articles': articles, 'flat': flat})
