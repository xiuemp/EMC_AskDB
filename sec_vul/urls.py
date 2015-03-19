from django.conf.urls import patterns, url
from sec_vul import views

urlpatterns = patterns('', \
        url(r'^$', views.console, name='console'),\
        url(r'^overview/$', views.overview, name='overview'),\
        url(r'^back/$', views.back_to_menu, name='back_to_menu'),\
        url(r'^search/$', views.search, name='search'),\
        url(r'^db/$', views.db, name='db'),\
        url(r'^db_sql/$', views.db_sql, name='db_sql'),\
        )

