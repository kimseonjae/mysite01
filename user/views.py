from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from user import models


def joinform(request):
    return render(request, 'user/joinform.html')


def join(request):
    name = request.POST["name"]
    email = request.POST['email']
    password = request.POST['password']
    gender = request.POST['gender']

    models.insert(name, email, password, gender)

    return HttpResponseRedirect('/user/joinsuccess')


def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')

# ==========================================================

def loginform(request):
    return render(request, 'user/loginform.html')


def login(request):
    email = request.POST['email']
    password = request.POST['password']

    result = models.findby_email_and_password(email, password)

    if result is None:
        return HttpResponseRedirect('/user/loginform?result=fail')

    # login 처리
    request.session['authuser'] = result

    return HttpResponseRedirect('/')


def logout(request):
    del request.session['authuser']  # 정보 지우기

    return HttpResponseRedirect('/')


def relogin(request):
    return render(request, 'user/relogin.html')

# =======================================================

def updateform(request):
    # ACCESS Control (접근 제어)
    # if 'authuser' not in request.session:
    #     return HttpResponseRedirect('/user/loginform')

    authuser = request.session.get('authuser')

    if authuser is None:
        return HttpResponseRedirect('/')
    authuser = request.session['authuser']
    result = models.find_by_no(authuser['no'])
    request.session['temp'] = result

    return render(request, 'user/updateform.html')


def update(request):
    del request.session['temp']

    # if request.POST['password'] is not '':
    #     password = request.POST['password']

    authuser = request.session['authuser']
    no = authuser['no']
    name = request.POST['name']
    password = request.POST['password']
    gender = request.POST['gender']

    models.update(name, password, gender, no)

    request.session['authuser']['name'] = name

    return HttpResponseRedirect('/user/updatesuccess')


def updatesuccess(request):
    return render(request, 'user/updatesuccess.html')