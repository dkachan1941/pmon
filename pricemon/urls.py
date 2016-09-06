# from django.conf.urls import patterns, include, url
from django.conf.urls import *
from django.contrib import admin


# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'pricemon.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),

#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^tasks/', include('tasks.urls')),
# )


urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/', include('tasks.urls')),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
