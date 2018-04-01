import collections

def get_empty_problem_tree():

    problem_tree = {"basicIO" : {"value" : 0, "input" : {"value" : 0}, "output" : {"value" : 0}},
        "condition" : {"value" : 0, "if" : {"value" : 0, "ifOnly" : {"value" : 0}, "withElse" : {"value" : 0}}, "switch" : {"value" : 0}},
        "loop" : {"value" : 0, "single" : {"value" : 0, "for" : {"value" : 0}, "while" : {"value" : 0}},
                               "nested" : {"value" : 0, "forOnly" : {"value" : 0}, "whileOnly" : {"value" : 0}, "mixed" : {"value" : 0}}},
        "array" : {"value" : 0, "nonCharArray": {"value" : 0, "singleDim": {"value" : 0}, "multiDim": {"value" : 0}}, "charArray": {"value" : 0, "singleDim": {"value" : 0}, "multiDim": {"value" : 0}}},
        "function" : {"value" : 0, "recursion": {"value" : 0, "procedure": {"value" : 0}, "function": {"value" : 0}}, "notRecursion": {"value" : 0, "procedure": {"value" : 0}, "function": {"value" : 0}}},
        "class" : {"value" : 0, "inheritance": {"value" : 0, "constructor": {"value" : 0}, "noConstructor": {"value" : 0}}, "noInheritance": {"value" : 0, "constructor": {"value" : 0}, "noConstructor": {"value" : 0}}},
        "module" : {"value" : 0, "string": {"value" : 0, "length": {"value" : 0}, "concat": {"value" : 0}, "substr": {"value" : 0}, "replace": {"value" : 0}, "changeType": {"value" : 0}},
                                 "fileIO": {"value" : 0, "open": {"value" : 0}, "close": {"value" : 0}, "write": {"value" : 0}, "read": {"value" : 0}},
                                 "array": {"value" : 0, "length": {"value" : 0}, "concat": {"value" : 0}, "split": {"value" : 0}, "sort": {"value" : 0}, "pop": {"value" : 0}, "push": {"value" : 0}, "find": {"value" : 0}}},
        "maxIfDepth" : {"value" : 0},
        "maxLoopDepth" : {"value" : 0},
        "totalArraySize" : {"value" : 0},
        "maxArrayDim" : {"value" : 0}
       }


    return problem_tree


