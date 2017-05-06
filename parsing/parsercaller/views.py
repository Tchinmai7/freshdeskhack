# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from freshdeskhack import pdf_parse
# Create your views here.

def parsefunc(request):
	path = request.GET.get('path','')
	response = pdf_parse.parsePDF(path)
	return HttpResponse(response)
