from django.db import models
from django.contrib import admin
from django.urls import reverse

import datetime
import urllib
# 
import myutils.abstract_models as mymodels


def nice_url_name(s):
	return urllib.parse.quote_plus(s)


# class XTMFundocEntry(mymodels.EnhancedModel):
# 	"""(XTMFundocEntry enhanced model - timestamps and creation fields inherited)"""
	
# 	name = models.CharField(blank=True, max_length=200, verbose_name="name")
# 	url = models.CharField(blank=True, max_length=350, verbose_name="url", help_text="URL to the github page for this function") 
# 	permalink = models.CharField(blank=True, max_length=350, verbose_name="permalink", help_text="Unique name to be used in the for this function")
# 	source = models.TextField(blank=True, verbose_name="implementation")
# 	fungroup = models.CharField(blank=True, max_length=350, verbose_name="group eg by prefix normally")
# 	funtype = models.CharField(blank=True, max_length=350, verbose_name="type eg whether r a macro or scheme function or xtlang")	
# 	is_custom = models.BooleanField(default=False, verbose_name="custom function?",
# 		help_text="Whether this function is a custom one, not from the official Extempore codebase.")	
	
# 	# unused for now
# 	desc = models.TextField(blank=True, verbose_name="desc")
# 	signature = models.CharField(blank=True, max_length=300, verbose_name="signature")
# 	examples = models.TextField(blank=True, verbose_name="examples")
# 	args = models.TextField(blank=True, verbose_name="args")
# 	returns = models.CharField(blank=True, max_length=300, verbose_name="returns")	
# 	related = models.CharField(blank=True, max_length=300, verbose_name="related")
	
# 	class Admin(admin.ModelAdmin):
# 		readonly_fields=('created_at', 'updated_at')
# 		list_display = ('id', 'name', 'is_custom', 'funtype', 'fungroup', 'updated_at')
# 		list_display_links = ('id', 'name',)
# 		search_fields = ['id', 'name', 'desc']
# 		list_filter = ('created_at', 'updated_at', 'created_by', 'editedrecord', 'is_custom', 'review', 'funtype', 'fungroup')
# 		#filter_horizontal = (,) 
# 		#related_search_fields = { 'fieldname': ('searchattr_name',)}
# 		#inlines = (inlineModel1, inlineModel2)
# 		fieldsets = [
# 			('Administration',	
# 				{'fields':	
# 					['editedrecord', 'review', 'internal_notes', ('created_at', 'created_by'), 
# 					  ('updated_at', 'updated_by')
# 					 ],	 
# 				'classes': ['collapse']
# 				}),
# 			('',	
# 				{'fields':	
# 					['name', 'url', 'source', 'is_custom', 'desc', 'fungroup', 'funtype', 'signature', 'examples', 'args', 'returns', 'related'
# 					 ],	 
# 				# 'classes': ['collapse']
# 				}),	
# 			]
# 		#class Media:
# 			#js = ("js/admin_fixes/fix_fields_size.js",)
			
# 		def save_model(self, request, obj, form, change):
# 			"""adds the user information when the rec is saved"""
# 			if getattr(obj, 'created_by', None) is None:
# 				  obj.created_by = request.user
# 			obj.updated_by = request.user
# 			obj.save()	
			

# 	def get_namespace(self):
# 		if self.fungroup:
# 			return self.fungroup
# 		else:
# 			return " top level"

# 	def get_absolute_url(self):        
# 		return reverse('extempore:fun_detail', kwargs={'permalink': self.permalink})

# 	def save(self, *args, **kwargs):
# 		"""Generate a permalink for the entry."""
# 		super(XTMFundocEntry, self).save(*args, **kwargs)
# 		if not self.permalink:
# 			self.permalink = nice_url_name(self.name.replace(":", "-"))
# 			super(XTMFundocEntry, self).save(*args, **kwargs)


# 	@classmethod
# 	def cleanup_permalinks(self, *args, **kwargs):
# 		"""Ensure each permalink is unique.
# 		If two functions have the same name, add a number to the end.
# 		NOTE run this utility after data input is complete.
# 		"""

# 		for each in self.objects.all().order_by('-id'):

# 			test = XTMFundocEntry.objects.filter(permalink=each.permalink).count()

# 			if test > 1:
# 				each.permalink = f"{each.permalink}-{test-1}"
# 				print("DUPLICATE EXISTS FOR FUNCTION", each.name, " => New permalink:", each.permalink)
# 				each.save()


# 	class Meta:
# 		verbose_name_plural="XTM Functions"
# 		verbose_name = "XTM Function"
# 		ordering = ["id"]
		
# 	def __unicode__(self):
# 		return "XTM Function %d" % self.id
	




