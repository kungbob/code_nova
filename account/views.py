from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from user.models import User
from tool.tree import translate_tree
from student.models import Student
import json
# Create your views here.

def login(request):

    # if already login, no need to login
    if request.user.is_authenticated():
        return redirect('index')

    # POST method
    if request.POST:
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']

            # since already checked in form, no need for further checking
            user = auth.authenticate(email=email, password=password)
            auth.login(request,user)

            return redirect('index')

    # GET method
    else:
        login_form = LoginForm()

    return render(request,'account/login.html',{"login_form":login_form})

def register(request):

    if request.POST:
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            my_email = register_form.cleaned_data['email']
            my_password = register_form.cleaned_data['password']
            my_acc_type = register_form.cleaned_data['acc_type']

            # since already checked in form, no need for further checking
            # user = auth.authenticate(email=email, password=password)
            # auth.login(request,user)

            user = User(email=my_email,acc_type=my_acc_type )
            user.set_password(my_password)
            user.save()

            return redirect('register_success')

    # GET method
    else:
        register_form = RegisterForm()

    return render(request,'account/register.html',{"register_form":register_form})

def register_success(request):
    return render(request,'account/register_success.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def myprofile(request):
    student = Student.objects.get(user=request.user)

    # translated_tree = translate_tree(json.loads(student.profile_tree))
    # print(str(translated_tree))

    return render(request,'account/profile.html',{"student":student})
