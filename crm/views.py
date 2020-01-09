from django.shortcuts import render
from django.contrib.auth.decorators import  login_required

# Create your views here.

#只有登录后才可以访问页面
@login_required
def dashboard(request):

    return render(request, 'crm/dashboard.html')



def sale(request):
    pass
