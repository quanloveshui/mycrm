from django.template import Library
from django.utils.safestring import mark_safe
import datetime ,time
register = Library()


@register.simple_tag
def  build_table_row(obj,admin_class):
    """
    生成一条记录的html element
    显示数据库中数据
    obj 是查询出来的Queryset中每个对象
    """

    ele = ""
    for column_name in admin_class.list_display:

        column_obj = admin_class.model._meta.get_field(column_name) #获取app的model某个表中列的对象  a=models.Customer._meta.get_field('name')-->django.db.models.fields.CharField
        if column_obj.choices: #get_xxx_display  如果是choice字段获取对应的值,否则通过反射直接获取field对应的值
            column_data = getattr(obj,'get_%s_display'% column_name)() #getattr(obj,'get_%s_display'% column_name)()--->'QQ群'
        else:
            column_data = getattr(obj,column_name)

        td_ele = "<td>%s</td>"% column_data
        ele += td_ele

    return mark_safe(ele)
