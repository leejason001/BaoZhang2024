# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime

from repository import models
from utils import myForms
# Create your views here.

def editArticle(request, tabs, article_id):
    theArticle = models.articles.objects.get( id=article_id )
    if 'GET' == request.method:
        articleFormObj = myForms.articleForm(request=request,
            data={
                "title"         :theArticle.title,
                "summary"       :theArticle.summary,
                "content"       :theArticle.detail.content,
                "articleType"   :theArticle.articleType,
                "classifications":theArticle.classification_id,
                "labels"        :theArticle.labelarticlerelationship_set.values_list('label')[0]
            }
        )
        return render(request, 'backend/articleBase.html', {'tabs':tabs, 'theTabCaption': u'文章管理', 'crumbs': [u'创建文章'], 'articleForm':articleFormObj})
    elif 'POST' == request.method:
        value = myForms.articleForm( request, request.POST )
        if value.is_valid():
            content = value.cleaned_data.pop('content')
            labels  = value.cleaned_data.pop('labels')
            value.cleaned_data["ownerBlog"] = theArticle.ownerBlog
            value.cleaned_data["classification"] = value.cleaned_data.pop('classifications')
            models.articlesDetail.objects.filter(id=theArticle.detail.id).update(content=content)
            models.labelArticleRelationShip.objects.filter(article=theArticle).delete()
            label_list = []
            for label in labels:
                label_list.append(models.labelArticleRelationShip(article=theArticle, label_id=int(label)))
            models.labelArticleRelationShip.objects.bulk_create(label_list)
            models.articles.objects.filter(id=theArticle.id).update(**value.cleaned_data)
            return redirect( '/backend' )
        else:
            return render(request, 'backend/createArticle.html', {'tabs':tabs, 'theTabCaption': u'文章管理', 'crumbs': [u'创建文章'],
                                                                  'articleForm':myForms.articleForm(request, request.POST), 'value':value})


def createArticle(request, tabs):
    if 'GET' == request.method:
        return render(request, 'backend/createArticle.html', {'tabs':tabs, 'theTabCaption': u'文章管理', 'crumbs': [u'创建文章'], 'articleForm':myForms.articleForm(request,
                                                                                                                                                            data={
                                                                                                                                                                "articleType": 1,
                                                                                                                                                                "classifications": 1,
                                                                                                                                                                "labels":1
                                                                                                                                                            }
                                                                                                                                                            )})
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

def menu_content(nodeList):
    response = ''
    menuDomNode = """
        <div class="item %s">
            <div class="caption">%s</div>
            <div class="content">%s</div>
        </div>
    """
    for node in nodeList:
        print(node)
        if(False == node['saved']):
            continue
        active = ''
        if(True == node['expand']):
            active = 'active'
        if('url' in node):
            response += "<a class='%s' href='%s'>%s</a>" % (active, node['url'], node['caption'])
        else:
            content = menu_content(node['child'])
            response += menuDomNode %(active, node['caption'], content)
    return response

def showMenuTree(request):
    currentLeaf = request.path_info
    menu_leaf_list = request.session['permission_action_info']['menu_leaf_list']
    menu_leaf_dict={}
    for item in menu_leaf_list:
        item = {
            'id':     item['permission_id'],
            'url':    item['permission__url'],
            'caption':item['permission__caption'],
            'parent_id': item['permission__menu'],
            'saved'    : True,
            'expand'   : False,
            'child':     [],
        }
        if(item['parent_id'] in menu_leaf_dict):
            menu_leaf_dict[item['parent_id']].append(item)
        else:
            menu_leaf_dict[item['parent_id']] = [item,]
            
    menu_list = request.session['permission_action_info']['menu_list']
    
    menu_dict = {}
    for menu in menu_list:
        menu['child'] = []
        menu['saved'] = False
        menu['expand'] = False
        menu_dict[menu['id']] = menu

    for k,v in menu_leaf_dict.items():
        menu_dict[k]['child'] = v
        parentMenu = k
        while parentMenu:
            if False == menu_dict[parentMenu]['saved']:
                menu_dict[parentMenu]['saved'] = True
                parentMenu = menu_dict[parentMenu]['parentMenu']
            else:
                break

    result = []

    for row in menu_dict.values():
        if not row['parentMenu']:
            result.append(row)
        else:
            menu_dict[row['parentMenu']]['child'].append(row)
    # for k,v in menu_dict.items():
    #     currentParent = menu_dict[k]['parent_id']
    #     if not currentParent:
    #         result.append(v)
    #     else:
    #         menu_dict[currentParent]['child'].append(v)        
            
            
    parentMenu = -1
    for v in menu_leaf_dict.values():
        for item in v:
            print(item['url'])
            print(currentLeaf)
            if item['url'] == currentLeaf:
                parentMenu = item['parent_id']
    if parentMenu ==-1:
        return HttpResponse('The permission of url is error!')


    while parentMenu:
        menu_dict[parentMenu]['expand'] = True
        parentMenu = menu_dict[parentMenu]['parentMenu']

    menuDomTrees = ''
    menuTreeNode = """
        <div class="item %s">
            <div class="title">%s</div>
            <div class="content">%s</div>
        </div>
    """
    for menuTree in result:
        if False == menuTree['saved']:
            continue
        active=""
        if True == menuTree['expand']:
            active = 'active'
        title = menuTree['caption']
        content = menu_content(menuTree['child'])
        menuDomTrees += menuTreeNode %(active, title, content)

    return render(request, 'backend/showMenuTree.html', {'menuDomTrees':menuDomTrees})