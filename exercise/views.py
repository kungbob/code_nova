from django.shortcuts import render
from .models import Exercise
from room.models import Room
from user.models import User
from student.models import Student
from cluster.models import Cluster
from django.shortcuts import redirect
from tool.import_data import import_data,delete_data,cluster_data
from tool.tree import get_empty_version_tree,flatten,translate
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
    empty_version_tree = ['basicIO_input','basicIO_output', 'condition_if_ifOnly', 'condition_if_withElse', 'condition_switch', 'loop_single_for', 'loop_single_while',
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

    translated_version_tree = []
    for skill in empty_version_tree:
        translated_version_tree.append({"skill":skill,"name":translate(skill)})


    print(str(translated_version_tree))
    return render(request,'exercise/list_exercise.html',{'exercises':exercises,'translated_version_tree':translated_version_tree})

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
