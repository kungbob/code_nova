# Suggest exercsise depends on mode
# Three mode are provided, hard, normal, easy
# 1: easy, 2: normal, 3: hard
import random, operator
# from generate_problem_database import generate_problem_database
from exercise.models import Exercise
import json
from tool.tree import flatten

def exercise_suggestion(seeker, mode):


    seeker_profile = seeker.profile_tree

    seeker_profile_json = json.loads(seeker_profile)
    seeker_profile_json_flatten = flatten(seeker_profile_json)
    thingtocompare = ['basicIO', 'condition', 'loop', 'array', 'function', \
                        'class', 'module']
    seeker_ability_dict = jsontocompare(seeker_profile_json_flatten, thingtocompare)

    seeker_ability_list = list(seeker_ability_dict.values())

    dictance_dict = dict()

    exercise_list = Exercise.objects.all()
    for exercise in exercise_list:
        print(exercise.complete_student.all())
        if seeker in exercise.complete_student.all():
            continue
        else:
            exercise_problem_json = json.loads(exercise.problem_tree)
            exercise_problem_json_flatten = flatten(exercise_problem_json)
            exercise_problem_dict = jsontocompare(exercise_problem_json_flatten, thingtocompare)
            exercise_problem_list = list(exercise_problem_dict.values())
            distance = diff(seeker_ability_list, exercise_problem_list)
            dictance_dict[exercise.id] = distance
    if len(dictance_dict) == 0:
        for exercise in exercise_list:
            exercise_problem_json = json.loads(exercise.problem_tree)
            exercise_problem_json_flatten = flatten(exercise_problem_json)
            exercise_problem_dict = jsontocompare(exercise_problem_json_flatten, thingtocompare)
            exercise_problem_list = list(exercise_problem_dict.values())
            distance = diff(seeker_ability_list, exercise_problem_list)
            dictance_dict[exercise.id] = distance
    sorted_distance = sorted(dictance_dict.items(), key=operator.itemgetter(1))
    print(sorted_distance)
    result_problem = call(sorted_distance, mode)
    print(result_problem)
    return result_problem

    '''
    user_list = list(profile.values())
    ability_list = user_list[0:7]
    dictance_dict = dict()
    for problem in problems:
        if problem in profile:
            # The user has finished this problem before
            if profile[problem] == 1:
                continue
        else:
            problem_dict = problems.get(problem)
            problem_list = list(problem_dict.values())
            problem_ability_list = problem_list[0:7]
            # Euclid need to be implemented by ourselves
            distance = diff(ability_list, problem_ability_list)
            dictance_dict[problem] = distance

    sorted_distance = sorted(dictance_dict.items(), key=operator.itemgetter(1))
    result_problem = call(sorted_distance, mode)
    '''

def call(problem_list, mode):
    result = []

    if mode == 1:
        result = [problem[0] for problem in problem_list if problem[1] > 0]
        if len(problem_list) == 0:
            result = call(problem_list, 2)
    elif mode == 2:
        result = [problem[0] for problem in problem_list if problem[1] < 3 or problem[1] > -3]
        if len(problem_list) == 0:
            result = call(problem_list, 3)
    else:
        result = [problem[0] for problem in problem_list if problem[1] < 0]
        if len(problem_list) == 0:
            result = call(problem_list, 2)
    result = random.choice(result)
    return result

def diff(ability_list, problem_ability_list):
    result = 0
    for i in range(7):
        temp = ability_list[i] - problem_ability_list[i]
        result = result + temp
    return result

def jsontocompare(user_json, thingtocompare):
    compare_dict = dict()
    for item in thingtocompare:
        compare_dict[item] = user_json[item]
    return compare_dict

if __name__ == "__main__":
    # Not used
    current_user = "test_user_1"
    # Just Hard-code
    profile = {'condition': 1, 'loop': 7, 'array': 7, 'function': 3, 'class': 7,
    'module': 7, 'basicIO': 10, '1': True, '2': True, '3': False}
    # Test
    mode = 1
    problem_database = generate_problem_database()
    list_ex = exercise_suggestion(profile, mode, problem_database)
    print(list_ex)
