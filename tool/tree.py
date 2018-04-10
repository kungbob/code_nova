import collections

def get_empty_version_tree():

    version_tree = {"basicIO" : {"value" : 0, "input" : {"value" : 0}, "output" : {"value" : 0}},
         "condition" : {"value" : 0, "if" : {"value" : 0, "ifOnly" : {"value" : 0}, "withElse" : {"value" : 0}}, "switch" : {"value" : 0}},
         "loop" : {"value" : 0, "single" : {"value" : 0, "for" : {"value" : 0}, "while" : {"value" : 0}},
                                "nested" : {"value" : 0, "forOnly" : {"value" : 0}, "whileOnly" : {"value" : 0}, "mixed" : {"value" : 0}}},
         "array" : {"value" : 0, "nonCharArray": {"value" : 0, "singleDim": {"value" : 0}, "multiDim": {"value" : 0}}, "charArray": {"value" : 0, "singleDim": {"value" : 0}, "multiDim": {"value" : 0}}},
         "function" : {"value" : 0, "recursion": {"value" : 0, "procedure": {"value" : 0}, "function": {"value" : 0}}, "notRecursion": {"value" : 0, "procedure": {"value" : 0}, "function": {"value" : 0}}},
         "class" : {"value" : 0, "inheritance": {"value" : 0, "constructor": {"value" : 0}, "noConstructor": {"value" : 0}}, "noInheritance": {"value" : 0, "constructor": {"value" : 0}, "noConstructor": {"value" : 0}}},
         "lambda" : {"value" : 0},
         "comprehension" : {"value" : 0, "list" : {"value" : 0}, "set" : {"value" : 0}, "dict" : {"value" : 0}},
         "dataStructure" : {"value" : 0, "list" : {"value" : 0, "construct" : {"value" : 0}, "function" : {"value" : 0, "append" : {"value" : 0}, "extend" : {"value" : 0}, "insert" : {"value" : 0}, "remove" : {"value" : 0}, "pop" : {"value" : 0}, "clear" : {"value" : 0}, "count" : {"value" : 0}, "sort" : {"value" : 0}, "reverse" : {"value" : 0}}},
                                   "set" : {"value" : 0}, "dict" : {"value" : 0}, "tuple" : {"value" : 0}},
         "py-str" : {"value" : 0, "construct" : {"value" : 0}, "attrfunc" : {"value" : 0, "count" : {"value" : 0}, "find" : {"value" : 0}, "join" : {"value" : 0}, "partition" : {"value" : 0}, "replace" : {"value" : 0}, "split" : {"value" : 0}, "splitlines" : {"value" : 0}}},
         "py-buildin": {"value" : 0, "abs" : {"value" : 0}, "all" : {"value" : 0}, "any" : {"value" : 0}, "ascii" : {"value" : 0}, "bin" : {"value" : 0}, "bool" : {"value" : 0}, "bytearray" : {"value" : 0}, "bytes" : {"value" : 0}, "callable" : {"value" : 0}, "chr" : {"value" : 0},
                                     "classmethod" : {"value" : 0}, "compile" : {"value" : 0}, "complex" : {"value" : 0}, "delattr" : {"value" : 0}, "dir" : {"value" : 0}, "divmod" : {"value" : 0}, "enumerate" : {"value" : 0}, "eval" : {"value" : 0},
                                     "exec" : {"value" : 0}, "filter" : {"value" : 0}, "float" : {"value" : 0}, "format" : {"value" : 0}, "frozenset" : {"value" : 0}, "getattr" : {"value" : 0}, "globals" : {"value" : 0}, "hasattr" : {"value" : 0}, "hash" : {"value" : 0},
                                     "help" : {"value" : 0}, "hex" : {"value" : 0}, "id" : {"value" : 0}, "int" : {"value" : 0}, "isinstance" : {"value" : 0}, "issubclass" : {"value" : 0}, "iter" : {"value" : 0}, "len" : {"value" : 0},
                                     "locals" : {"value" : 0}, "map" : {"value" : 0}, "max" : {"value" : 0}, "memoryview" : {"value" : 0}, "min" : {"value" : 0}, "next" : {"value" : 0}, "object" : {"value" : 0}, "oct" : {"value" : 0}, "open" : {"value" : 0}, "ord" : {"value" : 0},
                                     "pow" : {"value" : 0}, "property" : {"value" : 0}, "range" : {"value" : 0}, "repr" : {"value" : 0}, "reversed" : {"value" : 0}, "round" : {"value" : 0}, "setattr" : {"value" : 0}, "slice" : {"value" : 0},
                                     "staticmethod" : {"value" : 0}, "sum" : {"value" : 0}, "super" : {"value" : 0}, "type" : {"value" : 0}, "vars" : {"value" : 0}, "zip" : {"value" : 0}, "__import__" : {"value" : 0}},
         "module" : {"value" : 0, "collections": {"value" : 0, "namedtuple()": {"value" : 0}, "deque": {"value" : 0}, "ChainMap": {"value" : 0}, "Counter": {"value" : 0}, "OrderedDict": {"value" : 0}, "defaultdict": {"value" : 0}, "UserDict": {"value" : 0}, "UserList": {"value" : 0}, "UserString": {"value" : 0}}},
         "maxIfDepth" : {"value" : 0},
         "maxLoopDepth" : {"value" : 0},
         "maxArraySize" : {"value" : 0},
         "maxArrayDim" : {"value" : 0}
    }

    return version_tree

