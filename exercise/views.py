from django.shortcuts import render
from .models import Exercise
from room.models import Room
from user.models import User
from student.models import Student
from cluster.models import Cluster
from django.shortcuts import redirect
# Create your views here.

def statistics(exercise_id):

    exercise = Exercise.objects.get(pk=exercise_id)

    return render(request,'exercise/exercise.html',{'exercise' : exercise})

def exercise(request,exercise_id):

    exercise = Exercise.objects.get(pk=exercise_id)

    cluster_list = Cluster.objects.filter(exercise=exercise)

    return render(request,'exercise/exercise.html',{'exercise' : exercise,'cluster_list': cluster_list})

def list_exercise(request):
    exercises = Exercise.objects.all()
    return render(request,'exercise/list_exercise.html',{'exercises':exercises})

def start_exercise(request,exercise_id):

    try:
        pass
    except Exception as e:
        raise

    room = Room()
    room.exercise = Exercise.objects.get(pk=exercise_id)
    owner = Student.objects.get(user=request.user)
    room.owner = owner
    room.code = room.exercise.template
    room.save()

    room.particpant.add(owner)
    room.author.add(owner)
    room.save()

    return redirect('room',room_id=room.id)

    # return render(request,'exercise/start_exercise.html',{'room':room})



    # return render(request,'exercise/start_exercise.html',{'room':room})
