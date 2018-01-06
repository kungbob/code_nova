from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,'code_nova/index.html')

def connect(request):
    return render(request,'code_nova/connect.html')
