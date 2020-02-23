from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import  login_required
from  django import conf
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from myadmin import app_setup
from crm import models
from myadmin.sites import  site


app_setup.myadmin_auto_discover()
"""
django项目启动后会执行app_setup中myadmin_auto_discover函数，此函数实现加载每个app下的myadmin模块时同时会执行myadmin.py中的程序
每个app下的myadmin.py实现向我们自动定义的myadmin中注册model，实现在web页面上显示哪些表哪些表中列
"""
#print("sites.",site.enabled_admins)

@login_required
def app_index(request):

    return render(request,'myadmin/app_index.html',{'site':site})


#返回前端的过滤条件和通过过滤条件查询到的QuerySet集合
def get_filter_result(request,querysets):
    filter_conditions = {}
    for key,val in request.GET.items():
        if key in ('_page', '_o', '_q'):#去掉关键字不作为过滤条件
            continue
        if val:
            filter_conditions[key] =  val


    #print("filter_conditions>>>>>>>>>>",filter_conditions)
    #传入字典过滤数据方式：a=models.Customer.objects.all() a.filter(**{'source': '1', 'status': '0','date__gte': '2020-1-7'})
    return querysets.filter(**filter_conditions),filter_conditions


def get_orderby_result(request,querysets,admin_class):
    """
    排序
    排序后再分页
    """

    current_ordered_column = {}
    orderby_index = request.GET.get('_o')
    if orderby_index:
        orderby_key =  admin_class.list_display[ abs(int(orderby_index)) ]
        current_ordered_column[orderby_key] = orderby_index #current_ordered_column传到前端，为了让前端知道当前排序的列，以及下一次排序是正还是负

        if orderby_index.startswith('-'):
            orderby_key =  '-'+ orderby_key

        return querysets.order_by(orderby_key),current_ordered_column
    else:
        return querysets,current_ordered_column



def table_obj_list(request,app_name,model_name):
    #print("app_name,model_name:", site.enabled_admins[app_name][model_name]) #app_name,model_name: {'customer': <crm.myadmin.CustomerAdmin object at 0x0000000006B20CC0>, 'role': <myadmin.myadmin_base.BaseMyAdmin object at 0x0000000006B20CF8>}
    admin_class = site.enabled_admins[app_name][model_name]#注册时用户自定义的类，未定义时使用默认的BaseAdmin类
    model_obj=admin_class.model#获取model中对应的的表对象--><class 'crm.models.Customer'>
    querysets = admin_class.model.objects.all().order_by("id")#获取表中所有数据对象QuerySet集合 <QuerySet [<Customer: 客户1>, <Customer: 客户2>]>
    #print(querysets)
    querysets, filter_condtions = get_filter_result(request, querysets)
    admin_class.filter_condtions = filter_condtions#前端的过滤条件

    #单列排序
    querysets, sorted_column = get_orderby_result(request, querysets, admin_class)

    #print('request.GET>>>>>>>>>>>',request.GET) #<QueryDict: {'source': [''], 'consultant': [''], 'status': ['0'], 'date__gte': ['']}>
    #实现分页
    paginator = Paginator(querysets, 2)# 每页2条记录
    """
    per_page: 每页显示条目数量 例如上面的2
    count:    数据总个数
    num_pages:总页数
    page_range:总页数的索引范围，如: (1,10),(1,200)
    page:     page对象
    """
    page = request.GET.get('_page')#获取当前页
    try:
        querysets = paginator.page(page)#获取当前页所有的model对象数据 可以循环获取每一个数据的对象 querysets--><class 'django.core.paginator.Page'>
        #print(querysets) #<Page 2 of 3>
    except PageNotAnInteger:
        # 获取的_page不是数字返回第一页
        querysets = paginator.page(1)
    except EmptyPage:
        # 返回最后一页.
        querysets = paginator.page(paginator.num_pages)
    #print('>>>>>>>>>>>>',request.GET) #<QueryDict: {'_page': ['2']}>
    # print("admin class",admin_class.model )

    return render(request, 'myadmin/table_obj_list.html', {'querysets': querysets, 'admin_class': admin_class,'sorted_column':sorted_column})


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