from django.forms import ModelForm


#实现动态生成modelform
def create_dynamic_model_form(admin_class):

    class Meta:
        model = admin_class.model
        fields = "__all__"

    #用type生成类
    dynamic_form = type("DynamicModelForm" ,(ModelForm,) ,{'Meta' :Meta})

    print('>>>>>>>>>>',dynamic_form) #<class 'django.forms.widgets.DynamicModelForm'>
    return dynamic_form
