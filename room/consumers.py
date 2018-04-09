import json
from channels import Channel
from django.urls import reverse
from channels.auth import channel_session_user_from_http, channel_session_user
from user.models import User
# from .settings import MSG_TYPE_LEAVE, MSG_TYPE_ENTER, NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS
from .models import Room
from student.models import Student
from version.models import Version
from .utils import get_room_or_error, catch_client_error
from .exceptions import ClientError
from tool.find_helper import find_helper
from tool.compile_code import compile_code
from tool.analyser import analyser
from tool.advisor import advisor
from tool.tree import flatten,add_tree,reduce_tree
from tool.exercise_suggestion import exercise_suggestion

from tool.clustering import clustering

from cluster.models import Cluster
from exercise.models import Exercise

import numpy as np
import datetime
import time
import _thread
import random


CONST_MIN_VERSION = 10

@channel_session_user_from_http
def ws_connect(message):


    if message.user.is_authenticated():
        # add reply channel to user model

        message.user.reply_channel = str(message.reply_channel)
        message.user.save()

        message.reply_channel.send({'accept': True})
        message.channel_session['rooms'] = []


@channel_session_user
def ws_receive(message):

    # redirect all received message to other websocket handler

    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("room.receive").send(payload)

@channel_session_user
def ws_disconnect(message):

    for room_id in message.channel_session.get("rooms", set()):
        try:

            #remove reply_channel from websocket
            room = Room.objects.get(pk=room_id)
            room.websocket_group.discard(message.reply_channel)

            output_message = {"leave": room.id,"email":message.user.email,"user_id":message.user.id}
            temp_history = json.loads(room.chat_history)
            temp_history["chat_history"].append(output_message)
            room.chat_history = json.dumps(temp_history)

            room.save()
            room.broadcast(output_message)


            room.save()


        except Room.DoesNotExist:
            pass



    if message.user.is_authenticated():
        # print("deleting ")

        # try remove reply channel from user model
        message.user.reply_channel = ""
        message.user.save()

        student = Student.objects.get(user=message.user)

        # if user is room owner, remove help request of the rooms
        # prevent infinite loop of search helpers

        for room in student.room_owner_set.all():
            room.require_help = False
            room.save()


@catch_client_error
@channel_session_user
def join_room(message):

    print("joining room")
    print(message.user)
    room = get_room_or_error(message["room"], message.user)
    room.websocket_group.add(message.reply_channel)

    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))


    output_message = {"join": room.id,"email":message.user.email,"user_id":message.user.id}
    temp_history = json.loads(room.chat_history)
    temp_history["chat_history"].append(output_message)
    room.chat_history = json.dumps(temp_history)

    room.save()
    room.broadcast(output_message)

# ------------------------------------------------------

@channel_session_user
def leave_room(message):



    room = get_room_or_error(message["room"], message.user)

    # if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
    #     room.send_message(None, message.user, MSG_TYPE_LEAVE)

    room.websocket_group.discard(message.reply_channel)

    output_message = {"leave": room.id,"email":message.user.email,"user_id":message.user.id}

    temp_history = json.loads(room.chat_history)
    temp_history["chat_history"].append(output_message)
    room.chat_history = json.dumps(temp_history)

    room.save()
    room.broadcast(output_message)


@channel_session_user
def chat_send(message):

    room = get_room_or_error(message["room"], message.user)
    output_message = {'room': room.id, 'chat': message["chat"], 'user_id': message.user.id, 'email':message.user.email,'time':message["time"]}
    print("chat:"+str(message))

    temp_history = json.loads(room.chat_history)

    temp_history["chat_history"].append(output_message)


    room.chat_history = json.dumps(temp_history)

    room.save()

    room.broadcast(output_message)

@channel_session_user
def chat_load(message):

    # if int(message['room']) not in message.channel_session['rooms']:
    #     raise ClientError("ROOM_ACCESS_DENIED")

    room = get_room_or_error(message["room"], message.user)

    message.reply_channel.send({
        "text": room.chat_history,
    })


# ------------------------------------------------------------
@catch_client_error
@channel_session_user
def editor_send(message):
    # if int(message['room']) not in message.channel_session['rooms']:
    #     raise ClientError("ROOM_ACCESS_DENIED")
    room = get_room_or_error(message["room"], message.user)

