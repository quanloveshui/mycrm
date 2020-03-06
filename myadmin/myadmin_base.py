class BaseMyAdmin(object):
    list_display = []
    list_filter = []
    search_fields = []
    readonly_fields = []#只读字段，前端不能修改