from django.template import Library
from django.utils.safestring import mark_safe
import datetime ,time
register = Library()

#多条件过滤，生成select element
@register.simple_tag
def build_filter_ele(filter_column,admin_class):

    column_obj = admin_class.model._meta.get_field(filter_column)
    #print("column obj:",column_obj)
    try:
        filter_ele = "<select name='%s'>" % filter_column
        for choice in column_obj.get_choices():
            #column_obj.get_choices--->[('', '---------'), (0, '已报名'), (1, '未报名')]
            selected = ''
            if filter_column in admin_class.filter_condtions:#当前字段被过滤了
                # print("filter_column", choice,
                #       type(admin_class.filter_condtions.get(filter_column)),
                #       admin_class.filter_condtions.get(filter_column))
                if str(choice[0]) == admin_class.filter_condtions.get(filter_column):#当前值被选中了
                    selected = 'selected'
                    #print('selected......')

            option = "<option value='%s' %s>%s</option>" % (choice[0],selected,choice[1])
            filter_ele += option
    except AttributeError as e:
        #处理日期
        print("err",e)
        filter_ele = "<select name='%s__gte'>" % filter_column
        if column_obj.get_internal_type() in ('DateField','DateTimeField'):
            time_obj = datetime.datetime.now()
            time_list = [
                ['','------'],
                [time_obj,'Today'],
                [time_obj - datetime.timedelta(7),'七天内'],
                [time_obj.replace(day=1),'本月'],
                [time_obj - datetime.timedelta(90),'三个月内'],
                [time_obj.replace(month=1,day=1),'YearToDay(YTD)'],
                ['','ALL'],
            ]

            for i in time_list:
                selected = ''
                time_to_str = ''if not i[0] else  "%s-%s-%s"%(i[0].year,i[0].month,i[0].day)
                if  "%s__gte"% filter_column in admin_class.filter_condtions:  # 当前字段被过滤了
                    #print('-------------gte')
                    if time_to_str == admin_class.filter_condtions.get("%s__gte"% filter_column):  # 当前值被选中了
                        selected = 'selected'
                option = "<option value='%s' %s>%s</option>" % (time_to_str ,selected,i[1])
                filter_ele += option

    filter_ele += "</select>"
    return mark_safe(filter_ele)

@register.simple_tag
def  build_table_row(obj,admin_class):
    """
    生成一条记录的html element
    显示数据库中数据
    obj 是查询出来的QuerySet集合中每个对象
    """

    ele = ""
    if admin_class.list_display:#定义list_display时按照定义的数据进行显示
        for index,column_name in enumerate(admin_class.list_display):

            column_obj = admin_class.model._meta.get_field(column_name) #获取app的model某个表中列的对象  a=models.Customer._meta.get_field('name')-->django.db.models.fields.CharField
            if column_obj.choices: #get_xxx_display  如果是choice字段获取对应的值,否则通过反射直接获取field对应的值
                column_data = getattr(obj,'get_%s_display'% column_name)() #getattr(obj,'get_%s_display'% column_name)()--->'QQ群'
            else:
                column_data = getattr(obj,column_name)#a=models.Customer.objects.all()获取到QuerySet集合后，可以通过反射获取字段对应的值getattr(i,'name')-->i为循环时每一个QuerySet对象

            td_ele = "<td>%s</td>"% column_data
            #如果是第一列用户点进去可以编辑
            if index == 0:
                td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id, column_data)
            ele += td_ele
    else:
        # 没定义list_display时显示表名
        #td_ele = "<td>%s</td>" % obj #显示__str__方法中定义的返回值
        td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id, obj)

        ele += td_ele

    return mark_safe(ele)


@register.simple_tag
def get_model_name(admin_class):
    """
     获取表名
    """
    return admin_class.model._meta.model_name.upper()




@register.simple_tag
def render_filtered_args(admin_class, render_html=True):
    '''
    拼接筛选的字段
    便于分页过滤排序组合使用
    '''
    if admin_class.filter_condtions:
        ele = ''
        for k, v in admin_class.filter_condtions.items():
             ele += '&%s=%s' % (k, v)
        if render_html:
            return mark_safe(ele)
        else:
            return ele
    else:
        return ''

