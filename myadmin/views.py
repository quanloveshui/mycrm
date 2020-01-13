from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import  login_required
from  django import conf
from myadmin import app_setup
from crm import models
from myadmin.sites import  site


app_setup.myadmin_auto_discover()
"""
django项目启动后会执行app_setup中myadmin_auto_discover函数，此函数实现加载每个app下的myadmin模块时同时会执行myadmin.py中的程序
每个app下的myadmin.py实现向我们自动定向的myadmin中注册model，实现在web页面上显示哪些表哪些表中列
"""
#print("sites.",site.enabled_admins)

@login_required
def app_index(request):

    return render(request,'myadmin/app_index.html',{'site':site})


def table_obj_list(request,app_name,model_name):
    #print("app_name,model_name:", site.enabled_admins[app_name][model_name]) #app_name,model_name: {'customer': <crm.myadmin.CustomerAdmin object at 0x0000000006B20CC0>, 'role': <myadmin.myadmin_base.BaseMyAdmin object at 0x0000000006B20CF8>}
    admin_class = site.enabled_admins[app_name][model_name]#注册时用户自定义的类
    model_obj=admin_class.model#获取model中对应的的表对象--><class 'crm.models.Customer'>
    querysets = admin_class.model.objects.all()#获取表中所有数据对象QuerySet集合 <QuerySet [<Customer: 客户1>, <Customer: 客户2>]>
    #print(querysets)

    return render(request, 'myadmin/table_obj_list.html', {'querysets': querysets, 'admin_class': admin_class})


#登录
def acc_login(request):
    error_msg = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        #仅认证
        user = authenticate(username=username, password=password)
        if user:
            #print("passed authencation", user)
            #认证通过后登录
            login(request, user)
            return redirect(request.GET.get('next', '/myadmin'))
        else:
            error_msg = "Wrong username or password!"
    return render(request, 'myadmin/login.html', {'error_msg': error_msg})


#登出
def acc_logout(request):
    logout(request)
    return redirect("/login/")