from django.conf.urls import url,include
from crm import views

urlpatterns = [

    url(r'^$', views.dashboard,name="sales_dashboard"   ),
    url(r'^customer/', views.sale, name="customer"),
    url(r'^stu_enrollment/$', views.stu_enrollment,name="stu_enrollment"   ),#课程顾问填写信息生成报名连接
    url(r'^enrollment/(\d+)/$', views.enrollment,name="enrollment"   ),#学员填写信息
    url(r'^enrollment/(\d+)/fileupload/$', views.enrollment_fileupload,name="enrollment_fileupload"   ),#学员上传证件
    url(r'^stu_enrollment/(\d+)/contract_audit/$', views.contract_audit, name="contract_audit"),#课程顾问审核合同


]
