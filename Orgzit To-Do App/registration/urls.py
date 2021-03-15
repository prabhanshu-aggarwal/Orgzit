from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from registration import views

urlpatterns = [
    url(r'^create/$', views.create, name='create'),
    url(r'^read/$', views.read, name='read'),
    path('', views.ReadTodo.as_view(), name='read-todo'),
    url(r'^update_delete/$', views.update_delete, name='update_delete'),
    url(r'^update_db/$', views.updatedb, name='update_db'),
    url(r'^save/$', views.save, name='save')

]
