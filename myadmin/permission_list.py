from myadmin import permission_hook

perm_dic= {

    #'crm_table_index': ['table_index', 'GET', [], {'source':'qq'}, ],  # 可以查看CRM APP里所有数据库表
    'crm_table_list': ['table_obj_list', 'GET', [], {},permission_hook.view_my_own_customers],  # 可以查看每张表里所有的数据
    'crm_table_list_view': ['table_obj_change', 'GET', [], {}],  # 可以访问表里每条数据的修改页
    'crm_table_list_change': ['table_obj_change', 'POST', [], {}],  # 可以对表里的每条数据进行修改
    'crm_table_obj_add_view': ['table_obj_add', 'GET', [], {}],  # 可以访问数据增加页
    'crm_table_obj_add': ['table_obj_add', 'POST', [], {}],  # 可以创建表里的数据

}

"""
字典里的key是权限名，需要用这些权限名来跟用户进行关联
values里第一个值如'table_index'是django中的url name，在这里必须相对的url name, 而不是绝对url路径，因为考虑到django url正则匹配的问题，搞绝对路径，不好控制。 
values里第2个值是http请求方法
values里第3个[]是要求这个请求中必须带有某些参数，但不限定对数的值是什么
values里的第4个{}是要求这个请求中必须带有某些参数，并且限定所带的参数必须等于特定的值
"""