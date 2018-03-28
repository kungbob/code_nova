# list must be same length
#
# Question need to have the average ability point required in the question
#
from scipy.spatial.distance import *
import operator
# from generate_user_database import generate_user_database
from student.models import Student
from exercise.models import Exercise
from cluster.models import Cluster
from user.models import User
from tool.tree import flatten
from tool.analyser import analyser
import json
import numpy as np

# seeker: user object
def find_helper(code,seeker,current_exercise):
	# seeker profile into dict

	try:
		version_tree = analyser(code)
		flatten_tree = flatten(version_tree)
		cluster_list = Cluster.objects.filter(exercise=current_exercise)
		for i in range(0, len(center)):
			center[i] = float(center[i])
		nearest_cluster_id = 0
		nearest_cluster_dis = euclidean(np.array(list(flatten_tree.values())),np.array(center))
		for cluster in cluster_list:

			center = cluster.center.split(',')

			for i in range(0, len(center)):
				center[i] = float(center[i])

			dist = euclidean(list(flatten_tree.values()),np.array(center))

			if nearest_cluster_dis > dist:
				nearest_cluster_id = cluster.id

		nearest_cluster_object = Cluster.objects.get(pk=nearest_cluster_id)
		compare_list = json.loads(nearest_cluster_object.necessary_skill)
		#######################################################################

		student_list = Student.objects.all()

		seeker_profile = seeker.profile_tree

		seeker_profile_json = json.loads(seeker_profile)
		seeker_profile_json_flatten = flatten(seeker_profile_json)
		print(seeker_profile_json)
		print(flatten(seeker_profile_json))

		seeker_ability_dict = jsontocompare(seeker_profile_json_flatten, compare_list)
		print(seeker_ability_dict)
		seeker_ability_list = list(seeker_ability_dict.values())
		print(seeker_ability_list)
		# print(my_json)
		# Compare value of two students' abilities
		dictance_dict = dict()
		for helper in student_list:
			if seeker.id == helper.id:
				continue
			else:
				helper_profile_json = json.loads(helper.profile_tree)
				helper_profile_json_flatten = flatten(helper_profile_json)
				helper_ability_dict = jsontocompare(helper_profile_json_flatten, compare_list)
				helper_ability_list = list(helper_ability_dict.values())
				distance = euclidean(seeker_ability_list, helper_ability_list)
				dictance_dict[helper.id] = distance
		sorted_distance = sorted(dictance_dict.items(), key=operator.itemgetter(1))
		call_list = call(sorted_distance, 10)
		return call_list
	except Exception as e:
		cluster_list = Cluster.objects.filter(exercise=current_exercise)
		max_cluster_id = 0
		max_cluster_count = 0

		nearest_cluster_id = cluster_list[0].id
		center = cluster_list[0].center.split(',')

		for i in range(0, len(center)):
			center[i] = float(center[i])

		for cluster in cluster_list:
			if max_cluster_count < cluster.data_count:
				max_cluster_id = cluster.id

		majority_cluster_object = Cluster.objects.get(pk=max_cluster_id)
		compare_list = json.loads(majority_cluster_object.necessary_skill)
		#######################################################################

		student_list = Student.objects.all()

		seeker_profile = seeker.profile_tree

		seeker_profile_json = json.loads(seeker_profile)
		seeker_profile_json_flatten = flatten(seeker_profile_json)
		print(seeker_profile_json)
		print(flatten(seeker_profile_json))

		seeker_ability_dict = jsontocompare(seeker_profile_json_flatten, compare_list)
		print(seeker_ability_dict)
		seeker_ability_list = list(seeker_ability_dict.values())
		print(seeker_ability_list)
		# print(my_json)
		# Compare value of two students' abilities
		dictance_dict = dict()
		for helper in student_list:

			# check if the helper is seeker himself and helper is online or not
			if seeker.id == helper.id or helper.user.reply_channel == "":
				continue
			else:
				helper_profile_json = json.loads(helper.profile_tree)
				helper_profile_json_flatten = flatten(helper_profile_json)
				helper_ability_dict = jsontocompare(helper_profile_json_flatten, compare_list)
				helper_ability_list = list(helper_ability_dict.values())
				distance = euclidean(seeker_ability_list, helper_ability_list)
				dictance_dict[helper.id] = distance
		sorted_distance = sorted(dictance_dict.items(), key=operator.itemgetter(1))
		call_list = call(sorted_distance, 10)
		return call_list








	# seeker_profile = flatten(my_json)
	#
	#
	# print(seeker_profile)


	# seeker_dict = users.get(seeker)
	#
	#
	#
	#
	# seeker_list = list(seeker_dict.values())
	# # Only first seven part is the ability, later part is the exercise_no
	# seeker_ability_list = seeker_list[0:7]
	#
	# dictance_dict = dict()
	# for helper in users:
	#     if helper == seeker:
	#         continue
	#     else:
	#         helper_dict = users.get(helper)
	#         # If helper does not finish this exercise before, skip
	#         if not helper_dict[current_exercise]:
	#             continue
	#         helper_list = list(helper_dict.values())
	#         helper_ability_list = helper_list[0:7]
	#         # Use Eculidean method
	#         distance = euclidean(seeker_ability_list, helper_ability_list)
	#         dictance_dict[helper] = distance
	# # If no one finish this exercise before, rerun seeking process:
	# if len(dictance_dict) == 0:
	#     for helper in users:
	#         if helper == seeker:
	#             continue
	#         else:
	#             helper_dict = users.get(helper)
	#             helper_list = list(helper_dict.values())
	#             helper_ability_list = helper_list[0:7]
	#             # Use Eculidean method
	#             distance = euclidean(seeker_ability_list, helper_ability_list)
	#             dictance_dict[helper] = distance
	# # In ascending order
	# sorted_distance = sorted(dictance_dict.items(), key=operator.itemgetter(1))
	# # Set return 10 users
	# call_list = call(sorted_distance, 10)
	# print(call_list)
	# return call_list

def jsontocompare(user_json, compare_list):
	compare_dict = dict()
	for item in compare_list:
		compare_dict[item] = user_json[item]
	return compare_dict

def call(helper_list, number):
	if len(helper_list) < number:
		call_list = helper_list
		id_list = [student[0] for student in call_list]
		return id_list
	else:
		call_list = helper_list[:number]
		id_list = [student[0] for student in call_list]
		number_list = [student[1] for student in call_list]
		return id_list

if __name__ == "__main__":
	# Value set for demo
	database = generate_user_database()
	seeker = "test_user_1"
	print("Seeker is: " + seeker)
	current_exercise = "01"
	print("Current exercise is:" + current_exercise)
	helper_list = find_helper(seeker, current_exercise, database)
