#:coding:utf8
"""BaoZhang2024 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from views import home, realViews#不同app里的views包同名,是否会发生冲突

urlpatterns = [
    url(r'^mySite/(?P<articleType>\d)/$', realViews.index, name='mySiteIndex'),
    url(r'mySite/register.html', realViews.doRegisterForm, name='register'),
    url(r'mySite/login.html', realViews.doLogin, name='login'),
    url(r'mySite/getCheckcode', realViews.getValidateCodeImage),
    url(r'mySite/logout', realViews.doLogout, name='logout'),
    url(r'(?P<surfix>\w+)\/label\/(?P<label_id>\d)\.html', home.theLabelArticles),
    url(r'(?P<surfix>\w+)\/(?P<artilce_id>\d+)\.html', home.wholeArticle ),
    url(r'^(?P<surfix>\w+)\.html$', home.index),
    url(r'^$', realViews.index),
]
