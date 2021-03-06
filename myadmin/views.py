from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import  login_required
from  django import conf
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from myadmin import app_setup
from crm import models
from myadmin.sites import  site
from django.db.models import Q
from myadmin import form_handle
import json
from myadmin import permissions

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
        if key in ('_page', '_o', '_q' ):#去掉关键字不作为过滤条件
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


#搜索
def get_serached_result(request,querysets,admin_class):
    search_key = request.GET.get('_q')
    if search_key :
        q = Q()
        q.connector = 'OR'
        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains" % search_field, search_key))

        return  querysets.filter(q)
    return querysets

@permissions.check_permission
@login_required
def table_obj_list(request,app_name,model_name):
    #print("app_name,model_name:", site.enabled_admins[app_name][model_name]) #app_name,model_name: {'customer': <crm.myadmin.CustomerAdmin object at 0x0000000006B20CC0>, 'role': <myadmin.myadmin_base.BaseMyAdmin object at 0x0000000006B20CF8>}
    admin_class = site.enabled_admins[app_name][model_name]#注册时用户自定义的类，未定义时使用默认的BaseAdmin类
    model_obj=admin_class.model#获取model中对应的的表对象--><class 'crm.models.Customer'>
    #print(">>>>>>>",admin_class.actions)
    #if里执行用户定义的action
    if request.method == "POST":
        """"
        #print(request.POST)#<QueryDict: {'csrfmiddlewaretoken': ['F7K3yUHgYcevecTMnRhD1dgoZI87fRAwtLezgPvaKUw55Kge7g5oR6N2JgfaZPJ9'], 'action': ['change_status'], 'selected_ids': ['["11","10","9"]']}>
        selected_action = request.POST.get('action')
        selected_ids = json.loads(request.POST.get('selected_ids'))
        #print(selected_action, selected_ids)
        #获取对象
        selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
        #print(selected_objs)#<QuerySet [<Customer: 客户1234>, <Customer: 客户234567jj>]>
        #获取用户定义action对应的函数对象
        admin_action_func = getattr(admin_class, selected_action)
        #print(admin_action_func)#<bound method CustomerAdmin.change_status of <crm.myadmin.CustomerAdmin object at 0x0000000006B28320>>
        #执行用户定义action对应的函数
        admin_action_func(request, selected_objs)
        """
        #print(request.POST)
        selected_action = request.POST.get('action')
        selected_ids = json.loads(request.POST.get('selected_ids'))
        print(selected_action, selected_ids)
        if not selected_action:  # 如果有action参数,代表这是一个正常的action,如果没有,代表可能是一个删除动作
            if selected_ids:  # 这些选中的数据都要被删除
                admin_class.model.objects.filter(id__in=selected_ids).delete()
        else:  # 走action流程
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
            admin_action_func = getattr(admin_class, selected_action)
            response = admin_action_func(request, selected_objs)
            if response:
                return response

    querysets = admin_class.model.objects.all().order_by("-id")#获取表中所有数据对象QuerySet集合 <QuerySet [<Customer: 客户1>, <Customer: 客户2>]>
    #print(querysets)
    querysets, filter_condtions = get_filter_result(request, querysets)
    admin_class.filter_condtions = filter_condtions#前端的过滤条件

    #searched queryset result
    querysets = get_serached_result(request,querysets,admin_class)
    admin_class.search_key = request.GET.get('_q','')

    #单列排序
    querysets, sorted_column = get_orderby_result(request, querysets, admin_class)

    #print('request.GET>>>>>>>>>>>',request.GET) #<QueryDict: {'source': [''], 'consultant': [''], 'status': ['0'], 'date__gte': ['']}>
    #实现分页
    paginator = Paginator(querysets,3 )# 每页2条记录
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

    #return render(request, 'myadmin/table_obj_list.html', {'querysets': querysets, 'admin_class': admin_class,'sorted_column':sorted_column})
    return render(request, 'myadmin/table_obj_list.html',locals())





#编辑信息
@permissions.check_permission
@login_required
def table_obj_change(request,app_name,model_name,obj_id):
    """
    #django modelform简单使用
    from crm.forms import CustomerForm
    form_obj = CustomerForm()
    """
    """
    动态生成modelform 使用tpye生成类
    """
    admin_class = site.enabled_admins[app_name][model_name]
    #print(">>>>>>>>>>>>>>",admin_class.model)
    #执行函数form_handle.create_dynamic_model_form返回一个类  dynamic_form-><class 'django.forms.widgets.DynamicModelForm'>
    model_form = form_handle.create_dynamic_model_form(admin_class)
    # 类实例化
    #form_obj = model_form()
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "GET":
        # 把要修改的对象通过 instance 传入form组件中   必须为本类的对象
        form_obj = model_form(instance=obj)

        #print(">>>>",list(form_obj)[0]) #<input type="text" name="name" value="客户2" maxlength="32" class="form-control" id="id_name">
    elif request.method == "POST":
        # 有instance代表是更新数据
        # 如果 instance 有对象则是修改数据 没有就是 新增数据
        form_obj = model_form(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/myadmin/%s/%s/" % (app_name, model_name))


    return render(request, 'myadmin/table_obj_change.html',locals())

#添加数据
def table_obj_add(request,app_name,model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class,form_add=True)
    if request.method == "GET":
        form_obj = model_form()
    elif request.method == "POST":
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/myadmin/%s/%s/" % (app_name, model_name))

    return render(request,'myadmin/table_obj_add.html',locals())


#删除数据
@login_required
def table_obj_delete(request,app_name,model_name,obj_id):
    admin_class = site.enabled_admins[app_name][model_name]

    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "POST":
        obj.delete()
        return redirect("/myadmin/{app_name}/{model_name}/".format(app_name=app_name,model_name=model_name))
    return render(request,'myadmin/table_obj_delete.html',locals())

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