def view_my_own_customers(request):
    #用户可以自定义一下权限
    print("running permisionn hook check.....")
    return True
    # if str(request.user.id) == request.GET.get('consultant'):
    #     print("访问自己创建的用户,允许")
    #     return True
    # else:
    #     return False