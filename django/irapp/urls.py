from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
import views

urlpatterns = [

	url(r'^register/$', views.Registration, name = 'Registration'),
	url(r'^login/$', views.login, name = 'login'),
]

if settings.DEBUG:
		urlpatterns += [
			url(r'^media/(?P<path>.*)$', serve, {
				'document_root': settings.MEDIA_ROOT,
				}),
		]