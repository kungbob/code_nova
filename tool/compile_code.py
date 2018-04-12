import sys
from io import StringIO
import contextlib
import traceback
import json
from subprocess import run, PIPE,Popen
from code_nova.settings import BASE_DIR
import os

# manage stdout
@contextlib.contextmanager
def stdoutIO(stdout=None):
	old_out = sys.stdout
	if stdout is None:
		stdout = StringIO()
	sys.stdout = stdout

	yield stdout
	sys.stdout = old_out

# manage stderr
@contextlib.contextmanager
def stderrIO(stderr=None):
    old = sys.stderr
    if stderr is None:
        stderr = StringIO()
    sys.stderr = stderr
    yield stderr
    sys.stderr = old

# def compile_code(code, exercise):
#
# 	test_case_list = json.loads(exercise.test_case)["test_case"]
# 	result_list = []
# 	overall_success = True
# 	passed_test_case = 0
#
# 	for test_case in test_case_list:
# 		with stdoutIO() as out:
# 			with stderrIO() as err:
# 				try:
# 					sys.argv = test_case["input"]
# 					# exec(codeio,{})
# 					exec(code,globals())
# 				except Exception as e:
#
# 					traceback.print_exc()
#
# 		output = out.getvalue()
# 		error = err.getvalue()
#
# 		if output == test_case["expect_output"]:
# 			success = True
# 			passed_test_case = passed_test_case + 1
# 		else:
# 			success = False
# 			overall_success = False
#             # this case is passed
#
# 		result = {"input":test_case["input"],"expect_output":test_case["expect_output"],"output":str(output),"error":str(error),"success":success}
# 		result_list.append(result)
#
# 	# print(result_list)
#
# 	result = {"result":result_list,"total_test_case":len(test_case_list),"passed_test_case":passed_test_case,"overall_success":overall_success}
#
# 	return result
#


def compile_code(code,exercise):

	url = os.path.join(BASE_DIR, "dumb.py")

	file = open(url, 'w')
	file.write(code)
	file.close()




	test_case_list = json.loads(exercise.test_case)["test_case"]


	result_list = []
	overall_success = True
	passed_test_case = 0

	for test_case in test_case_list:


		# print("testcase:"+str(test_case["input"]))
		p = Popen(['python',url], stdout=PIPE, stdin=PIPE, stderr=PIPE)
		output, error = p.communicate(input=test_case["input"].encode())
		output = output.decode("utf8").strip()
		error = error.decode("utf8").strip()

		if output == test_case["expect_output"]:
			success = True
			passed_test_case = passed_test_case + 1
		else:
			success = False
			overall_success = False
            # this case is passed

		result = {"input":test_case["input"],"expect_output":test_case["expect_output"],"output":str(output),"error":str(error),"success":success}
		result_list.append(result)

	# print(result_list)

	result = {"result":result_list,"total_test_case":len(test_case_list),"passed_test_case":passed_test_case,"overall_success":overall_success}

	print(result)

	return result
