from django.conf.urls import patterns, url
from ask import views

urlpatterns = patterns('', \
	url(r'^$', views.console, name='console'),\
	)