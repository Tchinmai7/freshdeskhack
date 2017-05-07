# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from freshdeskhack import pdf_parse
# Create your views here.

def parsefunc(request):
    path = request.GET.get('path','')
    message_id = request.GET.get('message_id','')
    directory = "/Users/schinmai/Downloads/" + path
    response = pdf_parse.parsePDF(directory,message_id)
    print JsonResponse(response)
    return JsonResponse(response)
