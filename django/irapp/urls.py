from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
import views
urlpatterns = [

<<<<<<< HEAD
	url(r'^upload', views.upload, name = 'upload'),
	# url(r'^home/$', views.home, name = 'home'),
	# url(r'^login/$', views.login, name = 'Login'),
	# url(r'^logout/$', views.logout, name = 'Logout'),
=======
	url(r'^register/$', views.register, name = 'Registration'),
	url(r'^home/$', views.home, name = 'home'),
	url(r'^login/$', views.login, name = 'Login'),
	url(r'^logout/$', views.logout, name = 'Logout'),
	url(r'^upload/$', views.upload, name = 'Upload'),
>>>>>>> jomy
]
if settings.DEBUG:
	urlpatterns += [
	url(r'^media/(?P<path>.*)$', serve, {
		'document_root': settings.MEDIA_ROOT,
		}),
	]