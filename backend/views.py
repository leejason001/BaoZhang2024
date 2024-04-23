# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

# Create your views here.

def articleManager(request, tabs):
    return render(request, 'backend/backendBase.html', {'tabs': tabs})
