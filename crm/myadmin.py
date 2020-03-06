from myadmin.sites import site
from myadmin.myadmin_base import BaseMyAdmin
from crm import models


class CustomerAdmin(BaseMyAdmin):
    list_display = ['id','name','source','consult_course','consultant','content','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['source','name']
    readonly_fields = ['status']

class RoleAdmin(BaseMyAdmin):
    list_display = ['name']


site.register(models.Customer,CustomerAdmin)
site.register(models.Role,RoleAdmin)
site.register(models.Menus)
site.register(models.UserProfile)