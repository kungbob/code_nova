import ast, sys, json
from ast2json import ast2json
from tool.tree import get_empty_version_tree

def analyser(prog):
    def treeAnalyser(tree, parent, attr, ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar):
        # print ("Node Type: %s - %s" % (tree["_type"], str(allVar)))

        #if tree["_type"] == None:
        #    print ("Leave node is reached.")

        elif tree["_type"] == "Module":
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            
        elif tree["_type"] == "Interactive":
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Expression":
            treeAnalyser(tree["body"], tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "FunctionDef":
            if (tree["name"] == "__init__"):
                classList[0] = True
            functionName = tree["name"]
            funList = [False, False]
            if tree["returns"] != None:
                funList[0] = True
                treeAnalyser(tree["returns"], tree["_type"], "returns", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["decorator_list"]: 
                treeAnalyser(child, tree["_type"], "decorator_list", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            if funList == [False, False]:
                vtree["function"]["notRecursion"]["procedure"]["value"] += 1
            elif funList == [False, True]:
                vtree["function"]["recursion"]["procedure"]["value"] += 1
            elif funList == [True, False]:
                vtree["function"]["notRecursion"]["function"]["value"] += 1
            else:
                vtree["function"]["recursion"]["function"]["value"] += 1
            functionName = None

        elif tree["_type"] == "AsyncFunctionDef":
            if (tree["name"] == "__init__"):
                classList[0] = True
            functionName = tree["name"]
            funList = [False, False]
            if tree["returns"] != None:
                funList[0] = True
                treeAnalyser(tree["returns"], tree["_type"], "returns", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["decorator_list"]: 
                treeAnalyser(child, tree["_type"], "decorator_list", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            if funList == [False, False]:
                vtree["function"]["notRecursion"]["procedure"]["value"] += 1
            elif funList == [False, True]:
                vtree["function"]["recursion"]["procedure"]["value"] += 1
            elif funList == [True, False]:
                vtree["function"]["notRecursion"]["function"]["value"] += 1
            else:
                vtree["function"]["recursion"]["function"]["value"] += 1
            funList = [False, False]
            functionName = None

        elif tree["_type"] == "ClassDef":
            classNames.append(tree["name"])
            classList = [False, False]
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["bases"]: 
                treeAnalyser(child, tree["_type"], "bases", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["decorator_list"]: 
                treeAnalyser(child, tree["_type"], "decorator_list", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            if classList == [False, False]:
                vtree["class"]["noInheritance"]["noConstructor"]["value"] += 1
            elif classList == [False, True]:
                vtree["class"]["inheritance"]["noConstructor"]["value"] += 1
            elif classList == [True, False]:
                vtree["class"]["noInheritance"]["constructor"]["value"] += 1
            else:
                vtree["class"]["inheritance"]["constructor"]["value"] += 1
            #print (classList)
            functionName = None

        elif tree["_type"] == "Return":
            if functionName != None:
                funList[0] = True
            if tree["value"] != None:
                treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Delete":
            for child in tree["targets"]: 
                treeAnalyser(child, tree["_type"], "targets", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Assign":
            if (tree["targets"][0]["_type"] == "Name"):
                if (tree["value"]["_type"] == "Name" and tree["value"]["id"] in allVar):
                    nextAssignedVar = (tree["targets"][0]["id"], allVar[tree["value"]["id"]][0])
                    allVar[nextAssignedVar[0]] = (nextAssignedVar[1], allVar[tree["value"]["id"]][1], allVar[tree["value"]["id"]][2])
                else:
                    nextAssignedVar = (tree["targets"][0]["id"], findType(tree["value"]))
                    if (nextAssignedVar[1] == "list"):
                        allVar[nextAssignedVar[0]] = (nextAssignedVar[1], 1, 1)
                        if (vtree["maxArraySize"]["value"] < 1):
                            vtree["maxArraySize"]["value"] = 1
                        if (vtree["maxArrayDim"]["value"] < 1):
                            vtree["maxArrayDim"]["value"] = 1
                    else:
                        allVar[nextAssignedVar[0]] = (nextAssignedVar[1], 1, 0)

            for child in tree["targets"]: 
                treeAnalyser(child, tree["_type"], "targets", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "AugAssign":
            treeAnalyser(tree["target"], tree["_type"], "target", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "AnnAssign":
            treeAnalyser(tree["target"], tree["_type"], "target", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            treeAnalyser(tree["annotation"], tree["_type"], "annotation", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            if tree["value"] != None:
                treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "For":
            forDepth += 1
            if vtree["maxLoopDepth"]["value"] < forDepth + whileDepth:
                vtree["maxLoopDepth"]["value"] = forDepth + whileDepth;
            if loopList[0] < forDepth:
                loopList[0] = forDepth;

            if (forDepth == 1 and whileDepth == 0):
                loopList = [1, 0]
            treeAnalyser(tree["target"], tree["_type"], "target", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            treeAnalyser(tree["iter"], tree["_type"], "iter", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            if (forDepth == 1 and whileDepth == 0):
                updateLoop(loopList)

        elif tree["_type"] == "AsyncFor":
            forDepth += 1
            if vtree["maxLoopDepth"]["value"] < forDepth + whileDepth:
                vtree["maxLoopDepth"]["value"] = forDepth + whileDepth;
            if loopList[0] < forDepth:
                loopList[0] = forDepth;

            if (forDepth == 1 and whileDepth == 0):
                loopList = [1, 0]
            treeAnalyser(tree["target"], tree["_type"], "target", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            treeAnalyser(tree["iter"], tree["_type"], "iter", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            if (forDepth == 1 and whileDepth == 0):
                updateLoop(loopList)

        elif tree["_type"] == "While":
            whileDepth += 1
            if vtree["maxLoopDepth"]["value"] < forDepth + whileDepth:
                vtree["maxLoopDepth"]["value"] = forDepth + whileDepth;
            if loopList[1] < whileDepth:
                loopList[1] = whileDepth;

            if (forDepth == 0 and whileDepth == 1):
                loopList = [0, 1]
            treeAnalyser(tree["test"], tree["_type"], "test", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            if (forDepth == 0 and whileDepth == 1):
                updateLoop(loopList)

        elif tree["_type"] == "If":
            ifDepth += 1
            if vtree["maxIfDepth"]["value"] < ifDepth:
                vtree["maxIfDepth"]["value"] = ifDepth;
            if (tree["orelse"] == []):
                if (parent != "If" or attr != "orelse"):
                    vtree["condition"]["if"]["ifOnly"]["value"] += 1
            else:
                if (parent != "If" or attr != "orelse"):
                    vtree["condition"]["if"]["withElse"]["value"] += 1
            treeAnalyser(tree["test"], tree["_type"], "test", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["orelse"]: 
                treeAnalyser(child, tree["_type"], "orelse", ifDepth - 1, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "With":
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "AsyncWith":
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Raise":
            if tree["exc"] != None:
                treeAnalyser(tree["value"], tree["_type"], "exc", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            if tree["cause"] != None:
                treeAnalyser(tree["value"], tree["_type"], "cause", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Try":
            for child in tree["body"]: 
                treeAnalyser(child, tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["finalbody"]: 
                treeAnalyser(child, tree["_type"], "finalbody", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Assert":
            treeAnalyser(tree["test"], tree["_type"], "test", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            if tree["msg"] != None:
                treeAnalyser(tree["value"], tree["_type"], "msg", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
        
        elif tree["_type"] == "Import":
            for tname in tree["names"]:
                if tname["asname"] == None:
                    allVar[tname["name"]] = (tname["name"], 0, 0)
                else:
                    allVar[tname["asname"]] = (tname["name"], 0, 0)

        elif tree["_type"] == "ImportFrom":
            for tname in tree["names"]:
                if tname["asname"] == None:
                    allVar[tname["name"]] = (tree["module"] + "." + tname["name"], 0, 0)
                else:
                    allVar[tname["asname"]] = (tree["module"] + "." + tname["name"], 0, 0)

        #elif tree["_type"] == "Global":

        #elif tree["_type"] == "Nonlocal":

        elif tree["_type"] == "Expr":
            treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "BoolOp":
            for child in tree["values"]: 
                treeAnalyser(child, tree["_type"], "values", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "BinOp":
            treeAnalyser(tree["left"], tree["_type"], "left", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            treeAnalyser(tree["right"], tree["_type"], "right", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "UnaryOp":
            treeAnalyser(tree["operand"], tree["_type"], "operand", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Lambda":
            vtree["lambda"]["value"] += 1
            treeAnalyser(tree["body"], tree["_type"], "body", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        #elif tree["_type"] == "IfExp":

        elif tree["_type"] == "Dict":
            vtree["dataStructure"]["dict"]["value"] += 1
            for child in tree["keys"]: 
                treeAnalyser(child, tree["_type"], "keys", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["values"]: 
                treeAnalyser(child, tree["_type"], "values", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Set":
            vtree["dataStructure"]["set"]["value"] += 1
            for child in tree["elts"]: 
                treeAnalyser(child, tree["_type"], "elts", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "ListComp":
            vtree["comprehension"]["list"]["value"] += 1 # list comprehension
            vtree["dataStructure"]["list"]["construct"]["value"] += 1 # list comprehension is also a list
            treeAnalyser(tree["elt"], tree["_type"], "elt", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["generators"]:
                treeAnalyser(child, tree["_type"], "generators", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "SetComp":
            vtree["comprehension"]["set"]["value"] += 1 # set comprehension
            vtree["dataStructure"]["set"]["value"] += 1 # set comprehension is also a set
            treeAnalyser(tree["elt"], tree["_type"], "elt", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["generators"]:
                treeAnalyser(child, tree["_type"], "generators", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "DictComp":
            vtree["comprehension"]["dict"]["value"] += 1 # dict comprehension
            vtree["dataStructure"]["dict"]["value"] += 1 # dict comprehension is also a dict
            treeAnalyser(tree["key"], tree["_type"], "key", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["generators"]:
                treeAnalyser(child, tree["_type"], "generators", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "GeneratorExp":
            treeAnalyser(tree["elt"], tree["_type"], "elt", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["generators"]:
                treeAnalyser(child, tree["_type"], "generators", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Await":
            treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Yield":
            if tree["value"] != None:
                treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "YieldFrom":
            treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Compare":
            treeAnalyser(tree["left"], tree["_type"], "left", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["comparators"]: 
                treeAnalyser(child, tree["_type"], "comparators", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Call":
            treeAnalyser(tree["func"], tree["_type"], "func", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["args"]: 
                treeAnalyser(child, tree["_type"], "args", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Num":
            if (parent == "Assign"):
                allVar[nextAssignedVar[0]] = (nextAssignedVar[1], 1, 0)

        elif tree["_type"] == "Str":
            vtree["py-str"]["construct"]["value"] += 1
            if (parent == "Assign"):
                allVar[nextAssignedVar[0]] = (nextAssignedVar[1], 1, 0)

        elif tree["_type"] == "FormattedValue":
            treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "JoinedStr":
            for child in tree["values"]: 
                treeAnalyser(child, tree["_type"], "values", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        #elif tree["_type"] == "Bytes":

        #elif tree["_type"] == "NameConstant":

        #elif tree["_type"] == "Ellipsis":

        #elif tree["_type"] == "Constant":

        elif tree["_type"] == "Attribute":
            if (tree["attr"] in vtree["dataStructure"]["list"]["function"]):
                if (tree["value"]["_type"] == "List"):
                    vtree["dataStructure"]["list"]["function"][tree["attr"]]["value"] += 1
                elif (tree["value"]["_type"] == "Name" and tree["value"]["id"] in allVar):
                    if (allVar[tree["value"]["id"]][0] == "list"):
                        vtree["dataStructure"]["list"]["function"][tree["attr"]]["value"] += 1

            if (tree["attr"] in vtree["py-str"]["attrfunc"]):
                if (tree["value"]["_type"] == "Str"):
                    vtree["py-str"]["attrfunc"][tree["attr"]]["value"] += 1
                elif (tree["value"]["_type"] == "Name" and tree["value"]["id"] in allVar):
                    if (allVar[tree["value"]["id"]][0] == "string"):
                        vtree["py-str"]["attrfunc"][tree["attr"]]["value"] += 1
                elif (tree["value"]["_type"] == "Call"):
                    if (tree["value"]["func"]["_type"] == "Name"):
                        if (tree["value"]["func"]["id"] == "input"):
                            vtree["py-str"]["attrfunc"][tree["attr"]]["value"] += 1

            if (tree["value"]["_type"] == "Name"):
                 if (tree["value"]["id"] in allVar):
                    if (allVar[tree["value"]["id"]][0] in vtree["module"]):
                        if (tree["attr"] in vtree["module"][allVar[tree["value"]["id"]][0]]):
                            vtree["module"][allVar[tree["value"]["id"]][0]][tree["attr"]]["value"] += 1

            treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Subscript":
            treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            treeAnalyser(tree["slice"], tree["_type"], "slice", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Starred":
            treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Name":
            if tree["id"] in vtree["py-buildin"] and tree["id"] != "value":
                if tree["id"] == "sorted":
                    vtree["dataStructure"]["list"]["function"]["sort"]["value"] += 1 # assume that sorted() used in list because this is a simplified tree
                else:
                   vtree["py-buildin"][tree["id"]]["value"] += 1

            if (tree["id"] in allVar):
                checkModuleFun(allVar[tree["id"]][0])

            if tree["id"] == "range" or tree["id"] == "list": # range( ) returns a list
                vtree["dataStructure"]["list"]["construct"]["value"] += 1
            elif tree["id"] == "dict":
                vtree["dataStructure"]["dict"]["value"] += 1
            elif tree["id"] == "set":
                vtree["dataStructure"]["set"]["value"] += 1
            elif tree["id"] == "input" or tree["id"] == "str": # input( ) returns a string
                vtree["py-str"]["construct"]["value"] += 1
            elif tree["id"] == "tuple":
                vtree["dataStructure"]["tuple"]["value"] += 1

            if tree["id"] == "input":
                vtree["basicIO"]["input"]["value"] += 1
            elif tree["id"] == "print":
                vtree["basicIO"]["output"]["value"] += 1
            elif (tree["id"] == functionName and parent == "Call" and attr == "func"):
                funList[1] = True
            elif (tree["id"] in classNames and parent == "ClassDef" and attr == "bases"):
                classList[1] = True

        elif tree["_type"] == "List":
            vtree["dataStructure"]["list"]["construct"]["value"] += 1
            size, dim = calculatelistSize(tree["elts"], allVar)
            if (nextAssignedVar[0] != None):
                allVar[nextAssignedVar[0]] = (nextAssignedVar[1], size, dim)
            if (vtree["maxArraySize"]["value"] < size):
                vtree["maxArraySize"]["value"] = size
            if (vtree["maxArrayDim"]["value"] < dim):
                vtree["maxArrayDim"]["value"] = dim
            for child in tree["elts"]: 
                treeAnalyser(child, tree["_type"], "elts", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Tuple":
            vtree["dataStructure"]["tuple"]["value"] += 1
            for child in tree["elts"]: 
                treeAnalyser(child, tree["_type"], "elts", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Slice":
            if tree["lower"] != None:
                treeAnalyser(tree["lower"], tree["_type"], "lower", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            if tree["upper"] != None:
                treeAnalyser(tree["upper"], tree["_type"], "upper", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            if tree["step"] != None:
                treeAnalyser(tree["step"], tree["_type"], "step", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "ExtSlice":
            for child in tree["dims"]: 
                treeAnalyser(child, tree["_type"], "dims", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "Index":
            treeAnalyser(tree["value"], tree["_type"], "value", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

        elif tree["_type"] == "comprehension":
            treeAnalyser(tree["target"], tree["_type"], "target", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            treeAnalyser(tree["iter"], tree["_type"], "iter", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)
            for child in tree["ifs"]:
                treeAnalyser(child, tree["_type"], "ifs", ifDepth, forDepth, whileDepth, loopList, functionName, funList, classNames, classList, nextAssignedVar, allVar)

    def updateLoop(loopList):
        if (loopList[1] == 0):
            if loopList[0] == 1:
                vtree["loop"]["single"]["for"]["value"] += 1
            elif loopList[0] > 1:
                vtree["loop"]["nested"]["forOnly"]["value"] += 1
        elif (loopList[0] == 0):
            if loopList[1] == 1:
                vtree["loop"]["single"]["while"]["value"] += 1
            elif loopList[1] > 1:
                vtree["loop"]["nested"]["whileOnly"]["value"] += 1
        else:
            vtree["loop"]["nested"]["mixed"]["value"] += 1

    def findType(treevalue):
        # For simplicity, it will return one of the following types: "number", "string", "list", "dict", "set", "tuple", "byte"
        if treevalue["_type"] == "BinOp":
            t1 = findType(treevalue["left"])
            t2 = findType(treevalue["right"])
            if (t1 == "string" and (t2 == "string" or t2 == "number")):
                return "string"
            elif ((t1 == "string" or t1 == "number") and t2 == "string"):
                return "string"
            else:
                return t1 # t1 and t2 are expected to have the same type because boolop is either "And" or "Or"

        elif treevalue["_type"] == "UnaryOp":
            return findType(treevalue["operand"])

        elif treevalue["_type"] == "Lambda":
            return findType(treevalue["body"])

        # elif treevalue["_type"] == "IfExp":

        elif treevalue["_type"] == "Dict":
            return "dict"

        elif treevalue["_type"] == "Set":
            return "set"

        elif treevalue["_type"] == "ListComp":
            return "list"

        elif treevalue["_type"] == "SetComp":
            return "set"

        elif treevalue["_type"] == "DictComp":
            return "dict"

        elif treevalue["_type"] == "GeneratorExp":
            return findType(treevalue["elt"])

        elif treevalue["_type"] == "Await":
            return findType(treevalue["value"])

        elif treevalue["_type"] == "Yield":
            if treevalue["value"] != None:
                return findType(treevalue["value"])
            else:
                return "number"

        elif treevalue["_type"] == "YieldFrom":
            return findType(treevalue["value"])

        elif treevalue["_type"] == "Compare":
            return findType(treevalue["left"])

        elif treevalue["_type"] == "Call":
            if (treevalue["func"]["_type"] == "Name" and treevalue["func"]["id"] == "range"):
                return "list" # e.g. range(5) is eqv. to [0, 1, 2, 3, 4]
            elif (treevalue["func"]["_type"] == "Name" and treevalue["func"]["id"] == "input"):
                return "string" # e.g. input( ) returns to a string by reading a line
            else:
                return findType(treevalue["func"])

        elif treevalue["_type"] == "Num":
            return "number"

        elif treevalue["_type"] == "Str":
            return "string"

        elif treevalue["_type"] == "FormattedValue":
            return findType(treevalue["value"])

        elif treevalue["_type"] == "JoinedStr":
            return "string"

        elif treevalue["_type"] == "Bytes":
            return "byte"

        # elif treevalue["_type"] == "NameConstant":

        # elif treevalue["_type"] == "Ellipsis":

        # elif treevalue["_type"] == "Constant":

        elif treevalue["_type"] == "Attribute":
            return findType(treevalue["value"])

        elif treevalue["_type"] == "Subscript":
            return findType(treevalue["value"])

        elif treevalue["_type"] == "Starred":
            return findType(treevalue["value"])

        elif treevalue["_type"] == "Name":
            if treevalue["id"] == "byte":
                return "byte"
            elif treevalue["id"] == "dict":
                return "dict"
            elif treevalue["id"] == "list":
                return "list"
            elif treevalue["id"] == "set":
                return "set"
            elif treevalue["id"] == "str":
                return "string"
            elif treevalue["id"] == "tuple":
                return "tuple"
            else:
                return "number"

        elif treevalue["_type"] == "List":
            return "list"

        elif treevalue["_type"] == "Tuple":
            return "tuple"

        else:
            return "number"

    def calculatelistSize(elts, allVar):
        size = 0
        dim = 0
        for child in elts:
            if (child["_type"] == "List"):
                s, d = calculatelistSize(child["elts"], allVar)
                size += s
                if (dim < d):
                    dim = d
            elif (child["_type"] != "Name"):
                size += 1
            elif (child["id"] in allVar):
                if (allVar[child["id"]][0] == "list"):
                    size += allVar[child["id"]][1]
                    if (dim < allVar[child["id"]][2]):
                        dim = allVar[child["id"]][2]
                else:
                    size += 1
            else:
                size += 1
        return size, (dim + 1)

    def checkModuleFun(id):
        ids = id.split(".")
        if (len(ids) == 2):
            if (ids[0] in vtree["module"]):
                if (ids[1] in vtree["module"][ids[0]]):
                    vtree["module"][ids[0]][ids[1]]["value"] += 1

    def parentValue(tree):
        if len(tree) > 1:
            sum = 0
            for child in tree:
                if child != "value":
                    sum += parentValue(tree[child])
            tree["value"] = sum
        return tree["value"]

    vtree = get_empty_version_tree()
    
    prog2 = prog.replace("else:", "elif True:")

    try:
        astree = ast.parse(prog2)                  # ast class defined in Python (Ref: Python Doc 32.2)
    except:
        astree = ast.parse(prog)

    jsonstr = ast2json(astree)                   # convert ast to json string
    result = json.dumps(jsonstr, indent = 4)   # json string with pretty indentation

    treeAnalyser(jsonstr, None, None, 0, 0, 0, [0, 0], None, [False, False], [], [False, False], (None, None), {})

    for child in vtree:
        vtree[child]['value'] = parentValue(vtree[child])

    return vtree
