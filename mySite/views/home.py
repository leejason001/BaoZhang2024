#coding:utf8
from __future__ import unicode_literals
from django.shortcuts import HttpResponse, redirect, render
from django.utils.safestring import mark_safe
from django.db import connection

from repository import models
from utils import pagination


def index(request, *args, **kwargs):
    blogAndUserTable = models.blogs.objects.all().select_related('owner')

    theBlogAndUser = blogAndUserTable.filter(surfix=kwargs['surfix']).first()
    articles= models.articles.objects.filter(ownerBlog_id=theBlogAndUser.id)
    paginationHrefPrefix = '/' + theBlogAndUser.surfix + '.html'
    try:
        currentPageNum         = int(request.GET.get('currentPageNum'))
    except:
        currentPageNum         = 1
    paginations, startItemNum, endItemNum = pagination.returnPaginations( currentPageNum, articles.count(),
                                                                          paginationHrefPrefix )
    theLabels = []
    for label in theBlogAndUser.labels_set.all():
        label.count = models.labelArticleRelationShip.objects.filter(label_id=label.id).count()
        theLabels.append(label)

    dates = models.articles.objects.raw('select id, count(id) as theCount, strftime("%Y-%m", "ctime") as theTime from repository_articles group by strftime("%Y-%m", "ctime")')

    return render(request, 'mySite/home.html', {'user':theBlogAndUser,'theBlog':theBlogAndUser, 'articles':articles[startItemNum:endItemNum], 'paginations':mark_safe(paginations),'labels': theLabels, 'dates':dates})

def wholeArticle(request, *args, **kwargs):
    theBlog = models.blogs.objects.filter( surfix=kwargs['surfix'] ).first()
    article = models.articles.objects.filter(id=kwargs['artilce_id']).first()

    theLabels = []
    for label in theBlog.labels_set.all():
        label.count = models.labelArticleRelationShip.objects.filter(label_id=label.id).count()
        theLabels.append(label)
    return render(request, 'mySite/article.html', {'theBlog':theBlog, 'article':article, 'labels':theLabels})

def theLabelArticles(request, *args, **kwargs):
    theBlog = models.blogs.objects.filter( surfix=kwargs['surfix'] ).first()
    articles    = models.articles.objects.filter(labelarticlerelationship__label__id=kwargs['label_id'])

    paginationHrefPrefix = '/' + theBlog.surfix + '/label/' + kwargs['label_id'] + '.html'
    try:
        currentPageNum         = int(request.GET.get('currentPageNum'))
    except:
        currentPageNum         = 1
    paginations, startItemNum, endItemNum = pagination.returnPaginations( currentPageNum, articles.count(),
                                                                          paginationHrefPrefix )

    theLabels = []
    for label in theBlog.labels_set.all():
        label.count = models.labelArticleRelationShip.objects.filter(label_id=label.id).count()
        theLabels.append(label)

    return render(request, 'mySite/home.html', {'theBlog':theBlog, 'articles':articles[startItemNum:endItemNum], 'paginations':mark_safe(paginations), 'labels': theLabels})

def theDateArticles(request, *args, **kwargs):
    theBlog = models.blogs.objects.filter(surfix=kwargs['surfix']).first()
    articles = models.articles.objects.filter( ownerBlog=theBlog ).extra(
        where=['strftime("%%Y-%%m",ctime)=%s'], params=[kwargs['theDate'], ] ).all()
    print list(articles)

    paginationHrefPrefix = '/' + theBlog.surfix + '/date/' + kwargs['theDate'] + '.html'
    try:
        currentPageNum         = int(request.GET.get('currentPageNum'))
    except:
        currentPageNum         = 1
    paginations, startItemNum, endItemNum = pagination.returnPaginations( currentPageNum, len(list(articles)),
                                                                          paginationHrefPrefix )

    return render(request, 'mySite/home.html', {'theBlog':theBlog, 'articles':articles[startItemNum:endItemNum], 'paginations':mark_safe(paginations)})
