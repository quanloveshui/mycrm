from django.template import Library
from django.utils.safestring import mark_safe
import datetime ,time
register = Library()

#多条件过滤，生成select element
@register.simple_tag
def build_filter_ele(filter_column,admin_class):

    column_obj = admin_class.model._meta.get_field(filter_column)
    print("column obj:",column_obj)
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
        for column_name in admin_class.list_display:

            column_obj = admin_class.model._meta.get_field(column_name) #获取app的model某个表中列的对象  a=models.Customer._meta.get_field('name')-->django.db.models.fields.CharField
            if column_obj.choices: #get_xxx_display  如果是choice字段获取对应的值,否则通过反射直接获取field对应的值
                column_data = getattr(obj,'get_%s_display'% column_name)() #getattr(obj,'get_%s_display'% column_name)()--->'QQ群'
            else:
                column_data = getattr(obj,column_name)#a=models.Customer.objects.all()获取到QuerySet集合后，可以通过反射获取字段对应的值getattr(i,'name')-->i为循环时每一个QuerySet对象

            td_ele = "<td>%s</td>"% column_data
            ele += td_ele
    else:
        # 没定义list_display时显示表名
        td_ele = "<td>%s</td>" % obj #显示__str__方法中定义的返回值

        ele += td_ele

    return mark_safe(ele)


@register.simple_tag
def get_model_name(admin_class):
    """
     获取表名
    """
    return admin_class.model._meta.model_name.upper()


#分页
@register.simple_tag
def render_paginator(querysets,admin_class):
    ele = '''
      <ul class="pagination">
    '''
    for i in querysets.paginator.page_range:
        if abs(querysets.number - i) < 2 :#设置显示3个页码
            active = ''
            if querysets.number == i : #current page
                active = 'active'
            p_ele = '''<li class="%s"><a href="?_page=%s">%s</a></li>'''  % (active,i,i)

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
    print(sorted_column)
    if column in sorted_column:  # 这一列被排序了,
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction = 'top'
        ele = '''<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>''' % arrow_direction
        print(ele)
        return mark_safe(ele)
    return ''
