from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='list'),
    url(r'^list/$', views.list_images, name='list_images'),
    url(r'^view/$', views.view_image, name='view_image'),
    url(r'^admin/', include(admin.site.urls)),
)
