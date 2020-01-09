from django.conf.urls import url,include
from crm import views

urlpatterns = [

    url(r'^$', views.dashboard,name="sales_dashboard"   ),
    url(r'^customer/', views.sale, name="customer"),


]
