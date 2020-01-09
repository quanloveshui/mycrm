from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import  login_required

@login_required
def app_index(request):
    return render(request,'myadmin/app_index.html')


#登录
def acc_login(request):
    error_msg = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        #仅认证
        user = authenticate(username=username, password=password)
        if user:
            #print("passed authencation", user)
            #认证通过后登录
            login(request, user)
            return redirect(request.GET.get('next', '/myadmin'))
        else:
            error_msg = "Wrong username or password!"
    return render(request, 'myadmin/login.html', {'error_msg': error_msg})


#登出
def acc_logout(request):
    logout(request)
    return redirect("/login/")