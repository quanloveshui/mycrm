from myadmin.myadmin_base import BaseMyAdmin

class AdminSite(object):
    def __init__(self):
        self.enabled_admins = {}
        #{'crm':{'model_class':'Customer','admin_class':'CustomerAdmin'}}
        #{'crm': {'customer': <crm.myadmin.CustomerAdmin object at 0x0000000006AC0C50>, 'role': <myadmin.myadmin_base.BaseMyAdmin object at 0x0000000006AC0B00>}}


    def register(self,model_class,admin_class=None):
        """
        注册admin表
        model_class:用户每个app下自定义的myadmin.py中向myadmin 注册时models.py中表名
        admin_class:用户每个app下自定义的myadmin.py中自定义的类名，向myadmin注册时可以传入也可以不传
        app_name:用户每个app的名字,可以通过models.Customer._meta.app_label获取-->crm
        model_name:用户每个app中models.py中定义的每个model名字的小写，可以通过models.Customer._meta.app_label获取 -->  customer
        """

        #print("register",model_class,admin_class)
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        if not admin_class: #为了避免多个model共享同一个BaseMyAdmin内存对象
            admin_class = BaseMyAdmin()
        else:
            admin_class = admin_class()

        admin_class.model = model_class #把model_class赋值给了admin_class

        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class



site = AdminSite()