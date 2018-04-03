# from exercise.models import Exercise
import numpy as np # linear algebra
import pandas as pd
import os
from code_nova.settings import BASE_DIR
from room.models import Room
from student.models import Student
from tool.compile_code import compile_code
from tool.analyser import analyser
from version.models import Version
from tool.tree import flatten,flatten_self_define
from tool.clustering import clustering
from cluster.models import Cluster
from exercise.models import Exercise
import json


student_id = 8;
student = Student.objects.get(pk=student_id)

def import_data():
    # hard code room id and student id
    # room_id = 21;
    # student_id = 8;

    # room = Room.objects.get(pk=room_id)
    # student = Student.objects.get(pk=student_id)



    path = os.path.join(BASE_DIR,'tool\program_code_python_only.csv')
    df2 = pd.read_csv(path)

    room_list = dict()

    print(list(df2.QCode.unique()))

    for question_code in list(df2.QCode.unique()):
        exercise = Exercise()
        exercise.title = question_code

        exercise.save()

        room = Room()
        room.owner = student
        room.exercise = exercise
        room.save()

        room_list[question_code] = room



    for index, row in df2.iterrows():
        # print(row)
        # Problem_name = row.QCode
        # UserID = row.UserID
        # Solution_text = row.Solutions
        exercise = Exercise.objects.get(title=row.QCode)

        version = Version()
        version.room = room_list[row.QCode]
        version.exercise = exercise
        version.code = row.Solutions
        # version.result = compile_code(row.Solutions)
        version.version_tree = json.dumps(analyser(row.Solutions))
        version.overall_success = True
        version.save()
        #
        # print(Problem_name, UserID, Solution_text)

def cluster_data():


    path = os.path.join(BASE_DIR,'tool\program_code_python_only.csv')
    df2 = pd.read_csv(path)

    # print(list(df2.QCode.unique()))

    for question_code in list(df2.QCode.unique()):


        exercise = Exercise.objects.get(title=question_code)

        data_matrix = []
        version_list = Version.objects.filter(exercise=exercise)

        if len(version_list) >= 50 :
            for version in version_list:

                flatten_json = flatten_self_define(json.loads(version.version_tree))
                flatten_list = list(flatten_json.values())


                data_matrix.append(flatten_list)

            # remove all old clusters

            Cluster.objects.filter(exercise=exercise).delete()

            print("doing" + str(exercise))
            cluster_result = clustering(data_matrix)


            cluster_list = cluster_result["cluster_list"]
            label = cluster_result["label"]
            common_skill = cluster_result["common_skill"]

            cluster_object_list = []


            # create new cluster
            for cluster in cluster_list:
                new_cluster = Cluster()
                new_cluster.exercise = exercise
                # print(cluster["necessary_skill"])
                new_cluster.necessary_skill = json.dumps(cluster["necessary_skill"])
                new_cluster.redundant_skill = json.dumps(cluster["redundant_skill"])
                new_cluster.center = ','.join(map(str, cluster["center"].tolist()))
                new_cluster.data_count = cluster["data_count"]
                new_cluster.character_skill = json.dumps(cluster["character_skill"])
                new_cluster.other_skill = json.dumps(cluster["other_skill"])
                new_cluster.save()
                cluster_object_list.append(new_cluster)

            for i in range(0,len(label)):
                cluster = cluster_object_list[label[i]]
                version_list[i].cluster = cluster
                version_list[i].save()


            exercise.common_skill = json.dumps(common_skill)
            exercise.save()


def delete_data():
    # room_id = 21;
    # remove all version

    path = os.path.join(BASE_DIR,'tool\program_code_python_only.csv')
    df2 = pd.read_csv(path)


    print(list(df2.QCode.unique()))

    for question_code in list(df2.QCode.unique()):
        Exercise.objects.filter(title=question_code).delete()
