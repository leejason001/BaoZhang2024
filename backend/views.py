# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime

from repository import models
from utils import myForms
# Create your views here.

def editArticle(request, tabs, article_id):
    if 'GET' == request.method:
        theArticle = models.articles.objects.get(id=article_id)
        articleFormObj = myForms.articleForm(request=request,
            data={
                "title"         :theArticle.title,
                "summary"       :theArticle.summary,
                "content"       :theArticle.detail.content,
                "articleType"   :theArticle.articleType,
                "classifications":theArticle.classification,
                "labels"        :theArticle.labelarticlerelationship_set.values('label')
            }
        )
        print(theArticle.detail.content)
        return render(request, 'backend/articleBase.html', {'tabs':tabs, 'theTabCaption': u'文章管理', 'crumbs': [u'创建文章'], 'articleForm':articleFormObj})

def createArticle(request, tabs):
    if 'GET' == request.method:
        return render(request, 'backend/createArticle.html', {'tabs':tabs, 'theTabCaption': u'文章管理', 'crumbs': [u'创建文章'], 'articleForm':myForms.articleForm(request)})
    elif 'POST' == request.method:
        value = myForms.articleForm(request, request.POST)
        # print(value.errors)
        if value.is_valid():
            articleDetailObj = models.articlesDetail.objects.create(
                content = request.POST.get('content')
            )
            classificationObj = models.classifications.objects.get(id=request.POST.get('classifications'))
            articleObj = models.articles.objects.create(
                title = request.POST.get('title'),
                summary = request.POST.get('summary'),
                ownerBlog_id = request.session['blog_id'],
                ctime = datetime.now(),
                detail = articleDetailObj,
                articleType = request.POST.get('articleType'),
                classification = classificationObj
            )
            models.labelArticleRelationShip.objects.create(
                label_id = request.POST.get("labels"),
                article = articleObj
            )
            return redirect('/backend/')
        else:
            return render(request, 'backend/createArticle.html', {'tabs':tabs, 'theTabCaption': u'文章管理', 'crumbs': [u'创建文章'],
                                                                  'articleForm':myForms.articleForm(request), 'value':value})



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