# closed for demo
    # # for index,temp_line in enumerate(temp_code):
    # #     temp_code[index] = temp_line + "\r\n"
    #
    # temp_change = message["change"]
    # start_row = temp_change["start"]["row"]
    # start_column = temp_change["start"]["column"]
    # end_row = temp_change["end"]["row"]
    # end_column = temp_change["end"]["column"]
    #
    # temp_end = temp_change["end"]
    # temp_lines = temp_change["lines"]
    # temp_action  = temp_change["action"]
    #
    # # print("row:"+str(start_row))
    # # print("column:" + str(start_column))
    # # print("lines:"+str(temp_lines))
    #
    # if temp_action == "insert":
    #     # perform insert
    #
    #     temp_code = room.code.split("\r\n")
    #     # temp_code = room.code.splitlines()
    #     # print(temp_code)
    #
    #
    #     # print("length:"+ str(len(temp_code)))
    #     if (start_row >= len(temp_code)):
    #         # append at the last
    #         temp_code.append("\r\n".join(temp_lines))
    #
    #     else:
    #
    #         current_line = temp_code[start_row]
    #
    #         left_line = temp_code[start_row][:start_column]
    #         right_line = temp_code[start_row][start_column:]
    #
    #         # print("line:" + current_line)
    #         # print("left:"+left_line + "|right :"+right_line)
    #         # print(temp_change["lines"] == ["",""])
    #         # for temp_char in temp_change["lines"]:
    #         #     print("temp_char:"+str(len(temp_char)))
    #
    #         new_line = "\r\n".join(temp_lines)
    #         current_line = left_line + new_line + right_line
    #
    #         temp_code[start_row] = current_line
    #
    #     # room.code = ''.join(temp_code)
    #
    #     room.code = '\r\n'.join(temp_code)
    #
    #     # for line in temp_code:
    #     #     print("fianl:"+ line)
    #     room.save()
    #
    # elif temp_action == "remove":
    #
    #     temp_code = room.code.split("\r\n")
    #     for index,temp_line in enumerate(temp_code):
    #         if index != (len(temp_code) - 1):
    #             temp_code[index] = temp_line + "\r\n"
    #
    #     # temp_code = room.code.splitlines()
    #     print(str(temp_code))
    #
    #
    #     if start_row == end_row:
    #         # delete in same row
    #         left_line = temp_code[start_row][:start_column]
    #         right_line = temp_code[end_row][end_column:]
    #
    #         print("left:"+left_line+"|right:"+right_line)
    #
    #         temp_code[start_row] = left_line + right_line
    #
    #     elif start_row < end_row:
    #         #delete multiline
    #         for index,temp_line in enumerate(temp_code):
    #             if index == start_row:
    #                 temp_code[index] = temp_code[start_row][:start_column]
    #                 print("start_line :" + temp_code[index])
    #             elif index > start_row and index < end_row:
    #                 temp_code[index] = ""
    #                 print("empty")
    #             elif index == end_row:
    #                 temp_code[index] = temp_code[end_row][end_column:]
    #                 print("last_line :" + temp_code[index])
    #
    #     if "" in temp_code:
    #         # temp_code.remove([])
    #         temp_code = [x for x in temp_code if x != ""]
    #
    #     print("check:"+str(temp_code))
    #     # for line in temp_code:
    #     #     print("fianl:"+ line)
    #
    #     room.code = ''.join(temp_code)
    #     room.save()
        #perform remove

    output_message = {'room': room.id, 'change': message["change"], 'user_id': message.user.id}
    room.broadcast(output_message)
    #
    # room.send_message(message["change"], message.user)

@channel_session_user
def editor_load(message):
    # if int(message['room']) not in message.channel_session['rooms']:
    #     raise ClientError("ROOM_ACCESS_DENIED")
    room = get_room_or_error(message["room"], message.user)

    message.reply_channel.send({
        "text": json.dumps({
            "code": str(room.code),
        }),
    })




@channel_session_user
def editor_save(message):
    if int(message['room']) not in message.channel_session['rooms']:
        raise ClientError("ROOM_ACCESS_DENIED")
    room = get_room_or_error(message["room"], message.user)

    room.code = message["code"]
    room.save()
    print("saved")

