import re
from numpy import *

def load_data_set():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

def build_vocab(data_set):
	vocab = set()
	for sample in data_set:
		vocab.update(sample)
	return list(vocab)


def convert_words_to_vec(sample, vocab):
	length = len(vocab)
	word_vec = zeros(length)
	for word in sample:
		if (word in vocab):
			word_vec[vocab.index(word)] += 1
	return word_vec

def trainNB(train_matrix, train_classes):
	num_samples = len(train_matrix)
	num_words = len(train_matrix[0])
	p1 = sum(train_classes)/float(num_samples)
	p0 = 1.0 - p1
	pwi1 = ones(num_words)
	pwi2 = ones(num_words)
	pwi1Denom = 2.0
	pwi2Denom = 2.0

	for i in range(num_samples):
		if (train_classes[i] == 1):
			pwi1 += train_matrix[i]
			pwi1Denom += sum(train_matrix[i])
		else:
			pwi2 += train_matrix[i]
			pwi2Denom += sum(train_matrix[i])

	p1Vec = log(pwi1 / pwi1Denom)
	p0Vec = log(pwi2 / pwi2Denom)
	return p1,p0,p1Vec,p0Vec

def classifyNB(vec2_classify, p0Vec, p1Vec, p0, p1):
	c1 = sum(vec2_classify * p1Vec) + log(p1)
	c0 = sum(vec2_classify * p0Vec) + log(p0)
	if (c1 > c0):
		return 1
	else:
		return 0

def testingNB():
	posts,classes = load_data_set()
	vocab = build_vocab(posts)
	vposts = []
	for post in posts:
		vposts.append(convert_words_to_vec(post, vocab))
	p1,p0,p1Vec,p0Vec = trainNB(vposts, classes)
	Doc1 = ['love', 'my', 'dalmation']
	Doc2 = ['stupid', 'garbage']
	set1 = convert_words_to_vec(Doc1, vocab)
	set2 = convert_words_to_vec(Doc2, vocab)
	results = []
	results.append(classifyNB(set1, p0Vec,p1Vec,p0,p1))
	results.append(classifyNB(set2, p0Vec,p1Vec,p0,p1))
	for i in results:
		if (i == 1):
			print "Abusive article"
		else:
			print "Nice article"

def parse_text(str):
	reg = re.compile('\W+')
	lst = reg.split(str)
	lst = [tok.lower() for tok in lst if len(tok) > 0]
	return lst

def spam_filter_test():
	emails = []
	classes = []
	vocab = []
	for i in range (1,26):
		spam = parse_text(open('email/spam/%d.txt' % i).read())
		emails.append(spam)
		classes.append(1)
		ham = parse_text(open('email/ham/%d.txt' % i).read())
		emails.append(ham)
		classes.append(0)
	test_list = []
	vocab = build_vocab(emails)
	training_set = range(50)
	for i in range(10):
		rand_index = int(random.uniform(0, len(training_set)))
		test_list.append(training_set[rand_index])
		del(training_set[rand_index])

	vemails = []
	class_list = []
	for i in training_set:
		vemails.append(convert_words_to_vec(emails[i], vocab))
		class_list.append(classes[i])
	p1,p0,p1Vec,p0Vec = trainNB(array(vemails), array(classes))

	## Test algorithm
	error_count = 0.0;
	for i in test_list:
		vec = convert_words_to_vec(emails[i], vocab)
		algo_class = classifyNB(vec, p0Vec, p1Vec, p0, p1)
		real_class = classes[i]
		if (algo_class == real_class):
			#print "EMAIL: " + str(i) + " Classified correctly"
			error_count += 0
		else:
			error_count += 1.0
			#print "EMAIL: " + str(i) + " NOT classified correctly"
	error_percent = error_count/len(test_list)
	#print "ERROR RATE = ", error_percent
	return error_percent

def average_error_of_spam():
	mean = 0.0
	num_trials = 15
	for i in range(num_trials):
		mean += spam_filter_test()
	mean = mean / num_trials
	return mean

print "Average error of spam filter ", average_error_of_spam()