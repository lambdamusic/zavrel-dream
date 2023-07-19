from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

import time
import os

from settings import SITE_ROOT
from .models import *

def index(request, page=""):
	
	t = get_text()
	allpages_no = len(t)

	try:
		page_no = int(page)
		page = (page_no, t[page_no])
		nextpage_no = page_no + 1
		if nextpage_no > 19:
			nextpage_no = 1
	except:
		page = None
		nextpage_no = None

	print("Page: ", page)

	context = {	
		'alltext' : t , 
		'page' : page,
		'nextpage_no' : nextpage_no, 
		'allpages_no' : allpages_no 
		}

	return render(request, "zavrel/home.html", context)





def get_text(number=None):
	"""Read simple markdown file and spit out a dictionary with the text
		{1 : "...", 2 : "...."} etc..
	"""
	with open(os.path.join(SITE_ROOT, "src", "static", "thetext.md")) as f:
		text = f.readlines()

	data = {}

	n = 0
	for x in text:
		if x != "\n" and x[0] != "#":
			n += 1
			data[n] = x.replace("\n", "")
	
	try:
		return data[number]
	except:
		return data


