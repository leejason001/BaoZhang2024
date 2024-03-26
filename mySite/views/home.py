#coding:utf8
from __future__ import unicode_literals
from django.shortcuts import HttpResponse, redirect, render
from django.utils.safestring import mark_safe

from repository import models
from utils import pagination


def index(request, *args, **kwargs):
    theUser = models.users.objects.filter(id=request.session['id_login']).first()
    theBlog = models.blogs.objects.filter(owner_id=request.session['id_login']).first()
    articles= models.articles.objects.filter(ownerBlog=theBlog)
    paginationHrefPrefix = '/' + theBlog.surfix + '.html'
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


    return render(request, 'mySite/home.html', {'user':theUser,'theBlog':theBlog, 'articles':articles[startItemNum:endItemNum], 'paginations':mark_safe(paginations),'themeCS_Navigator':'', 'labels': theLabels, 'classifications': theBlog.classifications_set.all()})

def wholeArticle(request, *args, **kwargs):
    theBlog = models.blogs.objects.filter( owner_id=request.session['id_login'] ).first()
    article = models.articles.objects.filter(id=kwargs['artilce_id']).first()
    return render(request, 'mySite/article.html', {'theBlog':theBlog, 'article':article, 'labels':theBlog.labels_set.all()})

def theLabelArticles(request, *args, **kwargs):
    theBlog = models.blogs.objects.filter(owner_id=request.session['id_login']).first()
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

    return render(request, 'mySite/home.html', {'theBlog':theBlog, 'articles':articles[startItemNum:endItemNum], 'paginations':mark_safe(paginations), 'labels': theLabels, 'classifications': theBlog.classifications_set.all()})