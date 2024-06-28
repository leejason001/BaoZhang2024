#coding:utf8

from django.conf.urls import url
from .views import backendManage
from .views import troubleManage

tabs = [{'path':'11111', 'caption':u'文章管理'}, {'path':'22222', 'caption':u'分类管理'}, {'path':'333333333', 'caption':u'标签管理'}, {'path':'444444', 'caption':u'个人信息'}]
urlpatterns = [
    url( r'^createArticle.html$', backendManage.createArticle, {'tabs': tabs}, ),
    url( r'^editArticle/(?P<article_id>\d+).html$', backendManage.editArticle, {'tabs': tabs}),
    url(r'^(?P<one>\d*)/?(?P<two>\d*)/?$', backendManage.articleManager, {'tabs': tabs},),
    url(r'trouble/showTrouble.html', troubleManage.showTroubleList, {'tabs': tabs}),
    url(r'trouble/createNewTrouble.html', troubleManage.createNewTrouble, {'tabs': tabs}),
    url(r'trouble/trouble-edit-(\d)+.html', troubleManage.editTrouble, {'tabs': tabs}),
    url(r'trouble/trouble-killList.html', troubleManage.showTroubleKillList, {'tabs': tabs}),
    url(r'trouble/trouble-rob-(\d)+.html', troubleManage.robTrouble, {'tabs': tabs}),
]