from django.conf.urls import url
from django.views.generic import RedirectView

from . import views



app_name = 'zavrel'
urlpatterns = [
	# url(r'^search.html$', views.search, name='search', kwargs={'page': "search"}),
	# url(r'^def/(?P<permalink>.+)$', views.funpage, name='fun_detail'),
	url(r'^pages/(?P<page>[\w-]+)/$', views.index, name='pages'),
	url(r'^index$', views.index, name='index'),
	url(r'^$', RedirectView.as_view(url='/index'), name="home"),


]
	
