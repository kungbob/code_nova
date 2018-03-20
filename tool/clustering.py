from analyser import analyser
from tree import flatten
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
from advisor import advisor

tri_1 = """
n = int(input())
if n == 1:
	print ('*')
elif n == 2:
	print ('*')
	print ('**')
elif n == 3:
	print ('*')
	print ('**')
	print ('***')
elif n == 4:
	print ('*')
	print ('**')
	print ('***')
	print ('****')
elif n == 5:
	print ('*')
	print ('**')
	print ('***')
	print ('****')
	print ('*****')
elif n == 6:
	print ('*')
	print ('**')
	print ('***')
	print ('****')
	print ('*****')
	print ('******')
elif n == 7:
	print ('*')
	print ('**')
	print ('***')
	print ('****')
	print ('*****')
	print ('******')
	print ('*******')
elif n == 8:
	print ('*')
	print ('**')
	print ('***')
	print ('****')
	print ('*****')
	print ('******')
	print ('*******')
	print ('********')
elif n == 9:
	print ('*')
	print ('**')
	print ('***')
	print ('****')
	print ('*****')
	print ('******')
	print ('*******')
	print ('********')
	print ('*********')
else:
	print ('*')
	print ('**')
	print ('***')
	print ('****')
	print ('*****')
	print ('******')
	print ('*******')
	print ('********')
	print ('*********')
	print ('**********')
"""

tri_2 = """
n = int(input())
for i in range(n):
	for j in range(i + 1):
		print ('*', end = "")
	print()
"""

tri_3 = """
n = int(input())
output = ""
for i in range(n):
	output += "*"
	print(output)
"""

tri_4 = """
def printStr(x):
	for j in range(x + 1):
		print ('*', end = "")

n = int(input())
for i in range(n):
	printStr (i);
	print()
"""

tri_5 = """
def printStr(x):
	if x >= 0:
		print ('*', end = "")
		printStr(x - 1)

n = int(input())
for i in range(n):
	printStr (i);
	print()
"""

tri_6 = """
n = int(input())
for i in range(n):
	for j in range(n):
		if (i >= j):
			print ('*', end = "")
	print()
"""

tri_7 = """
n = int(input())
i = 0
while i < n:
	j = 0
	while j <= i:
		print ('*', end = "")
		j += 1
	print()
	i = i + 1
"""

tri_8 = """
n = int(input())
i = 0
while i < n:
	for j in range(i + 1):
		print ('*', end = "")
	print()
	i = i + 1
"""

tri_9 = """
n = int(input())
for i in range(n):
	j = 0
	while j <= i:
		print ('*', end = "")
		j += 1
	print()
"""

tri_10 = """
n = int(input())
for i in range(n):
	for j in range(i):
		print ('*', end = "")
	print('*')
"""

tri_11 = """
n = int(input())
for i in range(n):
	print('*' * (i + 1))
"""

tri_12 = """
n = int(input())
for i in range(n):
	output = ""
	for j in range(i + 1):
		output += '*'
	print(output)
"""

tri_13 = """
n = int(input())
for i in range(n):
	for j in range(i + 1):
		print('*', end="")
	print()
"""

tri_14 = """
n = int(input())
i = 0
while i < n:
	for j in range(i + 1):
		print ('*', end = "")
	print()
	i = i + 1
"""

tri_15 = """
n = int(input())
for i in range(n):
	j = 0
	while j <= i:
		print ('*', end = "")
		j += 1
	print()
"""

tri_16 = """
n = int(input())
for i in range(n):
	for j in range(i + 1):
		print('*', end="")
	print()
"""

tri_17 = """
n = int(input())
for i in range(n):
	for j in range(i + 1):
		print('*', end="")
	print()
"""

tri_18 = """
n = int(input())
i = 0
while i < n:
	j = 0
	while j <= i:
		print ('*', end = "")
		j += 1
	print()
	i = i + 1
"""

tri_19 = """
n = int(input())
i = 0
while i < n:
	for j in range(i + 1):
		print ('*', end = "")
	print()
	i = i + 1
"""

tri_20 = """
n = int(input())
for i in range(n):
	j = 0
	while j <= i:
		print ('*', end = "")
		j += 1
	print()
"""

wrong_tri_1 = """
n = int(input())
for i in range(n * (n + 1) // 2):
	print('*', end = '')
print()
"""

version_list = [tri_1, tri_2, tri_3, tri_4, tri_5, tri_6, tri_7, tri_8, tri_9,
				tri_10, tri_11, tri_12, tri_13, tri_14, tri_15, tri_16, tri_17,
				tri_18, tri_19, tri_20]

