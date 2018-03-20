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


pca = PCA(n_components = 2)
newData = pca.fit_transform(data_matrix)


plt.plot(newData[:, 0], newData[:, 1], 'o', color = 'blue', label='Normal code')
plt.plot(newData[0, 0], newData[0, 1], 'o', color = 'green', label='Hard-coded')
plt.legend(loc='upper right')
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Version tree in 2D after PCA processing')
plt.show()

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


cluster_1x = []
cluster_1y = []
cluster_2x = []
cluster_2y = []
cluster_3x = []
cluster_3y = []
cluster_4x = []
cluster_4y = []
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

for i in range(0,len(newData)):
	if label[i] == 0:
		cluster_1x.append(newData[i,0])
		cluster_1y.append(newData[i,1])
		cluster_1_count += 1
	elif label[i] == 1:
		cluster_2x.append(newData[i,0])
		cluster_2y.append(newData[i,1])
		cluster_2_count += 1
	elif label[i] == 2:
		cluster_3x.append(newData[i,0])
		cluster_3y.append(newData[i,1])
		cluster_3_count +=  1
	elif label[i] == 3:
		cluster_4x.append(newData[i,0])
		cluster_4y.append(newData[i,1])
		cluster_4_count +=  1



plt.plot(cluster_1x, cluster_1y, 'o', color = 'blue', label='cluster 1')

if cluster_2x != []:
	plt.plot(cluster_2x, cluster_2y, 'o', color = 'green', label='cluster 2')

if cluster_3x != []:
	plt.plot(cluster_3x, cluster_3y, 'o', color = 'yellow', label='cluster 3')

if cluster_4x != []:
	plt.plot(cluster_4x, cluster_4y, 'o', color = 'red', label='cluster 4')


plt.legend(loc='upper right')
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Clustering by K-Means')
plt.show();


