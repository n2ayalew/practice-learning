from numpy import *
import re
import operator
import bisect
import math
from os import listdir

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
	sorted_indicies = dists.argsort()
        class_score = {}
        for i in range(k):
            label = labels[sorted_indicies[i]]
            class_score[label] = class_score.get(label, 0) + 1
        sorted_classes = sorted(class_score.items(), key=operator.itemgetter(1), reverse=True)
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
    return data, ranges, mins

def dating_class_test():
    data, labels = file_to_mat('datingTestSet.txt')
    data, ranges, minVals = auto_norm(data)
    num_test = int(0.1 * shape(data)[0])
    train_len = shape(data)[0] - num_test
    train_data = data[num_test:,:]
    train_labels = labels[num_test:]
    k = 20
    error_count = 0.0
    for i in range(num_test):
        guessed_label = kNN_classify1(data[i,:], train_data, train_labels, 3)
        if (guessed_label != labels[i]):
            error_count +=1
    error_rate = error_count / float(num_test)
    print str(error_rate*100) + '%'
    return error_rate

def classify_person():
	percent_gaming = float(raw_input("Percentage of time playing video games?"))
	ff_miles = float(raw_input("Frequent flier miles earned per year?"))
	ice_cream = float(raw_input("Liters of ice cream consumed per year?"))
	arr = array([ff_miles, percent_gaming, ice_cream])
	data, labels = file_to_mat('datingTestSet.txt')
	data, ranges, mins = auto_norm(data)
	arr = (arr - mins) / ranges
	classifier_result = kNN_classify1(arr, data, labels, 3)
	return classifier_result

#CONSTS
IMAGE_WIDTH = 32
IMAGE_LENGTH = 32
def img_to_vector(filename):
	img = open(filename, 'r')
	retvec = zeros((1,1024))
	for i in range(IMAGE_WIDTH):
			line = img.readline()
			for j in range(IMAGE_LENGTH):
					retvec[0, IMAGE_WIDTH*i+j] = int(line[j])
	return retvec

def num_classifier():
	labels = []
	trainning_nums = listdir('trainingDigits')
	m = len(trainning_nums)
	n = IMAGE_WIDTH * IMAGE_LENGTH
	training_mat = zeros((m,n))
	
	for i in range(m):
		training_mat[i,:] = img_to_vector('trainingDigits/%s' % trainning_nums[i])
		file_num = trainning_nums[i].split('.')[0]
		labels.append(int(file_num.split('_')[0]))

	test_nums = listdir('testDigits')
	m = len(test_nums)
	error_rate = 0.0
	for i in range(m):
		file_name = test_nums[i].split('.')[0]
		test_num = int(file_name.split('_')[0])
		test_vector = img_to_vector('testDigits/%s' % test_nums[i])
		chosen_number = kNN_classify1(test_vector, training_mat, labels, 5)
		if (chosen_number != labels[i]):
				error_rate += 1
				print 'wrong number'
	error_rate = error_rate / m
	print error_rate

num_classifier()