data_matrix = []
wrong_data_matrix = []
for version in version_list:
	version_json = analyser(version)
	flatten_json = flatten(version_json)
	version_list = list(flatten_json.values())
	data_matrix.append(version_list)


wrong_json = analyser(wrong_tri_1)
flatten_wrong_json = flatten(wrong_json)
wrong_version_list = list(flatten_wrong_json.values())
wrong_array = np.array(wrong_version_list)


#pca = PCA(n_components = 2)
#newData = pca.fit_transform(data_matrix)


#plt.plot(newData[:, 0], newData[:, 1], 'o', color = 'blue', label='Normal code')
#plt.plot(newData[0, 0], newData[0, 1], 'o', color = 'green', label='Hard-coded')
#plt.legend(loc='upper right')
#plt.xlabel('x1')
#plt.ylabel('x2')
#plt.title('Version tree in 2D after PCA processing')
#plt.show()

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


cluster_1 = []
cluster_2 = []
cluster_3 = []
cluster_4 = []
cluster_1_count = 0
cluster_2_count = 0
cluster_3_count = 0
cluster_4_count = 0
cluster_1_skilltree = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cluster_2_skilltree = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cluster_3_skilltree = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cluster_4_skilltree = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in range(0,len(data_matrix)):
	if label[i] == 0:
		cluster_1.append(data_matrix[i])
		cluster_1_count += 1
	elif label[i] == 1:
		cluster_2.append(data_matrix[i])
		cluster_2_count += 1
	elif label[i] == 2:
		cluster_3.append(data_matrix[i])
		cluster_3_count +=  1
	elif label[i] == 3:
		cluster_4.append(data_matrix[i])
		cluster_4_count +=  1


cluster_list = [cluster_1, cluster_2, cluster_3, cluster_4]
cluster_skilltree_list = [cluster_1_skilltree, cluster_2_skilltree, cluster_3_skilltree, cluster_4_skilltree]



for cluster in cluster_list:
	skilltree = cluster_skilltree_list[cluster_list.index(cluster)]
	for data in cluster:
		for i in range(0, len(data)):
			if data[i] > 0:
				skilltree[i] += 1


#list of elements for comparison
compare_list = ['basicIO_output', 'condition_if_ifOnly', 'condition_if_withElse', 'condition_switch', 'loop_single_for', 'loop_single_while',
				'loop_nested_forOnly', 'loop_nested_whileOnly', 'loop_nested_mixed', 'array_nonCharArray_singleDim', 'array_nonCharArray_multiDim',
				'array_charArray_singleDim', 'array_charArray_multiDim', 'function_recursion_procedure', 'function_recursion_function', 'function_notRecursion_procedure',
				'function_notRecursion_function', 'class_inheritance_constructor', 'class_inheritance_noConstructor', 'class_noInheritance_constructor',
				'class_noInheritance_noConstructor', 'module_string_length', 'module_string_concat', 'module_string_substr', 'module_string_replace',
				'module_string_changeType', 'module_fileIO_open', 'module_fileIO_close', 'module_fileIO_write', 'module_fileIO_read', 'module_array_length',
				'module_array_concat', 'module_array_split', 'module_array_sort', 'module_array_pop', 'module_array_push', 'module_array_find']

skilltree_structure = list(flatten(analyser(tri_1)).keys())

compare_list_index = [2, 5, 6, 7, 10, 11, 12, 18, 19, 21, 22, 25, 26, 28, 29, 32, 33, 35, 36, 39, 40, 41, 42, 43, 45, 46, 47, 48, 50, 51, 52, 53 ,54 ,55, 56, 57, 58, 59, 60]

lack = []
redundance = []

for i in compare_list_index:
	if cluster_2_skilltree[i]/len(cluster_2) >= 0.7 and wrong_version_list[i] == 0:
		lack.append(skilltree_structure[i])
	elif cluster_2_skilltree[i]/len(cluster_2) <= 0.1 and wrong_version_list[i] > 0:
		redundance.append(skilltree_structure[i])


print("lacking element: ", lack)
print("redundant element: ", redundance)
#plt.plot(cluster_1[:,0], cluster_1[:,1], 'o', color = 'blue', label='cluster 1')
#plt.plot(cluster_2x, cluster_2y, 'o', color = 'green', label='cluster 2')
#plt.plot(cluster_3x, cluster_3y, 'o', color = 'yellow', label='cluster 3')
#plt.plot(cluster_4x, cluster_4y, 'o', color = 'red', label='cluster 4')


#plt.legend(loc='upper right')
#plt.xlabel('x1')
#plt.ylabel('x2')
#plt.title('Clustering by K-Means')
#plt.show();


