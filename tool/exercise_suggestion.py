# Suggest exercsise depends on mode
# Three mode are provided, hard, normal, easy
# 1: learn (random) new skill, 2: learn particular new skill, 3: reinforce a skill
import random, operator
# from generate_problem_database import generate_problem_database
from exercise.models import Exercise
from user.models import User
import json
from tool.tree import flatten

def exercise_suggestion(seeker, mode, skill):

    seeker_profile = seeker.profile_tree

    seeker_profile_json = json.loads(seeker_profile)
    seeker_profile_json_flatten = flatten(seeker_profile_json)

    #list of elements to learn, from user's profile tree, copied from advisor.py
	thingtocompare = ['basicIO_input','basicIO_output', 'condition_if_ifOnly', 'condition_if_withElse', 'condition_switch', 'loop_single_for', 'loop_single_while',
				'loop_nested', 'array_nonCharArray_singleDim', 'array_nonCharArray_multiDim',
				'array_charArray_singleDim', 'array_charArray_multiDim', 'function_recursion_procedure', 'function_recursion_function', 'function_notRecursion_procedure',
				'function_notRecursion_function', 'class_inheritance_constructor', 'class_inheritance_noConstructor', 'class_noInheritance_constructor',
				'class_noInheritance_noConstructor', 'module_string_length', 'module_string_concat', 'module_string_substr', 'module_string_replace',
				'module_string_changeType', 'module_fileIO_open', 'module_fileIO_close', 'module_fileIO_write', 'module_fileIO_read', 'module_array_length',
				'module_array_concat', 'module_array_split', 'module_array_sort', 'module_array_pop', 'module_array_push', 'module_array_find']

    learn_question_id_dict = dict((el, []) for el in thingtocompare)
    reinforce_question_id_dict = dict((el, []) for el in thingtocompare)
    seeker_ability_dict = jsontocompare(seeker_profile_json_flatten, thingtocompare)

    dictance_dict = dict()

    exercise_list = Exercise.objects.all()

    # complete_count = exercise.complete_student.count()
    # print("Complete:", complete_count)
    for exercise in exercise_list:
        # FIXME: When there are no students in the db, error occurs
        complete_count = exercise.complete_student.count()

        # # demo hardcode
        complete_count = 100

        # print(exercise.complete_student.all())
        if seeker in exercise.complete_student.all():
            continue
        else:
            exercise_problem_json = json.loads(exercise.problem_tree)
            exercise_problem_json_flatten = flatten(exercise_problem_json)
            exercise_problem_dict = jsontocompare(exercise_problem_json_flatten, thingtocompare)
            different_skill, same_skill = diff(seeker_ability_dict, exercise_problem_dict)
            for different in different_skill:
                learn_question_id_dict[different].append(exercise.id)
            for same in same_skill:
                reinforce_question_id_dict[same].append(exercise.id)
    if mode == 1:
        skill = random.choice(learn_question_id_dict.keys())
        learn_question_id = list(learn_question_id_dict[skill].values())
        return random.choice(learn_question_id)
    elif mode == 2:
        learn_question_id = list(learn_question_id_dict[skill].values())
        return random.choice(learn_question_id)
    elif mode == 3:
        reinforce_question_id = list(reinforce_question_id_dict[skill].values())
        return random.choice(reinforce_question_id)

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
        # The range is set for demo
        result = [problem[0] for problem in problem_list if problem[1] == 0]
        if len(problem_list) == 0:
            result = call(problem_list, 3)
    else:
        result = [problem[0] for problem in problem_list if problem[1] < 0]
        if len(problem_list) == 0:
            result = call(problem_list, 2)
    result = random.choice(result)
    return result

def diff(ability_dict, problem_ability_dict):
    different_skill = dict()
    same_skill = dict()
    for ability in ability_list:
        if ability in problem_ability_dict:
            if ability.values != 0:
                same_skill.append(ability)
            else:
                different_skill.append(ability)
        else:
            different_skill.append(ability)
    return same_skill, different_skill

def jsontocompare(user_json, thingtocompare):
    compare_dict = dict()
    for item in thingtocompare:
        compare_dict[item] = user_json[item]
    return compare_dict

if __name__ == "__main__":
    # Not used
    current_user = "test_user_1"
    # Just Hard-code duel to demo
    profile = {'condition': 1, 'loop': 7, 'array': 7, 'function': 3, 'class': 7,
    'module': 7, 'basicIO': 10, '1': True, '2': True, '3': False}
    # Test
    mode = 1
    problem_database = generate_problem_database()
    list_ex = exercise_suggestion(profile, mode, problem_database)
    print(list_ex)
