from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import  login_required
from django.views.decorators.csrf import csrf_exempt
from crm import models
from crm import forms
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
            #信息保存到报名表
            enrollment_obj = models.Enrollment.objects.create(
                customer_id=customer_id,
                enrolled_class_id=class_grade_id,
                consultant_id=request.user.userprofile.id,
            )
        except IntegrityError as e:  # 已经生成过报名表了
            enrollment_obj = models.Enrollment.objects.get(customer_id=customer_id,enrolled_class_id=class_grade_id)
            print(enrollment_obj)

        enrollment_link = "http://127.0.0.1:8081/crm/enrollment/%s/" % enrollment_obj.id
    return render(request, 'crm/stu_enrollment.html', locals())



def enrollment(request,enrollment_id):
    """学员在线报名表地址"""
    enrollment_obj = models.Enrollment.objects.get(id=enrollment_id)
    if enrollment_obj.contract_agreed:#已经报过名
        return HttpResponse("报名合同正在审核中....")
    if request.method == "POST":
        #print("enrollment :", request.POST)
        customer_form = forms.CustomerForm(instance=enrollment_obj.customer, data=request.POST)
        if customer_form.is_valid():
            #print(customer_form.cleaned_data)
            customer_form.save()
            enrollment_obj.contract_agreed = True#学员已同意合同条款,更新contract_agreed字段值
            enrollment_obj.contract_signed_date = datetime.now()
            enrollment_obj.save()
            return HttpResponse("您已成功提交报名信息,请等待审核通过")
        #print("form err", customer_form.errors)
    else:
        customer_form = forms.CustomerForm(instance=enrollment_obj.customer)

    # 列出已上传文件
    uploaded_files = []
    enrollment_upload_dir = os.path.join(conf.settings.CRM_FILE_UPLOAD_DIR, enrollment_id)
    if os.path.isdir(enrollment_upload_dir):
        uploaded_files = os.listdir(enrollment_upload_dir)

    return render(request, "crm/enrollment.html", locals())


#文件上传后端处理。前端通dropzone实现文件上传
@csrf_exempt
def enrollment_fileupload(request,enrollment_id):

    #print(request.FILES)
    enrollment_upload_dir = os.path.join(conf.settings.CRM_FILE_UPLOAD_DIR,enrollment_id)
    #print(">>>>>>>>>>",enrollment_upload_dir)
    if not os.path.isdir(enrollment_upload_dir):
        os.mkdir(enrollment_upload_dir)
    file_obj = request.FILES.get('file')
    if len(os.listdir(enrollment_upload_dir))<= 2:
        with open(os.path.join(enrollment_upload_dir,file_obj.name), "wb") as f:
            for chunks in file_obj.chunks():
                f.write(chunks)
    else:
        return HttpResponse(json.dumps({'status':False, 'err_msg':'max upload limit is 2' }))

    #print(conf.settings.CRM_FILE_UPLOAD_DIR)
    return HttpResponse(json.dumps({'status':True,  }))

def sale(request):
    pass