def get_compare_list():
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
    'py-buildin_chr', 'py-buildin_classmethod', 'py-buildin_compile', 'py-buildin_complex', 'py-buildin_delattr',
    'py-buildin_dir', 'py-buildin_divmod', 'py-buildin_enumerate', 'py-buildin_eval', 'py-buildin_exec', 'py-buildin_filter',
    'py-buildin_float', 'py-buildin_format', 'py-buildin_frozenset', 'py-buildin_getattr', 'py-buildin_globals', 'py-buildin_hasattr',
    'py-buildin_hash', 'py-buildin_help', 'py-buildin_hex', 'py-buildin_id', 'py-buildin_int', 'py-buildin_isinstance',
    'py-buildin_issubclass', 'py-buildin_iter', 'py-buildin_len', 'py-buildin_locals', 'py-buildin_map', 'py-buildin_max',
    'py-buildin_memoryview', 'py-buildin_min', 'py-buildin_next', 'py-buildin_object', 'py-buildin_oct', 'py-buildin_open', 'py-buildin_ord',
    'py-buildin_pow', 'py-buildin_property', 'py-buildin_range', 'py-buildin_repr', 'py-buildin_reversed',
    'py-buildin_round', 'py-buildin_setattr', 'py-buildin_slice', 'py-buildin_staticmethod','py-buildin_sum', 'py-buildin_super', 'py-buildin_type', 'py-buildin_vars', 'py-buildin_zip',
    'py-buildin___import__', 'module_collections_namedtuple()', 'module_collections_deque', 'module_collections_ChainMap',
    'module_collections_Counter', 'module_collections_OrderedDict', 'module_collections_defaultdict', 'module_collections_UserDict',
    'module_collections_UserList', 'module_collections_UserString', ]
    return thingtocompare

def add_tree(tree,new_tree):

    if type(tree) == int:
        tree = tree + new_tree
        return tree

    for key,value in tree.items():
        # print("key:"+key+"  value:"+str(value))
        tree[key] = add_tree(tree[key],new_tree[key])

    return tree



def reduce_tree(tree):
    if type(tree) == int:
        if tree > 0 :
            return 1
        else:
            return 0

    for key,value in tree.items():
        # print("key:"+key+"  value:"+str(value))
        tree[key] = reduce_tree(tree[key])

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

