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
    'loop_nested', 'array_nonCharArray_singleDim', 'array_nonCharArray_multiDim',
    'array_charArray_singleDim', 'array_charArray_multiDim', 'function_recursion_procedure', 'function_recursion_function', 'function_notRecursion_procedure',
    'function_notRecursion_function', 'class_inheritance_constructor', 'class_inheritance_noConstructor', 'class_noInheritance_constructor',
    'class_noInheritance_noConstructor', 'lambda', 'comprehension_list', 'comprehension_set', 'comprehension_dict',
    'dataStructure_list_construct', 'dataStructure_list_function_append', 'dataStructure_list_function_extend', 'dataStructure_list_function_insert',
    'dataStructure_list_function_remove', 'dataStructure_list_function_pop', 'dataStructure_list_function_clear', 'dataStructure_list_function_count',
    'dataStructure_list_function_sort', 'dataStructure_list_function_reverse', 'dataStructure_set', 'dataStructure_dict', 'dataStructure_tuple',
    'py-str_construct', 'py-str_attrfunc_count', 'py-str_attrfunc_find', 'py-str_attrfunc_join', 'py-str_attrfunc_partition',
    'py-str_attrfunc_replace', 'py-str_attrfunc_split', 'py-str_attrfunc_splitlines', 'py-buildin_abs', 'py-buildin_all', 'py-buildin_any',
    'py-buildin_ascii', 'py-buildin_bin', 'py-buildin_bool', 'py-buildin_bytearray', 'py-buildin_bytes', 'py-buildin_callable',
    'py-buildin_chr', 'py-buildin_classmethod', 'py-buildin_compile', 'py-buildin_complex', 'py-buildin_delattr', 'py-buildin_dict',
    'py-buildin_dir', 'py-buildin_divmod', 'py-buildin_enumerate', 'py-buildin_eval', 'py-buildin_exec', 'py-buildin_filter',
    'py-buildin_float', 'py-buildin_format', 'py-buildin_frozenset', 'py-buildin_getattr', 'py-buildin_globals', 'py-buildin_hasattr',
    'py-buildin_hash', 'py-buildin_help', 'py-buildin_hex', 'py-buildin_id', 'py-buildin_input', 'py-buildin_int', 'py-buildin_isinstance',
    'py-buildin_issubclass', 'py-buildin_iter', 'py-buildin_len', 'py-buildin_list', 'py-buildin_locals', 'py-buildin_map', 'py-buildin_max',
    'py-buildin_memoryview', 'py-buildin_min', 'py-buildin_next', 'py-buildin_object', 'py-buildin_oct', 'py-buildin_open', 'py-buildin_ord',
    'py-buildin_pow', 'py-buildin_print', 'py-buildin_property', 'py-buildin_range', 'py-buildin_repr', 'py-buildin_reversed',
    'py-buildin_round', 'py-buildin_set', 'py-buildin_setattr', 'py-buildin_slice', 'py-buildin_sorted', 'py-buildin_staticmethod',
    'py-buildin_str', 'py-buildin_sum', 'py-buildin_super', 'py-buildin_tuple', 'py-buildin_type', 'py-buildin_vars', 'py-buildin_zip',
    'py-buildin___import__', 'module_collections_namedtuple()', 'module_collections_deque', 'module_collections_ChainMap',
    'module_collections_Counter', 'module_collections_OrderedDict', 'module_collections_defaultdict', 'module_collections_UserDict',
    'module_collections_UserList', 'module_collections_UserString', 'module_fileIO_open', 'module_fileIO_close', 'module_fileIO_write',
    'module_fileIO_read']

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

            print("----different--")
            print(str(different_skill))
            print("---same---")
            print(str(same_skill))
            print("-------")

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
