from myadmin.myadmin_base import BaseMyAdmin

class AdminSite(object):
    def __init__(self):
        self.enabled_admins = {}
        #{'crm':{'customer':'CustomerAdmin','role':'RoleAdmin'}}
        #{'crm': {'customer': <crm.myadmin.CustomerAdmin object at 0x0000000006AC0C50>, 'role': <myadmin.myadmin_base.BaseMyAdmin object at 0x0000000006AC0B00>}}


    def register(self,model_class,admin_class=None):
        """
        注册admin表
        model_class:用户每个app下自定义的myadmin.py中向myadmin 注册时models.py中表名
        admin_class:用户每个app下自定义的myadmin.py中自定义的类名，向myadmin注册时可以传入也可以不传,不传入用默认的类
        app_name:用户每个app的名字,可以通过models.Customer._meta.app_label获取-->crm
        model_name:用户每个app中models.py中定义的每个model名字的小写，可以通过models.Customer._meta.app_label获取 -->  customer
        """

        #print("register",model_class,admin_class)
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        # 为了避免多个model共享同一个BaseMyAdmin内存对象
        if not admin_class:
            admin_class = BaseMyAdmin()#用户注册时如果未传入自定义的类，使用默认的类BaseMyAdmin，显示所有字段数据
            field_obj=model_class._meta.fields#获取字段对象
            list_display=[field_obj[i].name for i in range(len(field_obj))] #所有字段名组成列表
            admin_class.list_display=list_display
        else:
            admin_class = admin_class()

        admin_class.model = model_class #把model_class赋值给了admin_class类中的model属性,使程序可以通过admin_class获取model中的表对象（admin_class.model-->crm.models.Customer）

        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class



site = AdminSite()