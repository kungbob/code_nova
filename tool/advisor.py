from tool.tree import get_problem_tree, get_version_tree, flatten

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


def advisor(version_tree, problem_tree, total_count):

	lack_limit = 0.5
	redundance_limit = 0.1

	#lists for storing lacking and redundant elements
	lack = []
	redundance = []
	suggestions = []

	#list of elements for comparison
	compare_list = ['basicIO_output', 'condition_if_ifOnly', 'condition_if_withElse', 'condition_switch', 'loop_single_for', 'loop_single_while',
				'loop_nested_forOnly', 'loop_nested_whileOnly', 'loop_nested_mixed', 'array_nonCharArray_singleDim', 'array_nonCharArray_multiDim',
				'array_charArray_singleDim', 'array_charArray_multiDim', 'function_recursion_procedure', 'function_recursion_function', 'function_notRecursion_procedure',
				'function_notRecursion_function', 'class_inheritance_constructor', 'class_inheritance_noConstructor', 'class_noInheritance_constructor',
				'class_noInheritance_noConstructor', 'module_string_length', 'module_string_concat', 'module_string_substr', 'module_string_replace',
				'module_string_changeType', 'module_fileIO_open', 'module_fileIO_close', 'module_fileIO_write', 'module_fileIO_read', 'module_array_length',
				'module_array_concat', 'module_array_split', 'module_array_sort', 'module_array_pop', 'module_array_push', 'module_array_find']

	#flatten both trees
	flatten_version = flatten(version_tree)
	flatten_problem = flatten(problem_tree)

	#compare all elements in compare_list
	for i in compare_list:
		if flatten_problem[i]/total_count >= lack_limit and flatten_version[i] == 0:
			lack.append(i)
		elif flatten_problem[i]/total_count <= redundance_limit and flatten_version[i] > 0:
			redundance.append(i)


	suggestions.append(message_lack_redundance(lack, redundance, flatten_problem, total_count))
	suggestions.append(message_depth(flatten_version, flatten_problem))
	return suggestions
