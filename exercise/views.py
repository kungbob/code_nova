from django.shortcuts import render
from .models import Exercise
from room.models import Room
from user.models import User
from student.models import Student
from cluster.models import Cluster
from django.shortcuts import redirect
from tool.import_data import import_data,delete_data,cluster_data
from tool.tree import get_empty_version_tree,flatten,translate,get_compare_list

import json
# Create your views here.

def statistics(exercise_id):

    exercise = Exercise.objects.get(pk=exercise_id)

    return render(request,'exercise/exercise.html',{'exercise' : exercise})

def exercise(request,exercise_id):

    if int(exercise_id) == 9999:

        import_data()


        exercises = Exercise.objects.all()
        return render(request,'exercise/list_exercise.html',{'exercises':exercises})
    elif int(exercise_id) == 8888:
        delete_data()
        exercises = Exercise.objects.all()
        return render(request,'exercise/list_exercise.html',{'exercises':exercises})
    elif int(exercise_id) == 7777:
        cluster_data()
        exercises = Exercise.objects.all()
        return render(request,'exercise/list_exercise.html',{'exercises':exercises})

    else:

        exercise = Exercise.objects.get(pk=exercise_id)
        cluster_list = Cluster.objects.filter(exercise=exercise)


        output_cluster_list = []


        for cluster in cluster_list:


            cluster.necessary_skill = json.loads(cluster.necessary_skill)
            cluster.redundant_skill = json.loads(cluster.redundant_skill)
            cluster.character_skill = json.loads(cluster.character_skill)
            cluster.other_skill = json.loads(cluster.other_skill)
        #
        # for cluster in cluster_list:
        #     necessary_skill = json.loads(cluster.necessary_skill)
        #     redundant_skill = json.loads(cluster.redundant_skill)
        #     character_skill = json.loads(cluster.character_skill)
        #     other_skill = json.loads(cluster.other_skill)
        #     output_cluster_list.append({"necessary_skill":necessary_skill,"redundant_skill":redundant_skill,"character_skill":character_skill,"other_skill":other_skill})
        #
        # for cluster in output_cluster_list:
        #
        #     for skill in cluster["necessary_skill"]:
        #         skill = translate(skill)
        #     for skill in cluster["redundant_skill"]:
        #         skill = translate(skill)
        #     for skill in cluster["character_skill"]:
        # #         skill = translate(skill)
        #
        # print(output_cluster_list)

        #
		# for skill in necessary_skill_list:
		# 	if flatten_tree[skill] == 0 and skill in compare_list:
		# 		lacking.append(translate(skill))
        #
		# for skill in redundant_skill_list:
		# 	if flatten_tree[skill] > 0 and skill in compare_list:
		# 		redundance.append(translate(skill))
        #
		# for skill in character_skill_list:
		# 	if skill in compare_list:
		# 		character.append(translate(skill))
        #
		# for skill in other_skill_list:
		# 	if flatten_tree[skill["name"]] != skill["mode"]:
		# 		others.append({"name": translate(skill["name"]), "current": flatten_tree[skill["name"]], "suggestion": skill["mode"]})





        return render(request,'exercise/exercise.html',{'exercise' : exercise,'cluster_list': cluster_list})

def list_exercise(request):
    exercises = Exercise.objects.all()
    compare_list = get_compare_list()

    translated_version_tree = []
    for skill in compare_list:
        translated_version_tree.append({"skill":skill,"name":translate(skill)})


    print(str(translated_version_tree))
    return render(request,'exercise/list_exercise.html',{'exercises':exercises,'translated_version_tree':translated_version_tree})

def start_exercise(request,exercise_id):

    try:
        pass
    except Exception as e:
        raise


    if request.user.is_authenticated :

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

    else:
        return redirect('register')


    # return render(request,'exercise/start_exercise.html',{'room':room})



    # return render(request,'exercise/start_exercise.html',{'room':room})
