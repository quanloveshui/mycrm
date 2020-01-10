from  django import conf


"""
循环每个app
在app的目录中查询myadmin.py
如果有导入
"""
def myadmin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        # mod = importlib.import_module(app_name, 'kingadmin')
        try:
            """
           动态加载模块： __import__ (name） 其中name是被加载 module的名称。name可以是字符串
           加载每个app下的myadmin时同时会执行myadmin.py中的程序，会向自定义的myadmin中注册app中对应的model
           """
            mod = __import__('%s.myadmin' % app_name)
            #print(mod.myadmin)
        except ImportError :
            pass