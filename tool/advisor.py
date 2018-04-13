from tool.tree import  flatten, translate, get_empty_version_tree,get_compare_list
from tool.analyser import analyser
from scipy.spatial import distance
from cluster.models import Cluster
from exercise.models import Exercise
from version.models import Version
import numpy as np # linear algebra
import json
from sklearn.preprocessing import StandardScaler


def advisor(ex_id, version_tree):

	exercise = Exercise.objects.get(pk=ex_id)

	wanted_list = json.loads(exercise.common_skill)



	unwanted_list = []
	for i in list(flatten(get_empty_version_tree()).keys()):
		if i not in wanted_list:
			unwanted_list.append(i)

	flatten_tree = flatten(version_tree)
	for i in unwanted_list:
		flatten_tree.pop(i, None)

	original_tree = flatten(version_tree)

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
	compare_list = get_compare_list()

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

		if int(max_cluster_count) < int(cluster.data_count):
			# print("cluster:"+str(cluster.id)+ "count"+str(cluster.data_count))
			max_cluster_id = cluster.id
			max_cluster_count = cluster.data_count

		center = cluster.center.split(',')
		for i in range(0, len(center)):
			center[i] = float(center[i])

		dist = distance.euclidean(standardized_data,np.array(center))

		if nearest_cluster_dis > dist:
			nearest_cluster_id = cluster.id
			nearest_cluster_dis = dist

		for skill in necessary_skill_list:
			if flatten_tree[skill] == 0 and skill in compare_list:
				lacking.append(translate(skill))

		for skill in redundant_skill_list:
			if original_tree[skill] > 0 and skill in compare_list:
				redundance.append(translate(skill))

		for skill in character_skill_list:
			if skill in compare_list:
				character.append(translate(skill))

		for skill in other_skill_list:
			if flatten_tree[skill["name"]] != skill["mode"] and (skill["name"] != "MaxArraySize" or skill["mode"] >= 5):

		advice_list.append({"cluster_id": cluster.id,"data_count":cluster.data_count,"character_skill":character,"lacking": lacking, "redundance": redundance, "other_skill": others})

	output = {"max_cluster_id": max_cluster_id, "nearest_cluster_id": nearest_cluster_id, "advice_list": advice_list}

	return output
