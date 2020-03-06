from django.forms import ModelForm


#实现动态生成modelform
def create_dynamic_model_form(admin_class):

    class Meta:
        model = admin_class.model
        fields = "__all__"

    #为动态modelform添加样式
    def __new__(cls, *args, **kwargs):
        #print("__new__", cls, args, kwargs)
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class': 'form-control'})
        return ModelForm.__new__(cls)

    #用type生成类
    #dynamic_form = type("DynamicModelForm" ,(ModelForm,) ,{'Meta' :Meta})
    """
    第一个参数：类名。
    第二个参数：父类集合。用元组表示，指定所创建类继承的多个父类。尽管只有一个父类，也必须使用元组语法（父类+一个逗号）
    第三个参数：字典。字典内容为所创建类绑定的类变量和方法，字典的 key 为类变量或方法名，字典的 value 为普通值时表示类变量；字典的 value 为函数名时则表示方法。
    """
    dynamic_form = type("DynamicModelForm", (ModelForm,), {'Meta': Meta, '__new__': __new__})


    #print('>>>>>>>>>>',dynamic_form) #<class 'django.forms.widgets.DynamicModelForm'>
    return dynamic_form
