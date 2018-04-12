# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from learn.models import User, Advise, Textblog,list_info
from django.shortcuts import redirect
import time, os
from learn import Verification2,qr_code_demo
# from .send_email_demo import sent_mail,rand_code

import json

# Create your views here.
t1 = 0
t2 = 0
Path = '/home/CORPUSERS/xp023799/PycharmProjects/zqxt_tmpl/learn/static/QRcode/'

def about(request):
    if request.session.get('account', None):
        acc_exist = True
        acc_name = request.session['account']
    else:
        acc_exist = False
        acc_name = None
    return render(request, "about.html", {'acc_exist': acc_exist, 'acc_name': acc_name})


def contact(request):
    if request.session.get('account', None):
        acc_exist = True
        acc_name = request.session['account']
    else:
        acc_exist = False
        acc_name = None
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        Advise.objects.create(xname=name, xemail=email, Message=message)

    return render(request, "contact.html", {'acc_exist': acc_exist, 'acc_name': acc_name})


def features(request):
    if request.session.get('account', None):
        acc_exist = True
        acc_name = request.session['account']
    else:
        acc_exist = False
        acc_name = None
    return render(request, "features.html", {'acc_exist': acc_exist, 'acc_name': acc_name})


def work(request):
    if request.session.get('account', None):
        acc_exist = True
        acc_name = request.session['account']
    else:
        acc_exist = False
        acc_name = None
    if request.method == 'POST':
        if request.session.get('account', None):
            username = request.session['account']
            checkpoint = User.objects.filter(username__exact=username,permission__exact=True)
            if checkpoint:
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                message = request.POST['msg']
                Textblog.objects.create(username=username, times=times, message=message)
                blog_list = Textblog.objects.all()
                return render(request, "work.html", {'blog_list': blog_list,'acc_exist': acc_exist, 'acc_name': acc_name})
            else:
                return HttpResponse("This user is disabled by illegal behavior")

        else:
            return redirect('login')
    blog_list = Textblog.objects.all()

    return render(request,"work.html",{'blog_list': blog_list, 'acc_exist': acc_exist, 'acc_name': acc_name})





def login(request):
    error = {}
    filename = Verification2.gene_code(
        '/home/CORPUSERS/xp023799/PycharmProjects/zqxt_tmpl/learn/static/Verfily-code')
    if request.method == 'GET':
        global t1
        t1 = time.time()

    if request.method == 'POST':

        t2 = time.time()

        #print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        account = request.POST['account']
        password = request.POST['password']
        code = request.POST['verifycode']
        code2 = request.POST['filename']

        x = t2 - t1
        if (x < 60):
            if code == code2:
                user = User.objects.filter(username__exact=account, password__exact=password)
                if user:
                    os.unlink('/home/CORPUSERS/xp023799/PycharmProjects/zqxt_tmpl/learn/static/Verfily-code/'+code+'.png')
                    request.session.set_expiry(9999)
                    request.session['account'] = account
                    return redirect('index')
                else:
                    error['msg'] = 'account or password error'
            else:
                error['msg'] = 'Verifycode is error'

        else:
            error['msg'] = 'Verifycode is time over 60 seconds'

    return render(request, "login.html", {'error': error, 'filename': filename,})

def logout(request):
    del request.session['account']
    return render(request,'logout.html')



def jump(request):
    return render(request, 'jump.html')

def Register(request):
    if request.method == 'POST':

        account = request.POST['account']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if User.objects.filter(username=account).exists():
            return HttpResponse("account almost exist")

        if password1 != password2:
            return HttpResponse("Twice password are different")
        else:
            User.objects.create(username=account, password=password1, email=email)

        return render(request, "jump.html")

    return render(request, "register.html")


def index(request):
    if request.session.get('account', None):
        acc_exist = True
        acc_name = request.session['account']
    else:
        acc_exist = False
        acc_name = None
    if request.method == "POST":
        if request.session.get('account', None):
            username = request.session['account']
            checkpoint = User.objects.filter(username__exact=username)
            if checkpoint:
                path = '/home/CORPUSERS/xp023799/PycharmProjects/zqxt_tmpl/learn/static/uploads/'+username+"/"
                if not os.path.exists(path):
                    os.makedirs(path)
                os.chdir(path)
                print(path)
                with open(path + str(request.FILES['file']), 'wb+')as destination:
                    for chunk in request.FILES['file'].chunks():
                        destination.write(chunk)
                return HttpResponse('Successful')
            else:
                return HttpResponse("This user is disabled by illegal behavior")
        else:
            return redirect("login")
    return render(request, 'index.html', {'acc_exist': acc_exist, 'acc_name': acc_name})