def get_empty_version_tree():

	version_tree = {'basicIO' : {'value' : 0, 'input' : {'value' : 0}, 'output' : {'value' : 0}}, 
         'condition' : {'value' : 0, 'if' : {'value' : 0, 'ifOnly' : {'value' : 0}, 'withElse' : {'value' : 0}}, 'switch' : {'value' : 0}}, 
         'loop' : {'value' : 0, 'single' : {'value' : 0, 'for' : {'value' : 0}, 'while' : {'value' : 0}}, 
                                'nested' : {'value' : 0, 'forOnly' : {'value' : 0}, 'whileOnly' : {'value' : 0}, 'mixed' : {'value' : 0}}}, 
         'array' : {'value' : 0, 'nonCharArray': {'value' : 0, 'singleDim': {'value' : 0}, 'multiDim': {'value' : 0}}, 'charArray': {'value' : 0, 'singleDim': {'value' : 0}, 'multiDim': {'value' : 0}}}, 
         'function' : {'value' : 0, 'recursion': {'value' : 0, 'procedure': {'value' : 0}, 'function': {'value' : 0}}, 'notRecursion': {'value' : 0, 'procedure': {'value' : 0}, 'function': {'value' : 0}}}, 
         'class' : {'value' : 0, 'inheritance': {'value' : 0, 'constructor': {'value' : 0}, 'noConstructor': {'value' : 0}}, 'noInheritance': {'value' : 0, 'constructor': {'value' : 0}, 'noConstructor': {'value' : 0}}}, 
         'lambda' : {'value' : 0}, 
         'comprehension' : {'value' : 0, 'list' : {'value' : 0}, 'set' : {'value' : 0}, 'dict' : {'value' : 0}},
         'dataStructure' : {'value' : 0, 'list' : {'value' : 0, 'construct' : {'value' : 0}, 'function' : {'value' : 0, 'append' : {'value' : 0}, 'extend' : {'value' : 0}, 'insert' : {'value' : 0}, 'remove' : {'value' : 0}, 'pop' : {'value' : 0}, 'clear' : {'value' : 0}, 'count' : {'value' : 0}, 'sort' : {'value' : 0}, 'reverse' : {'value' : 0}}}, 
                                   'set' : {'value' : 0}, 'dict' : {'value' : 0}, 'tuple' : {'value' : 0}}, 
         'py-str' : {'value' : 0, 'construct' : {'value' : 0}, 'attrfunc' : {'value' : 0, 'count' : {'value' : 0}, 'find' : {'value' : 0}, 'join' : {'value' : 0}, 'partition' : {'value' : 0}, 'replace' : {'value' : 0}, 'split' : {'value' : 0}, 'splitlines' : {'value' : 0}}},
         'py-buildin': {'value' : 0, 'abs' : {'value' : 0}, 'all' : {'value' : 0}, 'any' : {'value' : 0}, 'ascii' : {'value' : 0}, 'bin' : {'value' : 0}, 'bool' : {'value' : 0}, 'bytearray' : {'value' : 0}, 'bytes' : {'value' : 0}, 'callable' : {'value' : 0}, 'chr' : {'value' : 0}, 
                                     'classmethod' : {'value' : 0}, 'compile' : {'value' : 0}, 'complex' : {'value' : 0}, 'delattr' : {'value' : 0}, 'dict' : {'value' : 0}, 'dir' : {'value' : 0}, 'divmod' : {'value' : 0}, 'enumerate' : {'value' : 0}, 'eval' : {'value' : 0}, 
                                     'exec' : {'value' : 0}, 'filter' : {'value' : 0}, 'float' : {'value' : 0}, 'format' : {'value' : 0}, 'frozenset' : {'value' : 0}, 'getattr' : {'value' : 0}, 'globals' : {'value' : 0}, 'hasattr' : {'value' : 0}, 'hash' : {'value' : 0}, 
                                     'help' : {'value' : 0}, 'hex' : {'value' : 0}, 'id' : {'value' : 0}, 'input' : {'value' : 0}, 'int' : {'value' : 0}, 'isinstance' : {'value' : 0}, 'issubclass' : {'value' : 0}, 'iter' : {'value' : 0}, 'len' : {'value' : 0}, 'list' : {'value' : 0}, 
                                     'locals' : {'value' : 0}, 'map' : {'value' : 0}, 'max' : {'value' : 0}, 'memoryview' : {'value' : 0}, 'min' : {'value' : 0}, 'next' : {'value' : 0}, 'object' : {'value' : 0}, 'oct' : {'value' : 0}, 'open' : {'value' : 0}, 'ord' : {'value' : 0}, 
                                     'pow' : {'value' : 0}, 'print' : {'value' : 0}, 'property' : {'value' : 0}, 'range' : {'value' : 0}, 'repr' : {'value' : 0}, 'reversed' : {'value' : 0}, 'round' : {'value' : 0}, 'set' : {'value' : 0}, 'setattr' : {'value' : 0}, 'slice' : {'value' : 0}, 
                                     'sorted' : {'value' : 0}, 'staticmethod' : {'value' : 0}, 'str' : {'value' : 0}, 'sum' : {'value' : 0}, 'super' : {'value' : 0}, 'tuple' : {'value' : 0}, 'type' : {'value' : 0}, 'vars' : {'value' : 0}, 'zip' : {'value' : 0}, '__import__' : {'value' : 0}},
         'module' : {'value' : 0, 'collections': {'value' : 0, 'namedtuple()': {'value' : 0}, 'deque': {'value' : 0}, 'ChainMap': {'value' : 0}, 'Counter': {'value' : 0}, 'OrderedDict': {'value' : 0}, 'defaultdict': {'value' : 0}, 'UserDict': {'value' : 0}, 'UserList': {'value' : 0}, 'UserString': {'value' : 0}}, 
                                  'fileIO': {'value' : 0, 'open': {'value' : 0}, 'close': {'value' : 0}, 'write': {'value' : 0}, 'read': {'value' : 0}}}, 
         'maxIfDepth' : {'value' : 0}, 
         'maxLoopDepth' : {'value' : 0}, 
         'maxArraySize' : {'value' : 0}, 
         'maxArrayDim' : {'value' : 0}
        }
	
	return version_tree