@catch_client_error
@channel_session_user
def editor_save_run(message):

    room = get_room_or_error(message["room"], message.user)
    code = message["code"]

    # run the code with test cases of the exercise
    result = compile_code(code,room.exercise)


    if result["overall_success"] == True:

        # print("all pass")

        overall_success = True
    else:
        overall_success = False
        # print("failed")

    room.code = message["code"]
    room.save()

    result_json = json.dumps(result)

    version = Version()
    try:
        version_tree = analyser(code)
        version_tree_json = json.dumps(version_tree)
        version.version_tree = version_tree_json

    except Exception as e:
        # version tree cannot be generated
        version.version_tree = ""



    version.code = message["code"]
    version.room = room
    version.exercise = room.exercise
    version.result = result_json
    version.overall_success = overall_success
    version.save()

    # when it is a success submission


    if overall_success:

        student = Student.objects.get(user=message.user)

        # add complete student to exercise
        room.exercise.complete_student.add(student)
        room.exercise.save()

        data_matrix = []
        version_list = Version.objects.filter(exercise=room.exercise,overall_success=True)


        student = Student.objects.get(user=message.user)
        profile_tree = json.loads(student.profile_tree)

        # reduce to 0 and 1
        reduce_version_tree = reduce_tree(version_tree)

        # udpate profile tree
        new_profile_tree = add_tree(profile_tree,version_tree);

        student.profile_tree = json.dumps(new_profile_tree)

        student.save()

        # will only run when the number of success submission is >= limit
        if len(version_list) >= CONST_MIN_VERSION :


            # remove all old clusters

            Cluster.objects.filter(exercise=room.exercise).delete()

            cluster_result = clustering(version_list)

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


    #
    message.reply_channel.send({
        "text": json.dumps(result),
    })


@channel_session_user
def ask_suggestion(message):

    student = Student.objects.get(user = message.user)
    suggestion_id = exercise_suggestion(student,message["mode"],message["skill"])

    # if there is no suggestion
    if suggestion_id == -1:

        exercise = random.choice(Exercise.objects.all())
    else:
        exercise = Exercise.objects.get(pk=suggestion_id)


    url = reverse('exercise',kwargs={'exercise_id':exercise.id})

    suggestion_json = {"exercise_title":exercise.title,"suggestion":exercise.id,"url":url}
    message.reply_channel.send({
        "text": json.dumps(suggestion_json),
    })


@channel_session_user
def ask_advice(message):

    room = get_room_or_error(message["room"], message.user)
    code = message["code"]


    version_tree = analyser(code)
    advice = advisor(room.exercise.id,version_tree)

    print(str(advice))

    message.reply_channel.send({
        "text": json.dumps(advice),
    })


    # print(advice)


    # try:
    #     version_tree = analyser(code)
    #     advice = advisor(room.exercise.id,version_tree)
    #     print(advice)
    #
    #     message.reply_channel.send({
    #         "text": json.dumps(advice),
    #     })
    #
    #
    # except Exception as e:
    #     # when version tree can not be generated
    #     print(e)












    # try:
    #     # problem_tree = json.loads(room.exercise.problem_tree)
    #
    #     version_tree = analyser(code)
    #
    #     # advice = advisor(version_tree,problem_tree,total_count)
    #
    #     advice = advisor(room.exercise.id,version_tree)
    #
    #     print(advice)
    #
    #     # advice_json = {"advice":advice}
    #     # message.reply_channel.send({
    #     #     "text": json.dumps(advice_json),
    #     # })
    #
    #
    # except:
    #     pass




@channel_session_user
def search_helper(message):


    code = message["code"]
    print(code)

    room = Room.objects.get(pk=message["room"])

    room.require_help = True
    room.save()

    print(message.user)

    # helper_list = find_helper(message.user,room.exercise)
    # return list of User object
    seeker = Student.objects.get(user=message.user)
    helper_list = find_helper(code,seeker,room.exercise)
    print("-------------------------")
    print(helper_list)

    for helper_id in helper_list:
        if room.require_help == False:
            break
        student = Student.objects.get(pk=helper_id)
        user = student.user
        output_json =  {
                "room_id": room.id,
                "help_seeker": user.email,
                "exercise_title":room.exercise.title,
                "url": reverse('accept_help_request',kwargs={'room_id':room.id})

            }

        print(output_json)

        # use another thread to send the message
        _thread.start_new_thread(channel_send_thread,(user.reply_channel,output_json,))
        time.sleep(20)




    # while room.require_help:
    #
    #     student = Student.objects.get(pk=helper_list[count])
    #     user = student.user
    #
    #     output_json =  {
    #             "room_id": room.id,
    #             "help_seeker": user.email,
    #             "exercise_title":room.exercise.title,
    #             "url": reverse('accept_help_request',kwargs={'room_id':room.id})
    #
    #         }
    #
    #     # use another thread to send the message
    #     _thread.start_new_thread(channel_send_thread,(user.reply_channel,output_json,))
    #
    #
    #     # find a helper every 20s
    #     time.sleep(20)
    #     room = Room.objects.get(pk=message["room"])
    #     count = count + 1

    print("search end")

def channel_send_thread(reply_channel,output_json):

    print("reply_channel="+reply_channel)
    # print("send start")
    Channel(reply_channel).send({
        "text": json.dumps(output_json),
    })

    # print("send end")
