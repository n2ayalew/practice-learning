from numpy import *
import operator
import bisect
import math

def build_data_set():
	groups = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
	labels = ['A', 'A', 'B', 'B']
	return groups, labels

def kNN_classify0(point, data_set, labels, k):
	dists = []
	j = 0
	for i in data_set:
		dist = math.sqrt((i[0] - point[0])**2 + (i[1] - point[1])**2)
		dists.append(dist)

	dists = array(dists)
	aCount = 0
	bCount = 0

	while(j < k):
		min_index = argmin(dists)
		if (labels[min_index] == 'A'):
			aCount += 1
		else:
			bCount += 1
		delete(dists, min_index)
		j += 1
	if (aCount > bCount):
		print 'CLASS: A'
	else:
		print 'CLASS: B'

def kNN_classify(point, data_set, labels, k):
	num_points = shape(data_set)[0]
	point_tile = tile(point, (num_points, 1))

g,l = build_data_set()
kNN_classify([0.2, 0.3], g, l, 3)