def add_tree(tree,new_tree):

    if type(tree) == int:
        tree = tree + new_tree
        return tree

    for key,value in tree.items():
        # print("key:"+key+"  value:"+str(value))
        tree[key] = add_tree(tree[key],new_tree[key])

    return tree


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
        	new_key = new_key[:-6]
        	items.append((new_key, v))
    return dict(items)

def flatten_self_define(d, wanted_list ,parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_self_define(v, wanted_list, new_key, sep=sep).items())
        else:
            new_key = new_key[:-6]
            if new_key in wanted_list:
                items.append((new_key, v))
    return dict(items)


def get_problem_tree():

    problem_tree = {"basicIO" : {"value" : 200, "input" : {"value" : 100}, "output" : {"value" : 100}},
        "condition" : {"value" : 3, "if" : {"value" : 3, "ifOnly" : {"value" : 3}, "withElse" : {"value" : 0}}, "switch" : {"value" : 0}},
        "loop" : {"value" : 98, "single" : {"value" : 3, "for" : {"value" : 3}, "while" : {"value" : 0}},
                               "nested" : {"value" : 95, "forOnly" : {"value" : 95}, "whileOnly" : {"value" : 0}, "mixed" : {"value" : 0}}},
        "array" : {"value" : 3, "nonCharArray": {"value" : 3, "singleDim": {"value" : 3}, "multiDim": {"value" : 0}}, "charArray": {"value" : 0, "singleDim": {"value" : 0}, "multiDim": {"value" : 0}}},
        "function" : {"value" : 0, "recursion": {"value" : 0, "procedure": {"value" : 0}, "function": {"value" : 0}}, "notRecursion": {"value" : 0, "procedure": {"value" : 0}, "function": {"value" : 0}}},
        "class" : {"value" : 0, "inheritance": {"value" : 0, "constructor": {"value" : 0}, "noConstructor": {"value" : 0}}, "noInheritance": {"value" : 0, "constructor": {"value" : 0}, "noConstructor": {"value" : 0}}},
        "module" : {"value" : 0, "string": {"value" : 0, "length": {"value" : 0}, "concat": {"value" : 0}, "substr": {"value" : 0}, "replace": {"value" : 0}, "changeType": {"value" : 0}},
                                 "fileIO": {"value" : 0, "open": {"value" : 0}, "close": {"value" : 0}, "write": {"value" : 0}, "read": {"value" : 0}},
                                 "array": {"value" : 0, "length": {"value" : 0}, "concat": {"value" : 0}, "split": {"value" : 0}, "sort": {"value" : 0}, "pop": {"value" : 0}, "push": {"value" : 0}, "find": {"value" : 0}}},
        "maxIfDepth" : {"value" : 0},
        "maxLoopDepth" : {"value" : 2},
        "totalArraySize" : {"value" : 0},
        "maxArrayDim" : {"value" : 0}
       }

    return problem_tree

