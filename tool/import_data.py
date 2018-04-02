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
from tool.tree import flatten
from tool.clustering import run_kmeans
from cluster.models import Cluster
import json


room_id = 21;
student_id = 8;
room = Room.objects.get(pk=room_id)
student = Student.objects.get(pk=student_id)

def import_data():
    # hard code room id and student id
    # room_id = 21;
    # student_id = 8;

    # room = Room.objects.get(pk=room_id)
    # student = Student.objects.get(pk=student_id)



    path = os.path.join(BASE_DIR,'tool\program_code_python_only.csv')
    df2 = pd.read_csv(path)

    for index, row in df2.iterrows():
        # print(row)
        # Problem_name = row.QCode
        # UserID = row.UserID
        # Solution_text = row.Solutions


        version = Version()
        version.room = room
        version.exercise = room.exercise
        version.code = row.Solutions
        # version.result = compile_code(row.Solutions)
        version.version_tree = json.dumps(analyser(row.Solutions))
        version.overall_success = True
        version.save()
        #
        # print(Problem_name, UserID, Solution_text)

def cluster_data():

    data_matrix = []
    version_list = Version.objects.filter(room=room)

    if len(version_list) >= 10 :
        for version in version_list:

            flatten_json = flatten(json.loads(version.version_tree))
            flatten_list = list(flatten_json.values())


            data_matrix.append(flatten_list)

        # remove all old clusters

        Cluster.objects.filter(exercise=room.exercise).delete()

        cluster_result = run_kmeans(data_matrix)

        print(cluster_result)


        cluster_list = cluster_result["cluster_list"]
        label = cluster_result["label"]
        common_skill = cluster_result["common_skill"]

        cluster_object_list = []


        # create new cluster
        for cluster in cluster_list:
            new_cluster = Cluster()
            new_cluster.exercise = room.exercise
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


        room.exercise.common_skill = json.dumps(common_skill)
        room.exercise.save()


def delete_data():
    # room_id = 21;
    # remove all version
    Version.objects.filter(room=room_id).delete()
