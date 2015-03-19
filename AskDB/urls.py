from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AskDB.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^customer_info/',include('ask.urls', namespace='ask')),
    url(r'^Atmos_Security_Vulnerability_Dashboard/',include('sec_vul.urls', namespace='sec_vul')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^access_pattern/', include('eye.urls', namespace='eye')),
)