def translate_tree(tree):

    new_tree = dict()
    for key,value in tree.items():
        if key == "value":
            new_tree[key] = tree[key]
        else:
            new_tree[translate2(key)] = translate_tree(tree[key])
    return new_tree

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
                'lambda': "Lambda Function", 'comprehension': "Comprehension", 'comprehension_list': "Comprehension (List)", 'comprehension_set': "Comprehension (Set)",
                'comprehension_dict': "Comprehension (Dict)", 'dataStructure': "Data Structure", 'dataStructure_list': "List",
                'dataStructure_list_construct': "List Construct", 'dataStructure_list_function': "List Function", 'dataStructure_list_function_append': "List-append",
                'dataStructure_list_function_extend': "List-extend", 'dataStructure_list_function_insert': "List-insert", 'dataStructure_list_function_remove': "List-remove",
                'dataStructure_list_function_pop': "List-pop", 'dataStructure_list_function_clear': "List-clear", 'dataStructure_list_function_count': "List-count",
                'dataStructure_list_function_sort': "List-sort", 'dataStructure_list_function_reverse': "List-reverse", 'dataStructure_set': "Set",
                'dataStructure_dict': "Dict", 'dataStructure_tuple': "Tuple", 'py-str': "String", 'py-str_construct': "String Construct",
                'py-str_attrfunc': "String Function", 'py-str_attrfunc_count': "String-count", 'py-str_attrfunc_find': "String-find",
                'py-str_attrfunc_join': "String-join", 'py-str_attrfunc_partition': "String-partition", 'py-str_attrfunc_replace': "String-replace",
                'py-str_attrfunc_split': "String-split", 'py-str_attrfunc_splitlines': "String-splitlines", 'py-buildin': "Built-in Function",
                'py-buildin_abs': "Builtin-abs", 'py-buildin_all': "Builtin-all", 'py-buildin_any': "Builtin-any", 'py-buildin_ascii': "Builtin-ascii",
                'py-buildin_bin': "Builtin-bin", 'py-buildin_bool': "Builtin-bool", 'py-buildin_bytearray': "Builtin-byteArray", 'py-buildin_bytes': "Builtin-bytes",
                'py-buildin_callable': "Builtin-callable", 'py-buildin_chr': "Builtin-chr", 'py-buildin_classmethod': "Builtin-classmethod",
                'py-buildin_compile': "Builtin-compile", 'py-buildin_complex': "Builtin-complex", 'py-buildin_delattr': "Builtin-delattr",
                'py-buildin_dict': "Builtin-dict", 'py-buildin_dir': "Builtin-dir", 'py-buildin_divmod': "Builtin-divmod", 'py-buildin_enumerate': "Builtin-enumerate",
                'py-buildin_eval': "Builtin-eval", 'py-buildin_exec': "Builtin-exec", 'py-buildin_filter': "Builtin-filter", 'py-buildin_float': "Builtin-float",
                'py-buildin_format': "Builtin-format", 'py-buildin_frozenset': "Builtin-frozenset", 'py-buildin_getattr': "Builtin-getattr", 'py-buildin_globals': "Builtin-globals",
                'py-buildin_hasattr': "Builtin-hasattr", 'py-buildin_hash': "Builtin-hash", 'py-buildin_help': "Builtin-help", 'py-buildin_hex': "Builtin-hex",
                'py-buildin_id': "Builtin-id", 'py-buildin_int': "Builtin-int", 'py-buildin_isinstance': "Builtin-isinstance",
                'py-buildin_issubclass': "Builtin-issubclass", 'py-buildin_iter': "Builtin-iter", 'py-buildin_len': "Builtin-len",
                'py-buildin_list': "Builtin-list", 'py-buildin_locals': "Builtin-locals", 'py-buildin_map': "Builtin-map", 'py-buildin_max': "Builtin-max",
                'py-buildin_memoryview': "Builtin-memoryview", 'py-buildin_min': "Builtin-min", 'py-buildin_next': "Builtin-next", 'py-buildin_object': "Builtin-object",
                'py-buildin_oct': "Builtin-oct", 'py-buildin_open': "Builtin-open", 'py-buildin_ord': "Builtin-ord", 'py-buildin_pow': "Builtin-pow",
                'py-buildin_property': "Builtin-property", 'py-buildin_range': "Builtin-range", 'py-buildin_repr': "Builtin-repr",
                'py-buildin_reversed': "Builtin-reversed", 'py-buildin_round': "Builtin-round", 'py-buildin_set': "Builtin-set", 'py-buildin_setattr': "Builtin-setattr",
                'py-buildin_slice': "Builtin-slice", 'py-buildin_staticmethod': "Builtin-staticmethod", 'py-buildin_str': "Builtin-str",
                'py-buildin_sum': "Builtin-sum", 'py-buildin_super': "Builtin-super", 'py-buildin_tuple': "Builtin-tuple", 'py-buildin_type': "Builtin-type",
                'py-buildin_vars': "Builtin-vars", 'py-buildin_zip': "Builtin-zip", 'py-buildin___import__': "Builtin-import", 'module': "Module",
                'module_collections': "Collections", 'module_collections_namedtuple()': "Collections-namedtuple", 'module_collections_deque': "Collections-deque",
                'module_collections_ChainMap': "Collections-chain map", 'module_collections_Counter': "Collections-counter", 'module_collections_OrderedDict': "Collections-ordered dict",
                'module_collections_defaultdict': "Collections-default dict", 'module_collections_UserDict': "Collections-user dict", 'module_collections_UserList': "Collections-user list",
                'module_collections_UserString': "Collections-user string", 'module_fileIO': "File IO", 'module_fileIO_open': "File IO-open", 'module_fileIO_close': "File IO-close",
                'module_fileIO_write': "File IO-write", 'module_fileIO_read': "File IO-read",
                "maxIfDepth": "Maximum Depth of If", "maxLoopDepth": "Maximum Depth of Loop", "maxArraySize": "Largest Array Size", "maxArrayDim": "Largest Array Dimension"}

    return conversion_list[skill]

