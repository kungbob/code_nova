from tool.tree import  flatten, translate, flatten_self_define, get_empty_version_tree
from tool.analyser import analyser
from scipy.spatial import distance
from cluster.models import Cluster
from exercise.models import Exercise
from version.models import Version
import numpy as np # linear algebra
import json
from sklearn.preprocessing import StandardScaler


def advisor(ex_id, version_tree):

	wanted_list = []

	unwanted_list = []
	for i in list(flatten(get_empty_version_tree()).keys()):
		if i not in wanted_list:
			unwanted_list.append(i)

	flatten_tree = flatten(version_tree)
	for i in unwanted_list:
		flatten_tree.pop(i, None)

	exercise = Exercise.objects.get(pk=ex_id)


	# list of all version
	version_list = Version.objects.filter(exercise=exercise)

	# data_matrix used for standardization
	data_matrix = []

	for version in version_list:

		flatten_json = flatten(json.loads(version.version_tree))
		for i in unwanted_list:
			flatten_json.pop(i, None)

		flatten_list = list(flatten_json.values())
		data_matrix.append(flatten_list)


	scaler = StandardScaler().fit(data_matrix)


	standardized_data = scaler.transform(np.array([list(flatten_tree.values())]))

	cluster_list = Cluster.objects.filter(exercise=exercise)


	#list of elements for comparison
	compare_list = ['basicIO_input','basicIO_output', 'condition_if_ifOnly', 'condition_if_withElse', 'condition_switch', 'loop_single_for', 'loop_single_while',
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


	advice_list = []

	max_cluster_id = 0
	max_cluster_count = 0

	nearest_cluster_id = cluster_list[0].id

	center = cluster_list[0].center.split(',')
	for i in range(0, len(center)):
		center[i] = float(center[i])

	nearest_cluster_dis = distance.euclidean(standardized_data,np.array(center))

	for cluster in cluster_list:

		necessary_skill_list = json.loads(cluster.necessary_skill)
		redundant_skill_list = json.loads(cluster.redundant_skill)
		character_skill_list = json.loads(cluster.character_skill)
		other_skill_list = json.loads(cluster.other_skill)


		lacking = []
		redundance = []
		character = []
		others = []

		if max_cluster_count < cluster.data_count:
			max_cluster_id = cluster.id

		center = cluster.center.split(',')
		for i in range(0, len(center)):
			center[i] = float(center[i])

		dist = distance.euclidean(standardized_data,np.array(center))

		if nearest_cluster_dis > dist:
			nearest_cluster_id = cluster.id

		for skill in necessary_skill_list:
			if flatten_tree[skill] == 0 and skill in compare_list:
				lacking.append(translate(skill))

		for skill in redundant_skill_list:
			if flatten_tree[skill] > 0 and skill in compare_list:
				redundance.append(translate(skill))

		for skill in character_skill_list:
			if skill in compare_list:
				character.append(translate(skill))

		for skill in other_skill_list:
			if flatten_tree[skill["name"]] != skill["mode"]:
				others.append({"name": translate(skill["name"]), "current": flatten_tree[skill["name"]], "suggestion": skill["mode"]})


		advice_list.append({"cluster_id": cluster.id,"data_count":cluster.data_count,"character_skill":character,"lacking": lacking, "redundance": redundance, "other_skill": others})

	output = {"max_cluster_id": max_cluster_id, "nearest_cluster_id": nearest_cluster_id, "advice_list": advice_list}

	return output







def message_lack_redundance (lack, redundance, flatten_problem, total_count):



	#a dictionary to convert dictionary terms to natural language terms
	conversion_list = {"basicIO_input": "Basic Input", "basicIO_output": "Basic Output", "condition_if_ifOnly": "If (Without else)",
				"condition_if_withElse": "If (With else)", "condition_switch": "Switch", "loop_single_for": "Single For-loop", "loop_single_while": "Single While-loop",
				"loop_nested_forOnly": "Nested For-loop", "loop_nested_whileOnly": "Nested While-loop", "loop_nested_mixed": "Nested Loop (For and While)",
				"array_nonCharArray_singleDim": "Non-character Array (Single Dimension)", "array_nonCharArray_multiDim": "Non-character Array (Multi-Dimension)",
				"array_charArray_singleDim": "Character Array (Single Dimension)", "array_charArray_multiDim": "Character Array (Multi-Dimension)",
				"function_recursion_procedure": "Procedure with Recursion", "function_recursion_function": "Function with Recursion",
				"function_notRecursion_procedure": "Procedure without Recursion", "function_notRecursion_function": "Function without Recursion",
				"class_inheritance_constructor": "Class (With Inheritance and Constructor)", "class_inheritance_noConstructor": "Class (With Inheritance and Without Constructor)",
				"class_noInheritance_constructor": "Class (Without Inheritance and With Constructor)", "class_noInheritance_noConstructor": "Class (Without Inheritance and Constructor)",
				"module_string_length": "String-Length", "module_string_concat": "String-Concatenate", "module_string_substr": "String-Substring",
				"module_string_replace": "String-Replace", "module_string_changeType": "String-Change Type", "module_fileIO_open": "FileIO-Open",
				"module_fileIO_close": "FileIO-Close", "module_fileIO_write": "FileIO-Write", "module_fileIO_read": "FileIO-Read",
				"module_array_length": "Array-Length", "module_array_concat": "Array-Concatenate", "module_array_split": "Array-Split",
				"module_array_sort": "Array-Sort", "module_array_pop": "Array-Pop", "module_array_push": "Array-Push", "module_array_find": "Array-Find"}

	str = "You may try the followings to improve your program:\n\n"

	if lack:
		if len(lack) == 1:
			str = str + "%d out of the %d (%.2f%%) correct solutions contain " % (flatten_problem[lack[0]], total_count, 100*flatten_problem[lack[0]]/total_count) + conversion_list[lack[0]] + " while your program does not.\n"
			str = str + "You may try to utilize this element in your program to see whether the problem can be solved.\n\n"
		else:
			str = str + "Majority of the correct solutions contain the following elements while your program does not.\n"
			for i in lack:
				str = str + "%d out of the %d (%.2f%%) correct solutions contain " % (flatten_problem[i], total_count, 100*flatten_problem[i]/total_count) + conversion_list[i] + ".\n"
			str = str + "You may try to utilize these elements in your program to see whether the problem can be solved.\n\n"

	if redundance:
		if len(redundance) == 1 and flatten_problem[redundance[0]] == 0:
			str = str + "Your program contains " + conversion_list[redundance[0]] + " while all of the %d correct solutions do not.\n" % (total_count)
			str = str + "You may check whether this element is necessary for this exercise.\n\n"
		elif len(redundance) == 1 and flatten_problem[redundance[0]] > 0:
			str = str + "Your program contains " + conversion_list[redundance[0]] + " while only %d out of the %d (%.2f%%) correct solutions contain this element.\n" % (flatten_problem[redundance[0]], total_count, 100*flatten_problem[redundance[0]]/total_count)
			str = str + "You may check whether this element is necessary for this exercise.\n\n"
		else:
			str = str + "Your program contains the following elements while most of the correct solutions do not.\n"
			for i in redundance:
				if flatten_problem[i] == 0:
					str = str + "None of the %d correct solutions contains " % (total_count) + conversion_list[i] + ".\n"
				else:
					str = str + "Only %d out of the %d (%.2f%%) correct solutions contain " % (flatten_problem[i], total_count, 100*flatten_problem[i]/total_count) + conversion_list[i] + ".\n"
			str = str + "You may check whether these elements are necessary for this exercise.\n\n"

	return str

def message_depth (flatten_version, flatten_problem):

	str = ""
	#further check the maxIfDepth, maxLoopDepth and maxArrayDim
	if flatten_version['maxIfDepth'] != flatten_problem['maxIfDepth']:
		str = str + "Maximum depth of 'if' in your program is %d while the maximum depth of 'if' in the correct answer is %d. You may check the implementation of 'if' again.\n" % (flatten_version['maxIfDepth'], flatten_problem['maxIfDepth'])
		str = str + "\n"

	if flatten_version['maxLoopDepth'] != flatten_problem['maxLoopDepth']:
		str = str + "Maximum depth of loop in your program is %d while the maximum depth of loop in the correct answer is %d. You may check the implementation of loop again.\n" % (flatten_version['maxLoopDepth'], flatten_problem['maxLoopDepth'])
		str = str + "\n"

	if flatten_version['maxArrayDim'] != flatten_problem['maxArrayDim']:
		str = str + "Maximum dimension of arrray in your program is %d while the maximum dimension of array in the correct answer is %d. You may check the implementation of array again.\n" % (flatten_version['maxArrayDim'], flatten_problem['maxArrayDim'])
		str = str + "\n"

	return str
