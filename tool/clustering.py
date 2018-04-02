from tool.analyser import analyser
from tool.tree import flatten, get_empty_version_tree, flatten_self_define
from sklearn.decomposition import PCA
import numpy as np # linear algebra
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn import mixture
from matplotlib.colors import LogNorm
from sklearn import svm
import matplotlib.font_manager
from sklearn.cluster import KMeans, MeanShift, estimate_bandwidth

from version.models import Version


def run_kmeans(data_matrix):


	other_list = ["maxIfDepth", "maxLoopDepth", "maxArraySize", "maxArrayDim"]

	kmeans = KMeans(n_clusters=1, random_state=0).fit(data_matrix)
	min_error = kmeans.inertia_
	best_cluster_no = 1

	for i in range(2,4):
		kmeans = KMeans(n_clusters=i, random_state=0).fit(data_matrix)

		print("error in with no. "+str(i)+":"+str(kmeans.inertia_))
		if kmeans.inertia_ < min_error:
			best_cluster_no = i


	kmeans = KMeans(n_clusters=best_cluster_no, random_state=0).fit(data_matrix)
	label = kmeans.labels_
	center = kmeans.cluster_centers_


	best_cluster_no = len(np.unique(label))

	data_count = []
	data_list = []
	for i in range(0, best_cluster_no):
		data_count.append(0)
		data_list.append([])


	for i in range(0,len(data_matrix)):
		data_list[label[i]].append(data_matrix[i])
		data_count[label[i]] += 1

	skilltree_structure = list(flatten(get_empty_version_tree()).keys())
	cluster_list = []


	print(label)

	print(best_cluster_no)


	for cluster in range(0, best_cluster_no):
		skilltree = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


		print("cluster : " + str(cluster))
		print("data_list:"+str(data_list[cluster]))
		print("data_count:"+str(data_count[cluster]))

		necessary_skill = []
		redundant_skill = []
		other_count = []

		for i in other_list:
			other_count.append([])

		for data in data_list[cluster]:
			for i in range(0, len(data)):
				if data[i] > 0:
					skilltree[i] += 1

			for skill in [153,154,155,156]:
				other_count[skill - 153].append(data[skill])

		for i in range(0, len(skilltree)):
			if skilltree[i] >= data_count[cluster]*0.75 and skilltree_structure[i] not in other_list:
				necessary_skill.append(skilltree_structure[i])
			elif skilltree[i] <= data_count[cluster]*0.1 and skilltree_structure[i] not in other_list:
				redundant_skill.append(skilltree_structure[i])

		other_skill = []


		print("other_count:"+str(other_count))
		for i in range(0, len(other_list)):
			mode = max(set(other_count[i]), key=other_count[i].count)
			other_skill.append({"name": other_list[i], "mode": mode})

		cluster_list.append({"center": center[cluster], "data_count": data_count[cluster], "necessary_skill": necessary_skill,
			"redundant_skill": redundant_skill, "other_skill": other_skill, "character_skill": ""})


	common_feature = cluster_list[0]["necessary_skill"]
	for cluster in cluster_list:
		common_feature = list(set(cluster["necessary_skill"]).intersection(common_feature))

	for cluster in cluster_list:
		character_skill = list(cluster["necessary_skill"])
		for common in common_feature:
			character_skill.remove(common)
		cluster["character_skill"] = character_skill

	output = {"cluster_list": cluster_list, "label": label, "common_skill": common_feature}


	return output

def run_ms(data):

	scaler = StandardScaler().fit(data)
	standardized_data = scaler.transform(data)

	bandwidth = estimate_bandwidth(standardized_data, quantile=0.2, n_samples = 100)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(standardized_data)

	other_list = ["maxIfDepth", "maxLoopDepth", "maxArraySize", "maxArrayDim"]

	label = ms.labels_
	center = ms.cluster_centers_
	cluster_no = len(np.unique(label))

	data_count = []
	data_list = []
	for i in range(0, cluster_no):
		data_count.append(0)
		data_list.append([])


	for i in range(0,len(data_matrix)):
		data_list[label[i]].append(data_matrix[i])
		data_count[label[i]] += 1

	skilltree_structure = list(flatten(get_empty_version_tree()).keys())
	cluster_list = []


	for cluster in range(0, cluster_no):

		skilltree = []
		list_length = len(data_matrix[0])
		for i in range(0, list_length):
			skilltree.append(0)

		necessary_skill = []
		redundant_skill = []
		other_count = []

		for i in other_list:
			other_count.append([])

		for data in data_list[cluster]:
			for i in range(0, len(data)):
				if data[i] > 0:
					skilltree[i] += 1

			for skill in [list_length-4,list_length-3,list_length-2,list_length-1]:
				other_count[skill - list_length + 4].append(data[skill])

		for i in range(0, len(skilltree)):
			if skilltree[i] >= data_count[cluster]*0.75 and skilltree_structure[i] not in other_list:
				necessary_skill.append(skilltree_structure[i])
			elif skilltree[i] <= data_count[cluster]*0.1 and skilltree_structure[i] not in other_list:
				redundant_skill.append(skilltree_structure[i])

		other_skill = []


		for i in range(0, len(other_list)):
			mode = max(set(other_count[i]), key=other_count[i].count)
			other_skill.append({"name": other_list[i], "mode": mode})

		cluster_list.append({"center": center[cluster], "data_count": data_count[cluster], "necessary_skill": necessary_skill,
			"redundant_skill": redundant_skill, "other_skill": other_skill, "character_skill": ""})


	common_feature = cluster_list[0]["necessary_skill"]
	for cluster in cluster_list:
		common_feature = list(set(cluster["necessary_skill"]).intersection(common_feature))

	for cluster in cluster_list:
		character_skill = list(cluster["necessary_skill"])
		for common in common_feature:
			character_skill.remove(common)
		cluster["character_skill"] = character_skill

	output = {"cluster_list": cluster_list, "label": label, "common_skill": common_feature}


	return output
