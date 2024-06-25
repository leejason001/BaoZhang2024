# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class users(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=10)
    email    = models.EmailField(max_length=16)
    headPicture_path = models.CharField(max_length=128)


class blogs(models.Model):
    title = models.CharField(max_length=32)
    summary = models.CharField(max_length=128)
    owner   = models.OneToOneField(to=users)
    surfix  = models.CharField(max_length=64, unique=True)

    themeChoices = [
        (0, "homeBlue"),
        (1, "homeRed"),
    ]
    theme   = models.IntegerField(choices=themeChoices)

    def __str__(self):
        return self.title

class reportTroubles(models.Model):
    uid = models.UUIDField(max_length=16)
    title = models.CharField(max_length=32)
    detail = models.CharField(max_length=256)
    reportPerson = models.ForeignKey(to=users, related_name="report_person")
    dealPerson   = models.ForeignKey(to=users, related_name="deal_person", null=True, blank=True)
    ctime        = models.DateTimeField()
    Dtime        = models.DateTimeField()

    statusTypes = [
        (0, "willDeal"),
        (1, "Dealing"),
        (2, "Dealed"),
    ]
    status      = models.IntegerField(choices=statusTypes)

class classifications(models.Model):
    className = models.CharField(max_length=16)
    owner     = models.ForeignKey(to=blogs)
    def __str__(self):
        return self.className

class articlesDetail(models.Model):
    content = models.TextField()

class articles(models.Model):
    title    = models.CharField(max_length=16)
    summary  = models.CharField(max_length=64)
    ownerBlog= models.ForeignKey(to=blogs)
    ctime    = models.DateTimeField()
    detail   = models.OneToOneField(to=articlesDetail)

    type_choices = [
        (0, "Python"),
        (1, "Linux"),
        (2, "OpenStack"),
        (3, "GoLang"),
    ]
    articleType    = models.IntegerField(choices=type_choices)
    classification = models.ForeignKey(to=classifications)
    favorCount     = models.IntegerField(default=0)
    opposeCount    = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class labels(models.Model):
    labelName = models.CharField(max_length=16)
    toBlog     = models.ForeignKey(to=blogs)
    def __str__(self):
        return self.labelName

class labelArticleRelationShip(models.Model):
    label    = models.ForeignKey(to=labels)
    article  = models.ForeignKey(to=articles)

    class Meta:
        unique_together = ("label", "article")

class readerAttitude(models.Model):
    reader  = models.ForeignKey(to=users)
    article = models.ForeignKey(to=articles)

    attitudeType = (
        (0, "favor"),
        (1, "oppose"),
    )
    attitude = models.IntegerField(choices=attitudeType)

    class Meta:
        unique_together = ("reader", "article")

class comments(models.Model):
    reader  = models.ForeignKey(to=users)
    article = models.ForeignKey(to=articles)
    content = models.CharField(max_length=128)
    ctime   = models.DateTimeField()
    parentComment = models.ForeignKey(to='self', to_field='id', related_name='back', null=True, blank=True)

    class Meta:
        ordering = ("-ctime",)

    def __str__(self):
        return  self.content

class troubleDetail(models.Model):
    detailContent = models.TextField()

class troubles(models.Model):
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=256)
    detail  = models.ForeignKey(to=troubleDetail)
    thePoser= models.ForeignKey(to=users, related_name='poser')
    ctime   = models.DateTimeField()

    markChoices = (
        (0, 'bad'),
        (1, 'common'),
        (2, 'good'),
    )
    mark  = models.IntegerField(choices=markChoices, null=True, blank=True)

    statusChoices = (
        (0, 'Have not processed'),
        (1, 'Processing'),
        (2, 'Processed'),
    )
    status = models.IntegerField(choices=statusChoices, default=0)

    theProcesser = models.ForeignKey(to=users, related_name='processer', null=True, blank=True)
    solution     = models.TextField(null=True, blank=True)
    ptime        = models.DateTimeField(null=True, blank=True)






