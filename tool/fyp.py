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
	print(flatten_json)
	'''
	choose_list = dict()
	thingtocompare = ['basicIO', 'condition', 'loop', 'array', 'function',
						'class', 'module']
	for item in thingtocompare:
		choose_list[item] = flatten_json[item]
	print(choose_list)
	version_list = list(choose_list.values())
	'''
	version_list = list(flatten_json.values())
	data_matrix.append(version_list)
	print(version_list)


wrong_json = analyser(wrong_tri_1)
flatten_wrong_json = flatten(wrong_json)
wrong_version_list = list(flatten_wrong_json.values())
wrong_array = np.array(wrong_version_list)

# PCA To 2 dimension
pca = PCA(n_components = 2)
newData = pca.fit_transform(data_matrix)
print(newData)
print(newData[:, 0])
print(newData[:, 1])


plt.plot(newData[:, 0], newData[:, 1], 'o', color = 'blue', label='Normal code')
# plt.plot(newData[-1, 0], newData[-1, 1], 'o', color = 'red')
plt.plot(newData[0, 0], newData[0, 1], 'o', color = 'green', label='Hard-coded')
plt.legend(loc='upper right')
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Version tree in 2D after PCA processing')
plt.show()

# Standardization
scaler = StandardScaler().fit(data_matrix)
standardized_data_matrix = scaler.transform(data_matrix)
pca = PCA(n_components = 2)
newData_standard = pca.fit_transform(standardized_data_matrix)
plt.plot(newData_standard[:, 0], newData_standard[:, 1], 'o', color = 'blue')
plt.plot(newData_standard[0, 0], newData_standard[0, 1], 'o', color = 'green')
# plt.plot(newData_standard[-1, 0], newData_standard[-1, 1], 'o', color = 'red')
plt.show()

# Normalization
scaler = Normalizer().fit(data_matrix)
normalized_data_matrix = scaler.transform(data_matrix)
pca = PCA(n_components = 2)
newData_normal = pca.fit_transform(normalized_data_matrix)
plt.plot(newData_normal[:, 0], newData_normal[:, 1], 'o', color = 'blue')
plt.plot(newData_normal[0, 0], newData_normal[0, 1], 'o', color = 'green')
# plt.plot(newData_normal[-1, 0], newData_normal[-1, 1], 'o', color = 'red')
plt.show()

# Plot GaussianMixture

raw_data = newData
test_data = (newData[1:, :])
test_data_standard = (newData_standard[1:, :])
test_data_normal = (newData_normal[1:, :])
all_dataset = []
all_dataset.append(raw_data)
all_dataset.append(test_data)
all_dataset.append(newData_standard)
all_dataset.append(test_data_standard)
all_dataset.append(newData_normal)
all_dataset.append(test_data_normal)

for dataset in all_dataset:
	clf = mixture.GaussianMixture(n_components=2, covariance_type='full')
	clf.fit(dataset)

	x = np.linspace(-5., 5.)
	y = np.linspace(-5., 5.)
	X, Y = np.meshgrid(x, y)
	XX = np.array([X.ravel(), Y.ravel()]).T
	Z = -clf.score_samples(XX)
	Z = Z.reshape(X.shape)


	CS = plt.contour(X, Y, Z, norm=LogNorm(vmin=1.0, vmax=1000.0),
	                 levels=np.logspace(0, 3, 10))
	CB = plt.colorbar(CS, shrink=0.8, extend='both')
	plt.scatter(dataset[1:, 0], dataset[1:, 1], 8, marker = 'o', label = 'Normal code')
	plt.scatter(dataset[0, 0], dataset[0, 1], 8, marker = 'o', color = 'red',
				label = 'Hard-coded')
	plt.xlabel('x1')
	plt.ylabel('x2')
	plt.title('Data Density using Gaussian Method')
	plt.legend(loc='upper right')
	plt.show()

for dataset in all_dataset:
	xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))
	clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
	clf.fit(dataset)

	Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
	Z = Z.reshape(xx.shape)


	plt.title("Novelty Detection")
	plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.PuBu)
	a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='darkred')
	plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='palevioletred')

	s = 40
	b1 = plt.scatter(dataset[:, 0], dataset[:, 1], c='white', s=s,
						edgecolors='k', label = 'Normal code')
	b2 = plt.scatter(dataset[0, 0], dataset[0, 1], c='blue', s=s,
						edgecolors='k', label = 'Hard-coded')
	plt.axis('tight')
	plt.xlabel('x1')
	plt.ylabel('x2')
	plt.title('Novelty Detection using SVM method')
	plt.legend(loc='upper right')
	# plt.xlim((-5, 5))
	# plt.ylim((-5, 5))
	plt.show()

clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
clf.fit(raw_data)
result = clf.predict(wrong_version_list)
print(result)
