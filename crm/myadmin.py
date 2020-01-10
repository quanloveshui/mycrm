from myadmin.sites import site
from myadmin.myadmin_base import BaseMyAdmin
from crm import models


class CustomerAdmin(BaseMyAdmin):
    list_display = ['name','source','contact_type','contact','consultant','consult_content','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name']

site.register(models.Customer,CustomerAdmin)
site.register(models.Role)
site.register(models.Menus)
site.register(models.UserProfile)