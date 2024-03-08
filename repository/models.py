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
    surfix  = models.CharField(max_length=64)

    themeChoices = [
        (0, "skyBlue"),
        (1, "fireRed"),
    ]
    theme   = models.IntegerField(choices=themeChoices)

class reportTroubles(models.Model):
    uid = models.UUIDField(max_length=16)
    title = models.CharField(max_length=32)
    detail = models.CharField(max_length=256)
    reportPerson = models.ForeignKey(to=users)
    dealPerson   = models.ForeignKey(to=users, null=True, blank=True)
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

class articlesDetail(models.Model):
    content = models.CharField(max_length=256)

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

class labels(models.Model):
    labelName = models.CharField(max_length=16)
    owner     = models.ForeignKey(to=blogs)

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
    parentComment = models.ForeignKey(to='self', related_name='parentComment')






