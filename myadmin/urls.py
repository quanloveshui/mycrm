from django.conf.urls import url,include
from django.contrib import admin
from myadmin import views


urlpatterns = [
    url(r'^login/',views.acc_login ),
    url(r'^logout/',views.acc_logout,name="logout" ),
    url(r'^$', views.app_index, name="app_index"),

]