#分页
@register.simple_tag
def render_paginator(querysets,admin_class,sorted_column):
    ele = '''
      <ul class="pagination">
    '''
    for i in querysets.paginator.page_range:
        if abs(querysets.number - i) < 2 :#设置显示3个页码
            active = ''
            if querysets.number == i : #current page
                active = 'active'

            #分页和排序、过滤组合
            filter_ele = render_filtered_args(admin_class)
            sorted_ele = ''
            if sorted_column:
                sorted_ele = '&_o=%s' % list(sorted_column.values())[0]

            p_ele = '''<li class="%s"><a href="?_page=%s%s%s">%s</a></li>''' % (active, i, filter_ele, sorted_ele, i)

            ele += p_ele



    ele += "</ul>"

    return mark_safe(ele)



#处理排序相关
#处理_o=是正还是负
@register.simple_tag
def get_sorted_column(column,sorted_column,forloop):
    #sorted_column = {'name': '-0'}
    #column当前列
    if column in sorted_column:#这一列被排序了,判断上一次排序是什么顺序,本次取反
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):#上一次是正序，这一次为反序
            this_time_sort_index = last_sort_index.strip('-')
        else:
            this_time_sort_index = '-%s' % last_sort_index
        return this_time_sort_index
    else:
        #直接返回列的索引
        return forloop



#在排序的每一列在图标
@register.simple_tag
def render_sorted_arrow(column,sorted_column):
    #print(sorted_column)
    if column in sorted_column:  # 这一列被排序了,
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction = 'top'
        ele = '''<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>''' % arrow_direction
        #print(ele)
        return mark_safe(ele)
    return ''



@register.simple_tag
def get_current_sorted_column_index(sorted_column):
    return list(sorted_column.values())[0] if sorted_column else ''


@register.simple_tag
def get_obj_field_val(form_obj,field):
    '''
    返回model obj具体字段的值
    field传入的是字符串，可以通过反射获取值
    '''
    #print(">>>>>>>>>>>>>>>>>>>",type(form_obj.instance)) #<class 'crm.models.Customer'>
    #return getattr(form_obj.instance,field)#如果是非choice字段直接通过getattr获取对应的值
    return getattr(form_obj.instance,'get_%s_display'% field)() #如果是choice字段获取对应的值


'''
@register.simple_tag
def get_available_m2m_data(field_name,form_obj,admin_class):
    """返回的是m2m字段关联表的所有数据"""

    #获取字段对象可以通过model的_meta.get_field
    field_obj = admin_class.model._meta.get_field(field_name)  #admin_class.model-><class 'crm.models.Customer'>


    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>",field_obj)
    #通过字段对象获取关联的model对象用related_model  field_obj-><django.db.models.fields.related.ForeignKey: consult_course>  field_obj.related_model->crm.models.Course
    obj_list = set(field_obj.related_model.objects.all())

    #print(">>>>>>>>>>>>>>>>>>>", type(form_obj.instance),form_obj.instance)
    #form_obj.instance为model中的一个对象 如:models.Customer.objects.get(id='11')
    #通过反射获取字段值
    #print('>>>>>>>>>>>>>>>>>>>>',getattr(form_obj.instance ,field_name),'<<<<<<<<<<<<',type(getattr(form_obj.instance ,field_name)))
    selected_data = set(getattr(form_obj.instance ,field_name).all())


    return obj_list -selected_data

@register.simple_tag
def get_selected_m2m_data(field_name,form_obj,admin_class):
    """返回已选的m2m数据"""

    selected_data = getattr(form_obj.instance ,field_name).all()

    return selected_data
'''


@register.simple_tag
def display_all_related_objs(obj):
    """
    显示要被删除对象的所有关联对象
    :param obj:
    :return:
    """
    ele = "<ul>"
    # ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a></li>" %(obj._meta.app_label,
    #                                                                  obj._meta.model_name,
    #                                                                  obj.id,obj)

    for reversed_fk_obj in obj._meta.related_objects:

        related_table_name =  reversed_fk_obj.name
        related_lookup_key = "%s_set" % related_table_name
        related_objs = getattr(obj,related_lookup_key).all() #反向查所有关联的数据
        ele += "<li>%s<ul> "% related_table_name

        if reversed_fk_obj.get_internal_type() == "ManyToManyField":  # 不需要深入查找
            for i in related_objs:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a> 记录里与[%s]相关的的数据将被删除</li>" \
                       % (i._meta.app_label,i._meta.model_name,i.id,i,obj)
        else:
            for i in related_objs:
                #ele += "<li>%s--</li>" %i
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a></li>" %(i._meta.app_label,
                                                                                 i._meta.model_name,
                                                                                 i.id,i)
                ele += display_all_related_objs(i)

        ele += "</ul></li>"

    ele += "</ul>"

    return ele

