from django.forms import ModelForm
from crm import models
from django import forms

#django modelform简单使用
class CustomerForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        #print("__new__", cls, args, kwargs)
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class': 'form-control'}) #给前端html添加样式属性

            if field_name in cls.Meta.readonly_fields:
                filed_obj.widget.attrs.update({'disabled': 'true'})
                # print("--new meta:",cls.Meta)

        # print(cls.Meta.exclude)
        return ModelForm.__new__(cls)

    class Meta:
        model = models.Customer
        #fields = ['name','consultant','status']
        fields = "__all__"
        exclude = ['consult_content', 'status', 'consult_courses']
        readonly_fields = [ 'consultant', 'referral_from', 'source']

    #clean方法中定义自己想要实现功能，禁止用户通过前端修改只读字段数据
    def clean(self):
        '''form defautl clean method'''

        #print("cleaned_dtat:", self.cleaned_data)

        if self.errors:
            raise forms.ValidationError(("Please fix errors before re-submit."))
        if self.instance.id is not None:  # means this is a change form ,should check the readonly fields
            for field in self.Meta.readonly_fields:
                old_field_val = getattr(self.instance, field)  # 数据库里的数据
                form_val = self.cleaned_data.get(field) #前端提交过来数据
                print("filed differ compare:", old_field_val, form_val)
                if old_field_val != form_val:
                    self.add_error(field, "Readonly Field: field should be '{value}' ,not '{new_value}' ". \
                                   format(**{'value': old_field_val, 'new_value': form_val}))