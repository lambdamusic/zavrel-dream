from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

import time
import os

from settings import SITE_ROOT
from .models import *

def index(request, page=""):
	
	q = request.GET.get("q", "")

	t = get_text()

	context = {	'data' : t , 
				'q' : q , 
				}

	return render(request, "zavrel/home.html", context)





def get_text():
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
	
	return data


