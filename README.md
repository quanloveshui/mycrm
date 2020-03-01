django和bootstrap开发crm系统
一、创建工程及应用，使用bootstrap模板实现基本页面
二、完成动态菜单功能。实现不同用户关联不同角色，登录后看见不同菜单
三、自己写app实现django的admin相关功能
    1、创建app：myadmin和student
    2、myadmin实现独立的登录、首页的相关功能（模板及静态文件、登录函数直接拷贝crm中）
    3、实现myadmin自动发现和注册
    4、实现根据list_display中的配置在前端页面显示后端数据
    5、用户未定义list_display时默认显示所有字段数据
    6、实现根据list_filter中的配置完成多条件过滤
    7、实现分页功能
    8、实现按照某列进行排序
    9、完成分页排序筛选组合使用
    10、完成搜索功能
    11、django modelform简单使用，完成编辑页面显示
    12、动态生成modelform，完成不同页面的显示
