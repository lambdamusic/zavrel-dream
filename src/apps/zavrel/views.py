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
	is_last = False

	try:
		# single page
		page_no = int(page)
		if allpages_no == page_no:
			is_last = True
		page_data = (page_no, t[page_no])
		nextpage_no = page_no + 1
		if nextpage_no > 19:
			nextpage_no = 1
	except:
		# index page
		page_data = None
		nextpage_no = None

	print("Page: ", page_data)

	context = {	
		'alltext' : t , 
		'page' : page_data,
		'nextpage_no' : nextpage_no, 
		'allpages_no' : allpages_no,
		'is_last' : is_last 
		}

	return render(request, "zavrel/home.html", context)





def get_text(number=None):
	"""Read simple markdown file and spit out a dictionary with the text
		{1 : "...", 2 : "...."} etc..
	"""
	with open(os.path.join(SITE_ROOT, "src", "static", "thetext.md")) as f:
		text = f.readlines()

	data = {}

	#
	# Read source file
	# Newlines are preserved as <br />
	# '#' sign is used to delimit a page 
	#
	linenumber = 0
	buffertext = ""
	for x in text:
		if x == "\n" and not buffertext: 
			# skip first empty line
			continue
		elif x[0] == "#":  
			# new page: save buffer and zero variables
			if linenumber:
				data[linenumber] = buffertext
			linenumber += 1
			buffertext = ""
		else: 
			# load buffer
			buffertext += x.replace("\n", "<br />")
	

	try:
		return data[number]
	except:
		return data