def translate2(skill):
    conversion_list = {'basicIO': "Basic IO", 'input': "Input", 'output': "Output", 'condition': "Condition", 'if': "If", 'ifOnly': "Without Else",
                'withElse': "With Else", 'switch': "Switch", 'loop': "Loop", 'single': "Single Loop", 'for': "For Loop", 'while': "While Loop",
                'nested': "Nested Loop", 'forOnly': "For Only", 'whileOnly': "While Only", 'mixed': "Mixed", 'array': "Array",
                'nonCharArray': "Non-character Array", 'singleDim': "Single Dimension", 'multiDim': "Multi-Dimension", 'charArray': "Character Array",
                'function': "Function", 'recursion': "With Recursion", 'procedure': "Procedure", 'notRecursion': "Without Recursion",
                'class': "Class", 'inheritance': "With Inheritance", 'constructor': "With Constructor", 'noConstructor': "Without Constructor",
                'noInheritance': "Without Inheritance", 'lambda': "Lambda Function", 'comprehension': "Comprehension", 'list': "List",
                'set': "Set", 'dict': "Dict", 'dataStructure': "Data Structure", 'append': "Append", 'extend': "Extend", 'insert': "Insert",
                'remove': "Remove", 'pop': "Pop", 'clear': "Clear", 'count': "Count", 'sort': "Sort", 'reverse': "Reverse", 'tuple': "Tuple",
                'py-str': "String", 'construct': "Construction", 'attrfunc': "Attribution Function", 'count': "Count", 'find': "Find",
                'join': "Join", 'partition': "Partition", 'replace': "Replace", 'split': "Split", 'splitlines': "Splitlines", 'py-buildin': "Built-in Function",
                'abs': "abs", 'all': "all", 'any': "any", 'ascii': "ascii", 'bin': "bin", 'bool': "bool", 'bytearray': "bytearray", 'bytes': "bytes",
                'callable': "callable", 'chr': "chr", 'classmethod': "classmethod", 'compile': "compile", 'complex': "complex", 'delattr': "delattr",
                'dir': "dir", 'divmod': "divmod", 'enumerate': "enumerate", 'eval': "eval", 'exec': "exec", 'filter': "filter", 'float': "float",
                'format': "format", 'frozenset': "frozenset", 'getattr': "getattr", 'globals': "globals", 'hasattr': "hasattr", 'hash': "hash",
                'help': "help", 'hex': "hex", 'id': "id", 'int': "int", 'isinstance': "isinstance", 'issubclass': "issubclass", 'iter': "iter",
                'len': "len", 'locals': "locals", 'map': "map", 'max': "max", 'memoryview': "memoryview", 'min': "min", 'next': "next", 'object': "object",
                'oct': "oct", 'open': "open", 'ord': "ord", 'pow': "pow", 'property': "property", 'range': "range", 'repr': "repr", 'reversed': "reversed",
                'round': "round", 'setattr': "setattr", 'slice': "slice", 'staticmethod': "staticmethod", 'sum': "sum", 'super': "super", 'type': "type",
                'vars': "vars", 'zip': "zip", '__import__': "__import__", 'module': "Module", 'collections': "Collections",'namedtuple()': "namedtuple()",
                'deque': "Deque", 'ChainMap': "Chain Map", 'Counter': "Counter", 'OrderedDict': "Ordered Dict", 'defaultdict': "Default Dict",
                'UserDict': "User Dict", 'UserList': "User List", 'UserString': "User String", "maxIfDepth": "Maximum Depth of If",
                "maxLoopDepth": "Maximum Depth of Loop", "maxArraySize": "Largest Array Size", "maxArrayDim": "Largest Array Dimension"}

    return conversion_list[skill]
