# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from repository import models
admin.site.register(models.users)
class blogsAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
admin.site.register(models.blogs, blogsAdmin)
admin.site.register(models.reportTroubles)
admin.site.register(models.classifications)
admin.site.register(models.articlesDetail)
class articlesAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(models.articles, articlesAdmin)
admin.site.register(models.labels)
admin.site.register(models.labelArticleRelationShip)
admin.site.register(models.readerAttitude)
admin.site.register(models.comments)

admin.site.register(models.troubles)
admin.site.register(models.troubleDetail)
admin.site.register(models.solutionAlternated)

