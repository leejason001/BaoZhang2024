#coding:utf8

from django.conf.urls import url
import views

tabs = [{'path':'11111', 'caption':u'文章管理'}, {'path':'22222', 'caption':u'分类管理'}, {'path':'333333333', 'caption':u'标签管理'}, {'path':'444444', 'caption':u'个人信息'}]
urlpatterns = [
    url( r'^createArticle.html$', views.createArticle, {'tabs': tabs}, ),
    url(r'(?P<one>\d*)/?(?P<two>\d*)/?', views.articleManager, {'tabs': tabs},),
]