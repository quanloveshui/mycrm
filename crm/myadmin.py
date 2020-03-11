from myadmin.sites import site
from myadmin.myadmin_base import BaseMyAdmin
from crm import models


class CustomerAdmin(BaseMyAdmin):
    list_display = ['id','name','source','consult_course','consultant','content','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['source','name']
    readonly_fields = ['status']
    filter_horizontal = ['consult_course' ]
    actions = ['change_status', ]

    #用户定义action对应的函数
    def change_status(self, request, querysets):
        print("pyadmin action:", self, request, querysets)
        #批量更新status的值
        #querysets.update(status=0)

class RoleAdmin(BaseMyAdmin):
    list_display = ['name']



site.register(models.Customer,CustomerAdmin)
site.register(models.Role,RoleAdmin)
site.register(models.Menus)
site.register(models.UserProfile)