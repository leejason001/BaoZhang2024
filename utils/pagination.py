# coding:utf8
import math

MAX_ELEMENT_NUMS_PER_PAGE = 1
MAX_SHOW_PAGES_NUM        = 5

def returnPaginations(currentPageNum, siteArticlesNum, paginationHrefPrefix):
    MAX_PAGES_NUM = int(math.ceil(siteArticlesNum/MAX_ELEMENT_NUMS_PER_PAGE))
    normalExistedLength = int( math.ceil( MAX_SHOW_PAGES_NUM / 2.0 ) )
    paginations = []

    if MAX_PAGES_NUM < MAX_SHOW_PAGES_NUM:
        pageNum = MAX_PAGES_NUM
        for i in range( 0, pageNum ):
            paginations.append( '<a href=' + paginationHrefPrefix + '?currentPageNum=%d>%d</a>' % (i + 1, i + 1) )
    else:
        pageNum = MAX_SHOW_PAGES_NUM
        if currentPageNum-normalExistedLength <= 0:
            startPage = 1
            endPage   = MAX_SHOW_PAGES_NUM
        elif currentPageNum+normalExistedLength > MAX_PAGES_NUM:
            startPage = MAX_PAGES_NUM-MAX_SHOW_PAGES_NUM+1
            endPage   = MAX_PAGES_NUM
        else:
            startPage = currentPageNum-normalExistedLength+1
            endPage   = currentPageNum+normalExistedLength-1


        while startPage<=endPage:
            paginations.append( '<a href=' + paginationHrefPrefix + '?currentPageNum=%d>%d</a>' % (startPage, startPage))
            startPage += 1

    return ''.join(paginations), (currentPageNum-1)*MAX_ELEMENT_NUMS_PER_PAGE, (currentPageNum+1)*MAX_ELEMENT_NUMS_PER_PAGE-1
