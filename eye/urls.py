from django.conf.urls import patterns, url
from eye import views

urlpatterns = patterns('',\
	url(r'^$', views.index, name='index'),
	url(r'^clear_pic/$', views.clear_pic, name='clear_pic'),
	url(r'^clear_pd/$', views.clear_pd, name='clear_pd'),
	url(r'^back/$', views.back_to_menu, name='back_to_menu'),
	url(r'^log/$', views.log_index, name='log_index'),
	url(r'^log/add/$', views.log_add, name='log_add'),
	url(r'^domain/$', views.domain_index, name='domain_index'),
	url(r'^domain/add/$', views.domain_add, name='domain_add'),
	url(r'^draw/$', views.draw_index, name='draw_index'),
	url(r'^draw/view/$', views.draw, name='draw'),
	url(r'^draw/(?P<domain_id>\d+)/plot/$', views.draw_plot, name='draw_plot'),
	url(r'^pic/$', views.pic_index, name='pic_index'),
	url(r'^pic/show/$', views.pic_show, name='pic_show'),
	)