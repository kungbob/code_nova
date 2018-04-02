import ast, sys, json
from ast2json import ast2json
from tree import get_empty_version_tree

def analyser(prog):
    def treeAnalyser(tree, parent, attr, ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList):
        #print ('Node Type: %s' % tree['_type'])

        #if tree['_type'] == None:
            #print ('Leave node is reached.')

        if tree['_type'] == 'Module':
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Interactive':
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Expression':
            treeAnalyser(tree['body'], tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'FunctionDef':
            if (tree['name'] == '__init__'):
                classList[0] = True
            functionName = tree['name']
            funList = [False, False]
            if tree['returns'] != None:
                funList[0] = True
                treeAnalyser(tree['returns'], tree['_type'], 'returns', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['decorator_list']:
                treeAnalyser(child, tree['_type'], 'decorator_list', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            if funList == [False, False]:
                vtree['function']['notRecursion']['procedure']['value'] += 1
            elif funList == [False, True]:
                vtree['function']['recursion']['procedure']['value'] += 1
            elif funList == [True, False]:
                vtree['function']['notRecursion']['function']['value'] += 1
            else:
                vtree['function']['recursion']['function']['value'] += 1
            functionName = None

        elif tree['_type'] == 'AsyncFunctionDef':
            if (tree['name'] == '__init__'):
                classList[0] = True
            functionName = tree['name']
            funList = [False, False]
            if tree['returns'] != None:
                funList[0] = True
                treeAnalyser(tree['returns'], tree['_type'], 'returns', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['decorator_list']:
                treeAnalyser(child, tree['_type'], 'decorator_list', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            if funList == [False, False]:
                vtree['function']['notRecursion']['procedure']['value'] += 1
            elif funList == [False, True]:
                vtree['function']['recursion']['procedure']['value'] += 1
            elif funList == [True, False]:
                vtree['function']['notRecursion']['function']['value'] += 1
            else:
                vtree['function']['recursion']['function']['value'] += 1
            funList = [False, False]
            functionName = None

        elif tree['_type'] == 'ClassDef':
            classNames.append(tree['name'])
            classList = [False, False]
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['bases']:
                treeAnalyser(child, tree['_type'], 'bases', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['decorator_list']:
                treeAnalyser(child, tree['_type'], 'decorator_list', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            if classList == [False, False]:
                vtree['class']['noInheritance']['noConstructor']['value'] += 1
            elif classList == [False, True]:
                vtree['class']['inheritance']['noConstructor']['value'] += 1
            elif classList == [True, False]:
                vtree['class']['noInheritance']['constructor']['value'] += 1
            else:
                vtree['class']['inheritance']['constructor']['value'] += 1
            functionName = None

        elif tree['_type'] == 'Return':
            if functionName != None:
                funList[0] = True
            if tree['value'] != None:
                treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Delete':
            for child in tree['targets']:
                treeAnalyser(child, tree['_type'], 'targets', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Assign':
            for child in tree['targets']:
                treeAnalyser(child, tree['_type'], 'targets', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'AugAssign':
            treeAnalyser(tree['target'], tree['_type'], 'target', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'AnnAssign':
            treeAnalyser(tree['target'], tree['_type'], 'target', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            treeAnalyser(tree['annotation'], tree['_type'], 'annotation', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            if tree['value'] != None:
                treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'For':
            forDepth += 1
            if vtree['maxLoopDepth']['value'] < forDepth + whileDepth:
                vtree['maxLoopDepth']['value'] = forDepth + whileDepth;
            if loopList[0] < forDepth:
                loopList[0] = forDepth;

            if (forDepth == 1 and whileDepth == 0):
                loopList = [1, 0]
            treeAnalyser(tree['target'], tree['_type'], 'target', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            treeAnalyser(tree['iter'], tree['_type'], 'iter', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            if (forDepth == 1 and whileDepth == 0):
                updateLoop(loopList)

        elif tree['_type'] == 'AsyncFor':
            forDepth += 1
            if vtree['maxLoopDepth']['value'] < forDepth + whileDepth:
                vtree['maxLoopDepth']['value'] = forDepth + whileDepth;
            if loopList[0] < forDepth:
                loopList[0] = forDepth;

            if (forDepth == 1 and whileDepth == 0):
                loopList = [1, 0]
            treeAnalyser(tree['target'], tree['_type'], 'target', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            treeAnalyser(tree['iter'], tree['_type'], 'iter', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            if (forDepth == 1 and whileDepth == 0):
                updateLoop(loopList)

        elif tree['_type'] == 'While':
            whileDepth += 1
            if vtree['maxLoopDepth']['value'] < forDepth + whileDepth:
                vtree['maxLoopDepth']['value'] = forDepth + whileDepth;
            if loopList[1] < whileDepth:
                loopList[1] = whileDepth;

            if (forDepth == 0 and whileDepth == 1):
                loopList = [0, 1]
            treeAnalyser(tree['test'], tree['_type'], 'test', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            if (forDepth == 0 and whileDepth == 1):
                updateLoop(loopList)

        elif tree['_type'] == 'If':
            ifDepth += 1
            if vtree['maxIfDepth']['value'] < ifDepth:
                vtree['maxIfDepth']['value'] = ifDepth;
            if (tree['orelse'] == []):
                if (parent != 'If' or attr != 'orelse'):
                    vtree['condition']['if']['ifOnly']['value'] += 1
            else:
                if (parent != 'If' or attr != 'orelse'):
                    vtree['condition']['if']['withElse']['value'] += 1
            treeAnalyser(tree['test'], tree['_type'], 'test', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['orelse']:
                treeAnalyser(child, tree['_type'], 'orelse', ifDepth - 1, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'With':
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'AsyncWith':
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Raise':
            if tree['exc'] != None:
                treeAnalyser(tree['value'], tree['_type'], 'exc', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            if tree['cause'] != None:
                treeAnalyser(tree['value'], tree['_type'], 'cause', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Try':
            for child in tree['body']:
                treeAnalyser(child, tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['finalbody']:
                treeAnalyser(child, tree['_type'], 'finalbody', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Assert':
            treeAnalyser(tree['test'], tree['_type'], 'test', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            if tree['msg'] != None:
                treeAnalyser(tree['value'], tree['_type'], 'msg', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        #elif tree['_type'] == 'Import':

        #elif tree['_type'] == 'ImportFrom':

        #elif tree['_type'] == 'Global':

        #elif tree['_type'] == 'Nonlocal':

        elif tree['_type'] == 'Expr':
            treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'BoolOp':
            for child in tree['values']:
                treeAnalyser(child, tree['_type'], 'values', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'BinOp':
            treeAnalyser(tree['left'], tree['_type'], 'left', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            treeAnalyser(tree['right'], tree['_type'], 'right', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'UnaryOp':
            treeAnalyser(tree['operand'], tree['_type'], 'operand', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Lambda':
            treeAnalyser(tree['body'], tree['_type'], 'body', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        #elif tree['_type'] == 'IfExp':

        elif tree['_type'] == 'Dict':
            for child in tree['keys']:
                treeAnalyser(child, tree['_type'], 'keys', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['values']:
                treeAnalyser(child, tree['_type'], 'values', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Set':
            for child in tree['elts']:
                treeAnalyser(child, tree['_type'], 'elts', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Set':
            for child in tree['elts']:
                treeAnalyser(child, tree['_type'], 'elts', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'ListComp':
            treeAnalyser(tree['elt'], tree['_type'], 'elt', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'SetComp':
            treeAnalyser(tree['elt'], tree['_type'], 'elt', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'DictComp':
            treeAnalyser(tree['key'], tree['_type'], 'key', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'GeneratorExp':
            treeAnalyser(tree['elt'], tree['_type'], 'elt', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Await':
            treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Yield':
            if tree['value'] != None:
                treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'YieldFrom':
            treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Compare':
            treeAnalyser(tree['left'], tree['_type'], 'left', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['comparators']:
                treeAnalyser(child, tree['_type'], 'comparators', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Call':
            treeAnalyser(tree['func'], tree['_type'], 'func', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)
            for child in tree['args']:
                treeAnalyser(child, tree['_type'], 'args', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        #elif tree['_type'] == 'Num':

        #elif tree['_type'] == 'Str':

        elif tree['_type'] == 'FormattedValue':
            treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'JoinedStr':
            for child in tree['values']:
                treeAnalyser(child, tree['_type'], 'values', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        #elif tree['_type'] == 'Bytes':

        #elif tree['_type'] == 'NameConstant':

        #elif tree['_type'] == 'Ellipsis':

        #elif tree['_type'] == 'Constant':

        elif tree['_type'] == 'Attribute':
            treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Subscript':
            treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Starred':
            treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Name':
            if tree['id'] == 'input':
                vtree['basicIO']['input']['value'] += 1
            elif tree['id'] == 'print':
                vtree['basicIO']['output']['value'] += 1
            elif (tree['id'] == functionName and parent == 'Call' and attr == 'func'):
                funList[1] = True
            elif (tree['id'] in classNames and parent == 'ClassDef' and attr == 'bases'):
                classList[1] = True

        elif tree['_type'] == 'FormattedValue':
            treeAnalyser(tree['value'], tree['_type'], 'value', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'List':
            for child in tree['elts']:
                treeAnalyser(child, tree['_type'], 'elts', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

        elif tree['_type'] == 'Tuple':
            for child in tree['elts']:
                treeAnalyser(child, tree['_type'], 'elts', ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList)

    def updateLoop(loopList):
        if (loopList[1] == 0):
            if loopList[0] == 1:
                vtree['loop']['single']['for']['value'] += 1
            elif loopList[0] > 1:
                vtree['loop']['nested']['forOnly']['value'] += 1
        elif (loopList[0] == 0):
            if loopList[1] == 1:
                vtree['loop']['single']['while']['value'] += 1
            elif loopList[1] > 1:
                vtree['loop']['nested']['whileOnly']['value'] += 1
        else:
            vtree['loop']['nested']['mixed']['value'] += 1

    def parentValue(tree):
        if len(tree) > 1:
            sum = 0
            for child in tree:
                if child != 'value':
                    sum += parentValue(tree[child])
            tree['value'] = sum
        return tree['value']


    vtree = get_empty_version_tree()

    prog = prog.replace("else:", "elif True:")

    astree = ast.parse(prog)                  # ast class defined in Python (Ref: Python Doc 32.2)
    jsonstr = ast2json(astree)                   # convert ast to json string
    result = json.dumps(jsonstr, indent = 4)   # json string with pretty indentation
    #print (result)

    treeAnalyser(jsonstr, None, None, 0, 0, 0, [0, 0], None, [False, False], [], [False, False])

    for child in vtree:
        vtree[child]['value'] = parentValue(vtree[child])

    print (vtree)

    return vtree