def info(request):
    if request.session.get('account', None):
        acc_exist = True
        acc_name = request.session['account']
    else:
        return redirect('index')
    if request.method == 'POST':
        Name   = request.POST['Name']
        Tel    = request.POST['Tel']
        Sex    = request.POST.getlist('sex')
        sex    = Sex[0]
        date   = request.POST['date']
        se_area= request.POST['se_area']
        se_age = request.POST['se_age']
        msg    = request.POST['msg']
        account = User.objects.get(username__exact=acc_name)
        list_info.objects.update_or_create(username=account,name=Name,Tel=Tel,user_sex=sex,DATEBIRTH=date,Area=se_area,age=se_age,per_mess=msg)
        mess = 'OK! You have been successed to saved'
        return render(request, "person_info.html", {'acc_exist': acc_exist, 'acc_name': acc_name,'mess':mess})

    return render(request, "person_info.html", {'acc_exist': acc_exist, 'acc_name': acc_name})



def cdpwd(request):
    if request.session.get('account', None):
        acc_exist = True
        acc_name = request.session['account']
    else:
        return redirect('index')
    if request.method == 'POST':
        if request.session.get('account', None):
            username = request.session['account']
            password = request.POST['password']
            pw1 = request.POST['pw2']
            pw2 = request.POST['pw3']
            if pw1 == pw2:
                checkpoint = User.objects.filter(username__exact=username, password__exact=password)
                if checkpoint:
                    checkpoint.update(password=pw1)
                    return redirect('logout')
            else:
                print("888")
                return render(request, "change_password.html", {'acc_exist': acc_exist, 'acc_name': acc_name})

    return render(request, "change_password.html", {'acc_exist': acc_exist, 'acc_name': acc_name})


def info_confirm(request):
    if request.session.get('account', None):
        acc_exist = True
        acc_name = request.session['account']
        username = acc_name
        user_default = User.objects.get(username__exact=username)
        Name = "???"
        Sex  = "???"
        mail = user_default.email
        Date = "???"
        age  = "???"
        Area = "???"
        Tel  = "???"
        Mess = "???"

        user_m = list_info.objects.filter(username__exact=user_default)
        if user_m:
            user_m =list_info.objects.get(username__exact=user_default)
            Name = user_m.name
            Sex = user_m.user_sex
            mail = user_m.username.email
            Date = user_m.DATEBIRTH
            age = user_m.age
            Area = user_m.Area
            Tel = user_m.Tel
            Mess = user_m.per_mess
        return render(request, "info_confirm.html", {'acc_exist': acc_exist, 'acc_name': acc_name,'Name':Name,'Sex':Sex,
                                                     'mail':mail,'Date':Date,'age':age,"Area":Area,"Tel":Tel,'Mess':Mess,})

    else:
        return redirect('index')





def forget(request):
    if request.method == 'POST':
        account = request.POST['account']
        email   = request.POST['email']
        user = User.objects.filter(username__exact=account, email__exact=email)
        if user:
            x = "666"
            t2 = time.time()
            return render(request,'findback.html',{'account':account,'code':x,'t2':t2})
        else:
            mess ='The information has error,Try again!'



    return render(request,'forget.html',{'mess':mess})

# def findback(request):
#     error = {}
#     account = request.GET['account']
#     if account:
#         pw1  = request.POST['pw1']
#         pw2  = request.POST['pw2']
#         code = request.GET['code']
#         t2   = request.GET['t2']
#         if request.method == 'POST':
#             code2 = request.POST['verifycode']
#             if pw1 == pw2:
#                 if code == code2:
#                     timeout = time.time() - t2
#                     if timeout < 3600:
#                         User.objects.filter(username__exact=account).update(password=pw1)
#                     else:
#
#                         error['mess'] = 'time out!'
#
#                 else:
#                     error['mess'] = 'Verify code error'
#
#             else:
#                 error['mess'] = 'The confirm code are different'
#     return render(request,'findback.html',{'error':error})
def qr_code(request):
    if request.method == 'POST':
        URL = request.POST['URL']
        qr_code_demo.create(URL, Path)

    return render(request,'qr_code_create.html')
