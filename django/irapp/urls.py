from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from .views import upload
urlpatterns = [
url(r'^upload/$', views.upload, name = 'upload'),
]

if settings.DEBUG:
	urlpatterns += [
	url(r'^media/(?P<path>.*)$', serve, {
		'document_root': settings.MEDIA_ROOT,
		}),
	]