def get_version_tree():

	version_tree = {"basicIO" : {"value" : 2, "input" : {"value" : 1}, "output" : {"value" : 1}},
        "condition" : {"value" : 1, "if" : {"value" : 1, "ifOnly" : {"value" : 1}, "withElse" : {"value" : 0}}, "switch" : {"value" : 0}},
        "loop" : {"value" : 0, "single" : {"value" : 0, "for" : {"value" : 0}, "while" : {"value" : 0}},
                               "nested" : {"value" : 0, "forOnly" : {"value" : 0}, "whileOnly" : {"value" : 0}, "mixed" : {"value" : 0}}},
        "array" : {"value" : 0, "nonCharArray": {"value" : 0, "singleDim": {"value" : 0}, "multiDim": {"value" : 0}}, "charArray": {"value" : 0, "singleDim": {"value" : 0}, "multiDim": {"value" : 0}}},
        "function" : {"value" : 0, "recursion": {"value" : 0, "procedure": {"value" : 0}, "function": {"value" : 0}}, "notRecursion": {"value" : 0, "procedure": {"value" : 0}, "function": {"value" : 0}}},
        "class" : {"value" : 0, "inheritance": {"value" : 0, "constructor": {"value" : 0}, "noConstructor": {"value" : 0}}, "noInheritance": {"value" : 0, "constructor": {"value" : 0}, "noConstructor": {"value" : 0}}},
        "module" : {"value" : 0, "string": {"value" : 0, "length": {"value" : 0}, "concat": {"value" : 0}, "substr": {"value" : 0}, "replace": {"value" : 0}, "changeType": {"value" : 0}},
                                 "fileIO": {"value" : 0, "open": {"value" : 0}, "close": {"value" : 0}, "write": {"value" : 0}, "read": {"value" : 0}},
                                 "array": {"value" : 0, "length": {"value" : 0}, "concat": {"value" : 0}, "split": {"value" : 0}, "sort": {"value" : 0}, "pop": {"value" : 0}, "push": {"value" : 0}, "find": {"value" : 0}}},
        "maxIfDepth" : {"value" : 1},
        "maxLoopDepth" : {"value" : 0},
        "totalArraySize" : {"value" : 0},
        "maxArrayDim" : {"value" : 0}
       }

	return version_tree

def translate(skill):
    #a dictionary to convert dictionary terms to natural language terms
    conversion_list = {"basicIO": "Basic IO","basicIO_input": "Basic Input", "basicIO_output": "Basic Output",
                "condition": "Condition", "condition_if": "If", "condition_if_ifOnly": "If (Without else)", "condition_if_withElse": "If (With else)", "condition_switch": "Switch",
                "loop": "Loop", "loop_single": "Single Loop", "loop_single_for": "Single For-loop", "loop_single_while": "Single While-loop",
                "loop_nested": "Nested Loop", "loop_nested_forOnly": "Nested Loop (For Only)", "loop_nested_whileOnly": "Nested Loop (While Only)", "loop_nested_mixed": "Nested Loop (For + While)",
                "array": "Array", "array_nonCharArray": "Non-character Array", "array_charArray": "Character Array",
                "array_nonCharArray_singleDim": "Non-character Array (Single Dimension)", "array_nonCharArray_multiDim": "Non-character Array (Multi-Dimension)",
                "array_charArray_singleDim": "Character Array (Single Dimension)", "array_charArray_multiDim": "Character Array (Multi-Dimension)",
                "function": "Function/Procedure", "function_recursion": "Function/Procedure With Recursion", "function_notRecursion": "Function/Procedure Without Recursion",
                "function_recursion_procedure": "Procedure With Recursion", "function_recursion_function": "Function With Recursion",
                "function_notRecursion_procedure": "Procedure Without Recursion", "function_notRecursion_function": "Function Without Recursion",
                "class": "Class", "class_inheritance": "Class (With Inheritance)", "class_noInheritance": "Class (Without Inheritance)",
                "class_inheritance_constructor": "Class (With Inheritance and Constructor)", "class_inheritance_noConstructor": "Class (With Inheritance and Without Constructor)",
                "class_noInheritance_constructor": "Class (Without Inheritance and With Constructor)", "class_noInheritance_noConstructor": "Class (Without Inheritance and Constructor)",
                "module": "Module Function", "module_string": "Module Function (String)", "module_fileIO": "Module Function (File IO)", "module_array": "Module Function (Array)",
                "module_string_length": "String-Length", "module_string_concat": "String-Concatenate", "module_string_substr": "String-Substring",
                "module_string_replace": "String-Replace", "module_string_changeType": "String-Change Type", "module_fileIO_open": "FileIO-Open",
                "module_fileIO_close": "FileIO-Close", "module_fileIO_write": "FileIO-Write", "module_fileIO_read": "FileIO-Read",
                "module_array_length": "Array-Length", "module_array_concat": "Array-Concatenate", "module_array_split": "Array-Split",
                "module_array_sort": "Array-Sort", "module_array_pop": "Array-Pop", "module_array_push": "Array-Push", "module_array_find": "Array-Find",
                "maxIfDepth": "Maximum Depth of If", "maxLoopDepth": "Maximum Depth of Loop", "totalArraySize": "Total Array Size", "maxArrayDim": "Highest Array Dimension"}

    return conversion_list[skill]
