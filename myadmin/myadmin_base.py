class BaseMyAdmin(object):
    def __init__(self):
        self.actions.extend(self.default_actions)

    list_display = []
    list_filter = []
    search_fields = []
    readonly_fields = []#只读字段，前端不能修改
    filter_horizontal = []
    default_actions = ['delete_selected_objs']
    actions = []

    def delete_selected_objs(self, request, querysets):
        print("默认的actions操作")