#!/usr/bin/env python

"""
Helper for extracting metadata from Extempore source code. 
Returns a structure consisting of a list of metadata dictionaries (one per function)

2021-01-22: updated to py3 and latest app
2016-03-07: changes for working against 'HEAD'
2016-01-26: this is a duplicate of /code/zavrel/xtm-utils-public/etc..
"""


import os, sys
import click

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter



VALID_TYPES = ["define", "define-macro", "bind-func", "impc:aot:do-or-emit", "macro"]


##
### main functions
##



def walk_xtm_files(_DIRS, exclude_patterns=[], githubUrl=None):
	"""
	recursive src files browser & extractor

	exclude_patterns
		<aot-cache> : skipped by default (compiled stuff)
	"""

	index = []
	exclude_patterns += ["aot-cache"]


	def do_exclude(root):
		for pattern in exclude_patterns:
			if pattern in root:
				click.secho("skipping: " + root, fg="red")
				return True
		return False

	for path in _DIRS:

		click.secho("********\nProcessing:\n" + _DIRS[0] + "\n********", fg="green")

		for root, dirs, files in os.walk(path):
			for file in files:
				fullpath = root + "/" + file
				if file.endswith(".xtm"):
					if not do_exclude(fullpath):
						print("Parsing:", fullpath)
						index += _parse_onefile(fullpath, path, githubUrl=githubUrl)


	index = sorted(index, key=lambda x: x['name'])
	return index





def _parse_onefile(f, original_path, IGNORE_CONSTANTS=True, IGNORE_SYMBOLS=True, githubUrl=None, verbose=False):
	"""Extract definitions from a single Extempore file.

	Assume that valid functions definitions are separated by a blank line (at least). 
	The function keywords accepted are defined at the top of this file.

	Iterate through a list of lines, and for each line check if it starts with one of the function keywords.
	If it does, extract the function name and function-type and keep it in a buffer. 
	The line is added to another buffer and keep adding lines till the next blank line or function start keyword.

	Returns a list of dicts, one per function.
	If the function comments are present right after/before the function definition, they are picked up automatically.

	NOTE Special case with 'wrapped' functions eg:

	(impc:aot:do-or-emit
		(define-macro (steps . args)
					`(helper:mmplayp_f_with_offset beat dur *mididevice* ,@args))
			)


	Parameters
	----------
	f : string
		Filepath for the file to be parsed.
	
	Returns
	----------
	List of dicts

	"""
	output = []
	lines = open(f).read().splitlines()

	linebuffer = "" # all lines for the current function
	typebuffer = None # type of the current function
	titlebuffer = None # name of the current function


	def save_definition(linebuffer, titlebuffer, typebuffer):
		if verbose: click.secho("--saving--", fg="red")
		# linebuffer_text = "".join([x for xin linebuffer])
		return genDict(linebuffer, titlebuffer, f, original_path, typebuffer, githubUrl)

	for i in range(len(lines)):
		
		line = lines[i]
		if verbose: click.secho(line, dim=True)
		if verbose: click.secho(len(line), dim=True)

		if not line.strip(): 

			# = blank line delimiter
			if verbose: click.secho("--empty line--", fg="green")
			if titlebuffer and linebuffer: 
				output += save_definition(linebuffer, titlebuffer, typebuffer)

			# empty buffers
			linebuffer, titlebuffer, typebuffer = "", None, None

		else:


			if isValidType(line): # check if we have a function keyword 

				if verbose: click.secho(line, fg="green")

				if titlebuffer and linebuffer: 
					output += save_definition(linebuffer, titlebuffer, typebuffer)
					linebuffer, titlebuffer, typebuffer = "", None, None

				linebuffer += "\n" + line
				# if linebuffer: # if a buffer is already open, save it
				# 	output += genDict(linebuffer, titlebuffer, f, original_path, typebuffer, githubUrl)
				# 	linebuffer, titlebuffer, typebuffer = [], None, None

				lline = line.split()

				titlebuffer = _getTitle(lline) or "no title"
				typebuffer = _getType(lline)
				# linebuffer += "\n" + line

				if IGNORE_CONSTANTS and titlebuffer.startswith("*"):
					typebuffer = None
					titlebuffer = None
					linebuffer = ""

				if "impc:aot:do-or-emit" in line and titlebuffer == "no title":
					# check following line for title 
					line_next = lines[i+1]
					lline_next = line_next.split()
					titlebuffer = _getTitle(lline_next) or "no title"
					typebuffer = _getType(lline_next)
				
			else:

				linebuffer += "\n" + line

				# if titlebuffer: # if we have a title buffer, add the line to it
				# 	if not line[0] == "(":
				# 		linebuffer += "\n" + line
				#NOTE: the logic 'if not line[0] == "("' is a very weak way to determine 
				# two function definitions without empty line
				# in such a case we just skip it - assuming the good coding convention
				# this refers to cases like {bind-val etc...}
				# TODO - improve this


	return output








# ;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;; UTILS ;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;


def isValidType(s):
	"helper"
	for v in VALID_TYPES:
		if s.startswith("(" + v):
			return True
	return False

def _remove_parenthesis(s):
	s = s.replace("(", "")
	s = s.replace(")", "")
	return s

def _saveSpaces(line):
	return line.replace(" ", "&nbsp;")


def _getTitle(line_splitted):
	"""extract the name from a function definition - takes a list of strings"""
	s = ""
	if len(line_splitted) > 1: 
		s = line_splitted[1]
		s = _remove_parenthesis(s)

		if "[" and "]" in s:
			s = s.split(":")[0] # eg (bind-func qbuf_push:[void,QBuffer*,!a]*

	return s

def _getType(line_splitted):
	"""classify the type of a function definition - takes a list of strings"""
	s = line_splitted[0]
	s = _remove_parenthesis(s.strip())

	if "define-macro" in s or "macro" in s:
		return "macro"
	elif "define" in s:
		return "scheme"
	elif "bind-func" in s:
		return "xtlang"
	else:
		return "unknown"

def inferGroup(titlebuffer):
	"""infers the function prefix"""
	if titlebuffer:
		if titlebuffer[0] == "*":
			return "*var*"
		if titlebuffer[0] in ["-", "_"]:  #["*", "-", "_"]
			#strip first letter
			titlebuffer = titlebuffer[1:]

		if titlebuffer.startswith("glfw"):
			return "glfw:"

		idx = titlebuffer.rfind(":")
		# print(idx, titlebuffer[:idx+1])
		if idx >= 0:
			return titlebuffer[:idx+1]
	return "" # default


def genDict(linebuffer, titlebuffer, f, original_path, typebuffer, githubUrl):
	"""Puts the function info into a dict
	Also add pygments and hardcode github url info
	"""
	lexer = get_lexer_by_name("scheme", stripall=True)
	result = highlight(linebuffer, lexer, HtmlFormatter())
	url = f.replace(original_path, githubUrl)
	return [{'name' : titlebuffer,
			# 'code' : _saveSpaces(linebuffer),
			'codepygments' : result,
			'file' : f,
			'functiontype' : typebuffer,
			'url' : url,
			'group' : inferGroup(titlebuffer) }]











