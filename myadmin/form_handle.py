from django.forms import ModelForm


#实现动态生成modelform
def create_dynamic_model_form(admin_class):

    class Meta:
        model = admin_class.model
        fields = "__all__"

    #为动态modelform添加样式
    def __new__(cls, *args, **kwargs):
        print("__new__", cls, args, kwargs)
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class': 'form-control'})
        return ModelForm.__new__(cls)

    #用type生成类
    #dynamic_form = type("DynamicModelForm" ,(ModelForm,) ,{'Meta' :Meta})
    dynamic_form = type("DynamicModelForm", (ModelForm,), {'Meta': Meta, '__new__': __new__})




    print('>>>>>>>>>>',dynamic_form) #<class 'django.forms.widgets.DynamicModelForm'>
    return dynamic_form
