from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^get_articles/$', views.get_articles, name = 'get_articles'),
	url(r'^get_tasks_mobile/$', views.get_tasks_mobile, name = 'get_tasks_mobile'),
	url(r'^login_mobile/$', views.login_mobile, name = 'login_mobile'),
	url(r'^set_tasks_mobile/$', views.set_tasks_mobile, name = 'set_tasks_mobile'),
	url(r'^run_spider/$', views.run_spider, name = 'run_spider'),	
]
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
