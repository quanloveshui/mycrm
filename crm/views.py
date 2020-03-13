from django.shortcuts import render
from django.contrib.auth.decorators import  login_required
from crm import models
from django import conf
import os,json
from django.utils.timezone import datetime
from django.db.utils import IntegrityError

# Create your views here.

#只有登录后才可以访问页面
@login_required
def dashboard(request):

    return render(request, 'crm/dashboard.html')


def stu_enrollment(request):
    customers = models.Customer.objects.all()
    class_lists = models.ClassList.objects.all()
    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        class_grade_id = request.POST.get("class_grade_id")

        try:
            enrollment_obj = models.Enrollment.objects.create(
                customer_id=customer_id,
                enrolled_class_id=class_grade_id,
                consultant_id=request.user.userprofile.id,
            )
        except IntegrityError as e:  # 已经生成过报名表了
            pass
        enrollment_link = "http://localhost:8000/crm/enrollment/%s/" % enrollment_obj.id
    return render(request, 'crm/stu_enrollment.html', locals())

def sale(request):
    pass
