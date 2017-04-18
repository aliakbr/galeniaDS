from django.conf.urls import url
from . import views

app_name = 'galeniads'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/(?P<id>[0-9]+)/$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^account_manager/$', views.account_manager, name='account_manager'),
    url(r'^home/(?P<id>[0-9]+)/(?P<pk>[0-9]+)/view/$', views.view_file_in_folder, name="view_file_in_folder"),
    url(r'^home/(?P<id>[0-9]+)/(?P<pk>[0-9]+)/add/$', views.add_file, name="add_file"),
    url(r'^home/(?P<id>[0-9]+)/(?P<pk>[0-9]+)/edit/$', views.edit_folder, name="edit_folder"),
    url(r'^home/(?P<id>[0-9]+)/add/$', views.add_folder, name="add_folder"),
    url(r'^home/(?P<id>[0-9]+)/(?P<pk>[0-9]+)/recap/$', views.recap_file, name="recap_file"),
    url(r'^home/(?P<id>[0-9]+)/(?P<pk>[0-9]+)/(?P<file_id>[0-9]+)/download/$', views.download_file, name="download_file"),
]
