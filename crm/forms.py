from django.forms import ModelForm
from crm import models


#django modelform简单使用
class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        #fields = ['name','consultant','status']
        fields = "__all__"
