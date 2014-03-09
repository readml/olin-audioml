"""
Guassian Mixture Model Implementation of VoiceID
author: chris
"""

from config import *
import formatFeatures as FF
import numpy as np
from itertools import permutations
from operator import itemgetter

from sklearn.mixture import GMM
import os

def score(predict, real, n_components):
	predDict = {}
	realDict = {}
	for val in xrange(n_components):
		predDict[val] = set(np.where(predict == val)[0])
		realDict[val] = set(np.where(real == val)[0])

	scoreDict = {}
	for i in xrange(n_components):
		for j in xrange(n_components):
			pred = predDict[i]
			real_ = realDict[j]
			scoreDict[(i,j)] = len(pred - real_) + len(real_ - pred)

	scores = []
	for perm in permutations(xrange(n_components)):
		combs = zip(xrange(n_components), perm)
		scores.append((combs,sum([scoreDict[comb] for comb in combs])))
	scores.sort(key = itemgetter(1))
	mapping = dict(scores[0][0])
	print mapping
	print predict
	print scores[0]
	mapped_predict = [mapping[val] for val in predict]
	return float(len(np.where(mapped_predict - real == 0)[0]))/predict.shape[0]
	
			

	return 1
if __name__ == "__main__":
	voices,dataM,dataF = FF.getDataSet(os.listdir(samples_path))

    #Getting training and testing data     
	mTrainX, mTrainY, mTestX, mTestY = FF.splitTraining(dataM, onehot = False)     
	fTrainX, fTrainY, fTestX, fTestY = FF.splitTraining(dataF, onehot = False)

	model = GMM(len(voices))
	model.fit(mTrainX)

	predict = model.predict(mTestX)
#	print score(predict, mTestY, len(voices))

	# a = np.array([0,1,1,2])
	# b = np.array([0,1,2,1])

	# print score(a,b,3)



