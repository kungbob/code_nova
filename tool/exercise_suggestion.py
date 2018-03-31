# Suggest exercsise depends on mode

# 1: learn (random) new skill, 2: learn particular new skill, 3: reinforce a skill
import random, operator
# from generate_problem_database import generate_problem_database
from exercise.models import Exercise
from user.models import User
import json
from tool.tree import flatten

def exercise_suggestion(seeker, mode,skill):

    seeker_profile = seeker.profile_tree

    seeker_profile_json = json.loads(seeker_profile)
    seeker_profile_json_flatten = flatten(seeker_profile_json)

    #list of elements to learn, from user's profile tree, copied from advisor.py
    thingtocompare = ['basicIO_input','basicIO_output', 'condition_if_ifOnly', 'condition_if_withElse', 'condition_switch', 'loop_single_for', 'loop_single_while',
    'loop_nested', 'array_nonCharArray_singleDim', 'array_nonCharArray_multiDim','array_charArray_singleDim', 'array_charArray_multiDim', 'function_recursion_procedure', 'function_recursion_function', 'function_notRecursion_procedure',
    'function_notRecursion_function', 'class_inheritance_constructor', 'class_inheritance_noConstructor', 'class_noInheritance_constructor',
    'class_noInheritance_noConstructor', 'module_string_length', 'module_string_concat', 'module_string_substr', 'module_string_replace',
    'module_string_changeType', 'module_fileIO_open', 'module_fileIO_close', 'module_fileIO_write', 'module_fileIO_read', 'module_array_length',
    'module_array_concat', 'module_array_split', 'module_array_sort', 'module_array_pop', 'module_array_push', 'module_array_find']

    learn_question_id_dict = dict((el, []) for el in thingtocompare)
    reinforce_question_id_dict = dict((el, []) for el in thingtocompare)
    seeker_ability_dict = jsontocompare(seeker_profile_json_flatten, thingtocompare)


    print(str(seeker_ability_dict))

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

            exercise_problem = json.loads(exercise.common_skill)

            exercise_problem = [x for x in exercise_problem if x in thingtocompare]


            # exercise_problem_json_flatten = flatten(exercise_problem_json)
            # exercise_problem_dict = jsontocompare(exercise_problem_json_flatten, thingtocompare)


            different_skill, same_skill = diff(seeker_ability_dict.keys(), exercise_problem)

            print("------")
            print(learn_question_id_dict)
            print("------")
            print(reinforce_question_id_dict)

            for different in different_skill:
                learn_question_id_dict[different].append(exercise.id)
            for same in same_skill:
                reinforce_question_id_dict[same].append(exercise.id)



    print(str(learn_question_id_dict))
    print("-----")
    print(str(reinforce_question_id_dict))


    if mode == 1:

        # will not choose skill that has empty list
        skill_list = [x for x in learn_question_id_dict.keys() if learn_question_id_dict[x] != []]

        # all skills have learnt already,
        if skill_list == []:
            return -1;

        random_skill = random.choice([x for x in learn_question_id_dict.keys() if learn_question_id_dict[x] != []])
        learn_question_id = list(learn_question_id_dict[random_skill])
        return random.choice(learn_question_id)

    elif mode == 2:

        exercise_list = list(learn_question_id_dict[skill])

        # no exercise with the specified skill is avaliable,
        if exercise_list == []:
            return -1;

        return random.choice(exercise_list)

    elif mode == 3:

        # will not choose skill that has empty list
        skill_list = [x for x in reinforce_question_id_dict.keys() if reinforce_question_id_dict[x] != []]

        # all skill it a new skill, so no old skill to reinforce
        if skill_list == []:
            return -1;

        random_skill = random.choice(skill_list)
        reinforce_question_id = list(reinforce_question_id_dict[random_skill])
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


def diff(ability_list, problem_ability_list):

    different_skill = []
    same_skill = []


    for problem_ability in problem_ability_list:
        if problem_ability in ability_list:
            same_skill.append(problem_ability)
        else:
            different_skill.append(problem_ability)

    # for ability in ability_list:
    #     if ability in problem_ability_list:
    #         if ability.values != 0:
    #             same_skill.append(ability)
    #         else:
    #             different_skill.append(ability)
    #     else:
    #         different_skill.append(ability)
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
