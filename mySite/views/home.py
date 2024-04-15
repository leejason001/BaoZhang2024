#coding:utf8
from __future__ import unicode_literals
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime
from django.db import connection

from repository import models
from utils import pagination


MAX_SHOW_COMMENTSTREES = 5


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

def createCommentsDataTree(dictComments):
    for comment in dictComments.values():
        if comment.parentComment != None:
            dictComments[comment.parentComment.id].children.append(comment)

def createShowingHtmlCommentsTrees(comments):
    htmlTrees = ''
    for comment in comments:
        currentDom = '<div class="levelOffset">%s</div><div class="theComment  levelOffset" article="%d" me="%d">%s'%(comment.reader.username, comment.article.id, comment.id, comment.content,)
        currentDom += '<div class="rightLocation"><button class="replayButton">回复</button></div><div class="replayArea"><textarea></textarea><div class="leftLocation"><button class="replaySubmit">提交</button></div></div>'
        currentDom += createShowingHtmlCommentsTrees(comment.children)
        currentDom += '</div>'
        htmlTrees += currentDom
    return htmlTrees



def wholeArticle(request, *args, **kwargs):
    theBlog = models.blogs.objects.filter( surfix=kwargs['surfix'] ).first()
    article = models.articles.objects.filter(id=kwargs['artilce_id']).first()

    theLabels = []
    for label in theBlog.labels_set.all():
        label.count = models.labelArticleRelationShip.objects.filter(label_id=label.id).count()
        theLabels.append(label)

    counter = 0
    showingCommentsTrees = []
    dictComments = {}
    for comment in models.comments.objects.filter(article=article):
        comment.children = []
        dictComments[comment.id] = comment
        if None == comment.parentComment:
            # if counter < MAX_SHOW_COMMENTSTREES:#为实现 查看更多准备
                showingCommentsTrees.append(comment)
                # counter += 1#为实现 查看更多准备

    createCommentsDataTree( dictComments )
    '''
        #用于验证生成“评论树”的数据结构的正确性
        from utils import commonTools
        for treeNode in showingCommentsTrees:
            commonTools.printCurrentTree(treeNode, 1)
    '''
    showingHtmlCommentsTrees = createShowingHtmlCommentsTrees( showingCommentsTrees )



    try:
        theUserAttitude = models.readerAttitude.objects.get(reader=theBlog.owner, article=article)

    except:
        return render( request, 'mySite/article.html',
                       {'theBlog': theBlog, 'article': article, 'labels': theLabels, 'commentsTrees': mark_safe(showingHtmlCommentsTrees)} )
    if 0 == theUserAttitude.attitude:
        return render( request, 'mySite/article.html',
                       {'theBlog': theBlog, 'article': article, 'labels': theLabels, 'favor':1, 'commentsTrees': mark_safe(showingHtmlCommentsTrees)} )
    elif 1 == theUserAttitude.attitude:
        return render( request, 'mySite/article.html',
                       {'theBlog': theBlog, 'article': article, 'labels': theLabels, 'oppose': 1, 'commentsTrees': mark_safe(showingHtmlCommentsTrees)} )


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


    paginationHrefPrefix = '/' + theBlog.surfix + '/date/' + kwargs['theDate'] + '.html'
    try:
        currentPageNum         = int(request.GET.get('currentPageNum'))
    except:
        currentPageNum         = 1
    paginations, startItemNum, endItemNum = pagination.returnPaginations( currentPageNum, len(list(articles)),
                                                                          paginationHrefPrefix )

    return render(request, 'mySite/home.html', {'theBlog':theBlog, 'articles':articles[startItemNum:endItemNum], 'paginations':mark_safe(paginations)})

def userAttitleTheArticle(request):
    ATTITUDE_FAVOR  = 0
    ATTITUDE_OPPOSE = 1
    ON_ATTITUDE     = 1
    OFF_ATTITUDE    = -1
    try:
        theArticle = models.articles.objects.get(id=request.POST.get('articleId'))
        theDirection = int(request.POST.get('direction'))
        theAttitude  = int(request.POST.get('attitude'))


        if theDirection == ON_ATTITUDE:
            models.readerAttitude.objects.create(reader=models.users.objects.filter(blogs__surfix=request.POST.get('surfix')).first(), article=theArticle, attitude=theAttitude)

            if ATTITUDE_FAVOR == theAttitude:
                theArticle.favorCount += 1
            elif ATTITUDE_OPPOSE == theAttitude:
                theArticle.opposeCount += 1
            else:
                print 'theAttitude is Strange!!'
            theArticle.save()
        elif theDirection == OFF_ATTITUDE:
            models.readerAttitude.objects.filter(reader=models.users.objects.filter(blogs__surfix=request.POST.get('surfix')).first(), article=theArticle).delete()

            if ATTITUDE_FAVOR == theAttitude:
                theArticle.favorCount -= 1
            elif ATTITUDE_OPPOSE == theAttitude:
                theArticle.opposeCount -= 1
            else:
                print 'theAttitude is Strange!!'
            theArticle.save()
        else:
            print "theDirection is Strange!!!!"
    except:
        return HttpResponse('failed')
    return HttpResponse('success')

def readerCommentTheArticle(request):

    try:
        article_id = int(request.POST.get( "article_id" ))
        commentContent = request.POST.get( "content" )
    except:
        print "request error"
    if request.POST.get("parentComment"):
        commentObj = models.comments.objects.create(reader_id=request.session['id_login'], article_id=article_id,
                                       content=commentContent, ctime=datetime.now(),parentComment_id=int(request.POST.get("parentComment")))
    else:
        commentObj = models.comments.objects.create( reader_id=request.session['id_login'], article_id=article_id,
                                        content=commentContent, ctime=datetime.now())

    return JsonResponse({"comment_id": commentObj.id, "username": request.session["username"]})

