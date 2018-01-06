# list must be same length
#
# Question need to have the average ability point required in the question
#

from scipy.spatial.distance import *
import operator
# from generate_user_database import generate_user_database
from student.models import Student
from user.models import User
from tool.tree import flatten
import json

# seeker: user object
def find_helper(seeker, current_exercise):
    # seeker profile into dict

    student_list = Student.objects.all()




    seeker_profile = seeker.profile_tree

    seeker_profile_json = json.loads(seeker_profile)
    seeker_profile_json_flatten = flatten(seeker_profile_json)
    print(seeker_profile_json)
    print(flatten(seeker_profile_json))

    seeker_profile_json
    thingtocompare = ['basicIO', 'condition', 'loop', 'array', 'function', \
                        'class', 'module']
    seeker_ability_list = jsontocompare(seeker_profile_json_flatten, thingtocompare)
    print(seeker_ability_list)
    # print(my_json)
    dictance_dict = dict()
    for helper in student_list:
        helper_profile_json = json.loads(helper.profile_tree)
        print(temp)
        if seeker.id == helper.id:
            continue
        else:
            helper_dict = jsontocompare(helper_profile_json)
            


    # seeker_profile = flatten(my_json)
    #
    #
    # print(seeker_profile)


    # seeker_dict = users.get(seeker)
    #
    #
    #
    #
    # seeker_list = list(seeker_dict.values())
    # # Only first seven part is the ability, later part is the exercise_no
    # seeker_ability_list = seeker_list[0:7]
    #
    # dictance_dict = dict()
    # for helper in users:
    #     if helper == seeker:
    #         continue
    #     else:
    #         helper_dict = users.get(helper)
    #         # If helper does not finish this exercise before, skip
    #         if not helper_dict[current_exercise]:
    #             continue
    #         helper_list = list(helper_dict.values())
    #         helper_ability_list = helper_list[0:7]
    #         # Use Eculidean method
    #         distance = euclidean(seeker_ability_list, helper_ability_list)
    #         dictance_dict[helper] = distance
    # # If no one finish this exercise before, rerun seeking process:
    # if len(dictance_dict) == 0:
    #     for helper in users:
    #         if helper == seeker:
    #             continue
    #         else:
    #             helper_dict = users.get(helper)
    #             helper_list = list(helper_dict.values())
    #             helper_ability_list = helper_list[0:7]
    #             # Use Eculidean method
    #             distance = euclidean(seeker_ability_list, helper_ability_list)
    #             dictance_dict[helper] = distance
    # # In ascending order
    # sorted_distance = sorted(dictance_dict.items(), key=operator.itemgetter(1))
    # # Set return 10 users
    # call_list = call(sorted_distance, 10)
    # print(call_list)
    # return call_list

def jsontocompare(user_json, thingtocompare):
    compare_dict = dict()
    for item in thingtocompare:
        compare_dict[item] = user_json[item]
    return compare_dict

def call(helper_list, number):
    call_list = helper_list[:number]
    name_list = [name[0] for name in call_list]
    number_list = [name[1] for name in call_list]
    return name_list

if __name__ == "__main__":
    database = generate_user_database()
    seeker = "test_user_1"
    print("Seeker is: " + seeker)
    current_exercise = "01"
    print("Current exercise is:" + current_exercise)
    helper_list = find_helper(seeker, current_exercise, database)
