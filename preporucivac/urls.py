from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^(?P<id>[0-9]+)/$', views.details, name='details'),
	url(r'^pretraga/$', views.search, name='search'),
	url(r'^registracija/$', views.register, name='register'),
	url(r'^prijava/$', views.login_view, name='login_view'),
	url(r'^odjava/$', views.logout_view, name='logout_view'),
]
