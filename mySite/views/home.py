#coding:utf8
from __future__ import unicode_literals
from django.shortcuts import HttpResponse, redirect, render
from repository import models


def index(request, *args, **kwargs):
    theBlog = models.blogs.objects.filter(owner_id=request.session['id_login']).first()
    articles= list(models.articles.objects.filter(ownerBlog=theBlog))

    return render(request, 'mySite/home.html', {'theBlog':theBlog, 'articles':articles, 'themeCS_Navigator':'', 'labels':theBlog.labels_set.all(), 'classifications': theBlog.classifications_set.all()})