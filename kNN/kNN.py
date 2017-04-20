from numpy import *
import re
import operator
import bisect
import math

def build_data_set0():
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

def kNN_classify1(point, data_set, labels, k):
	num_points = shape(data_set)[0]
	point_tile = tile(point, (num_points, 1))
	diffs = point_tile - data_set
	squares = diffs**2
	sums = sum(squares, 1)
	dists = sums**0.5
	sorted_indicies = argsort(dists)
        class_score = {}
        for i in range(k):
            label = labels[sorted_indicies[i]]
            class_score[label] = class_score.get(label, 0) + 1
        sorted_classes = sorted(class_score.items(), key=operator.itemgetter(1))
        return sorted_classes[0][0]

def file_to_mat(filename):
    lines = open(filename, 'r')
    data_set = []
    labels = []
    for line in lines:
        line = line.strip()
        lst = line.split('\t')
        data_set.append(lst[:-1])
        labels.append(lst[-1])
    return array(data_set).astype(float), labels

def auto_norm(data):
    num_columns = data.shape[1]
    maxs = data.max(0)
    mins = data.min(0)
    ranges = maxs - mins
    num_rows = data.shape[0]
    for i in range(num_rows):
            data[i] = (data[i] - mins) / (ranges)
    return data

ds, cs = file_to_mat('datingTestSet.txt')
print ds
print auto_norm(ds)
