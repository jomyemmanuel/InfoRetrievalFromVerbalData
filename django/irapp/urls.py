from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
import views

urlpatterns = [

	url(r'^$', views.index, name = 'Index'),
	url(r'^register/$', views.register, name = 'Registration'),
	url(r'^login/$', views.login, name = 'Login'),
	url(r'^logout/$', views.logout, name = 'Logout'),
	url(r'^upload/$', views.upload, name = 'Upload'),
	url(r'^dashboard/$', views.dashboard, name = 'Dashboard'),
	url(r'^summaryAPI/$', views.summaryAPI, name='summaryAPI'),
]


if settings.DEBUG:
		urlpatterns += [
			url(r'^media/(?P<path>.*)$', serve, {
				'document_root': settings.MEDIA_ROOT,
				}),
		]