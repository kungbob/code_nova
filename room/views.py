
from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
#
# from .forms import LoginForm, RegisterForm

from django.contrib.auth.decorators import login_required
from user.models import User
from room.models import Room
from student.models import Student
# Create your views here.

@login_required
def accept_help_request(request,room_id):

    room = Room.objects.get(pk=room_id)
    student = Student.objects.get(user=request.user)

    # add the user to room participant and author
    room.particpant.add(student)
    room.author.add(student)

    room.save()

    return redirect("room",room_id=room_id)

@login_required
def room(request,room_id):

    room = Room.objects.get(pk=room_id)

    return render(request,'room/room.html',{'room' : room})

@login_required
def list_room(request):
    rooms = Room.objects.all()
    return render(request,'room/list_room.html',{'rooms':rooms})
