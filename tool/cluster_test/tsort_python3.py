import numpy as np # linear algebra
import pandas as pd
import matplotlib.pyplot as plt
import analyser_2 as analyser
from tree import flatten
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.cluster import MeanShift, estimate_bandwidth, DBSCAN, spectral_clustering, FeatureAgglomeration
from sklearn import random_projection
from matplotlib.colors import LogNorm
from itertools import cycle
from sklearn import mixture

# Clustering using Mean-shift & raw data
def mean_shift_clustering(data):
	bandwidth = estimate_bandwidth(data, quantile=0.2, n_samples = 100)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
	ms.fit(data)
	labels = ms.labels_
	# print(labels)
	cluster_centers = ms.cluster_centers_

	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique)

	print("number of estimated clusters : %d" % n_clusters_)

	plt.figure(1)
	plt.clf()

	colors = cycle('bgrcmykw')
	for k, col in zip(range(n_clusters_), colors):
		my_members = labels == k
		cluster_center = cluster_centers[k]
		plt.plot(data[my_members, 0], data[my_members, 1], col + '.')
		plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
				 markeredgecolor='k', markersize=14, label = k)
	plt.title('Estimated number of clusters: %d' % n_clusters_)
	plt.legend(loc='best')
	plt.show()
	return labels

def dbscan_clustering(X):
	db = DBSCAN(eps = 0.1, min_samples = 5)
	y_pred = db.fit_predict(X)
	plt.scatter(X[:, 0], X[:, 1], c=y_pred)
	labels = db.labels_
	# Number of clusters in labels, ignoring noise if present.
	n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
	print('Estimated number of clusters: %d' % n_clusters_)
	plt.show()
	return y_pred

def gaussian_clustering(newdata):
	clf = mixture.GaussianMixture(n_components=5, covariance_type='full')
	clf.fit(newdata)
	x = np.linspace(-20., 30.)
	y = np.linspace(-20., 40.)
	X, Y = np.meshgrid(x, y)
	XX = np.array([X.ravel(), Y.ravel()]).T
	Z = -clf.score_samples(XX)
	Z = Z.reshape(X.shape)

	CS = plt.contour(X, Y, Z, norm=LogNorm(vmin=1.0, vmax=1000.0),
					 levels=np.logspace(0, 3, 10))
	CB = plt.colorbar(CS, shrink=0.8, extend='both')
	plt.scatter(newdata[:, 0], newdata[:, 1], .8)

	plt.title('Negative log-likelihood predicted by a GMM')
	plt.axis('tight')
	plt.show()

df2 = pd.read_csv('program_code_python_only.csv')

# print(df2.QCode.unique())

df2 = df2[df2.QCode == "TSORT"]
print(df2.head())
'''
# 262 correct code in total
i = 0
data_matrix = []
print(df2.head())

for code in df2.iterrows():
	# print(code[1][0])
	i = i + 1
	print(code)
	version_json = analyser.analyser(code[1].Solutions)
	# flatten the data for ease of comparison
	flatten_json = flatten(version_json)
	# convert dict to list
	version_list = list(flatten_json.values())
	# append list of value into data matrix
	data_matrix.append(version_list)


print(i)
pca = PCA(n_components = 2)
newData = pca.fit_transform(data_matrix)

# Raw Data
plt.plot(newData[:, 0], newData[:, 1], 'o', color = 'blue', label='Normal code')
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
plt.title('Standarded Version tree in 2D after PCA processing')
plt.show()

# labels = mean_shift_clustering(newData)
labels = mean_shift_clustering(newData_standard)
# labels = dbscan_clustering(newData_standard)
# gaussian_clustering(newData_standard)

# Showing examples
j = 0
cluster_shown = []
for code in df2.iterrows():
	if labels[j] not in cluster_shown:
		print("Example of cluster ", labels[j], ":")
		print(code[1].Solutions)
		cluster_shown.append(labels[j])
	j = j + 1

# n_samples = 100, quantile = 0.2
# Cluster 0: x.sort()
# Cluster 2: x.sort() with function call
# Cluster 1: oneline Sorting - map
# Cluster 5: map
# Cluster 6: mergesort
# Cluster 3: mergesort
# Cluster 4: mergesort
# Cluster 7: countingsort
# Cluster 8: quicksort
# Cluster 9: mergeSort
# Cluster 10: quicksort

# transformer = random_projection.GaussianRandomProjection()
#transformer = random_projection.SparseRandomProjection(n_components=2)
#newData_standard_random = transformer.fit_transform(standardized_data_matrix)
alog = FeatureAgglomeration()
alog.fit(standardized_data_matrix)
newData_standard_random = alog.transform(standardized_data_matrix)
plt.plot(newData_standard_random[:, 0], newData_standard_random[:, 1], 'o', color = 'blue')
plt.title('Standarded Version tree in 2D after Gaussian Random processing')
plt.show()

labels = mean_shift_clustering(newData_standard_random)

j = 0
cluster_shown = []
for code in df2.iterrows():
	if labels[j] not in cluster_shown:
		print("Example of cluster ", labels[j], ":")
		print(code[1].Solutions)
		cluster_shown.append(labels[j])
	j = j + 1
'''
