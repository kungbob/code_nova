from tool.analyser import analyser
from tool.tree import flatten, get_empty_version_tree
from sklearn.decomposition import PCA
import numpy as np # linear algebra
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn import mixture
from matplotlib.colors import LogNorm
from sklearn import svm
import matplotlib.font_manager
from sklearn.cluster import KMeans

from version.models import Version

#pca = PCA(n_components = 2)
#newData = pca.fit_transform(data_matrix)


#plt.plot(newData[:, 0], newData[:, 1], 'o', color = 'blue', label='Normal code')
#plt.plot(newData[0, 0], newData[0, 1], 'o', color = 'green', label='Hard-coded')
#plt.legend(loc='upper right')
#plt.xlabel('x1')
#plt.ylabel('x2')
#plt.title('Version tree in 2D after PCA processing')
#plt.show()




#list of elements for comparison
#compare_list = ['basicIO_output', 'condition_if_ifOnly', 'condition_if_withElse', 'condition_switch', 'loop_single_for', 'loop_single_while',
#				'loop_nested_forOnly', 'loop_nested_whileOnly', 'loop_nested_mixed', 'array_nonCharArray_singleDim', 'array_nonCharArray_multiDim',
#				'array_charArray_singleDim', 'array_charArray_multiDim', 'function_recursion_procedure', 'function_recursion_function', 'function_notRecursion_procedure',
#				'function_notRecursion_function', 'class_inheritance_constructor', 'class_inheritance_noConstructor', 'class_noInheritance_constructor',
#				'class_noInheritance_noConstructor', 'module_string_length', 'module_string_concat', 'module_string_substr', 'module_string_replace',
#				'module_string_changeType', 'module_fileIO_open', 'module_fileIO_close', 'module_fileIO_write', 'module_fileIO_read', 'module_array_length',
#				'module_array_concat', 'module_array_split', 'module_array_sort', 'module_array_pop', 'module_array_push', 'module_array_find']


#compare_list_index = [2, 5, 6, 7, 10, 11, 12, 18, 19, 21, 22, 25, 26, 28, 29, 32, 33, 35, 36, 39, 40, 41, 42, 43, 45, 46, 47, 48, 50, 51, 52, 53 ,54 ,55, 56, 57, 58, 59, 60]

#lack = []
#redundance = []

#for i in compare_list_index:
#	if cluster_2_skilltree[i]/len(cluster_2) >= 0.7 and wrong_version_list[i] == 0:
#		lack.append(skilltree_structure[i])
#	elif cluster_2_skilltree[i]/len(cluster_2) <= 0.1 and wrong_version_list[i] > 0:
#		redundance.append(skilltree_structure[i])


#print("lacking element: ", lack)
#print("redundant element: ", redundance)

def run_kmeans(data_matrix):

	other_list = ["maxIfDepth", "maxLoopDepth", "totalArraySize", "maxArrayDim"]

	kmeans = KMeans(n_clusters=1, random_state=0).fit(data_matrix)
	min_error = kmeans.inertia_
	best_cluster_no = 1

	for i in range(2,4):
		kmeans = KMeans(n_clusters=i, random_state=0).fit(data_matrix)
		if kmeans.inertia_ < min_error:
			best_cluster_no = i

	kmeans = KMeans(n_clusters=best_cluster_no, random_state=0).fit(data_matrix)
	label = kmeans.labels_
	center = kmeans.cluster_centers_

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


	for cluster in range(0, best_cluster_no):
		skilltree = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		necessary_skill = []
		redundant_skill = []
		other_count = []

		for i in other_list:
			other_count.append([])

		for data in data_list[cluster]:
			for i in range(0, len(data)):
				if data[i] > 0:
					skilltree[i] += 1

			for skill in [57,58,59,60]:
				other_count[skill - 57].append(data[skill])

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
