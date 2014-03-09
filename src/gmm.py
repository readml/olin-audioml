"""
Guassian Mixture Model Implementation of VoiceID
author: chris
"""

from config import *
import formatFeatures as FF
import numpy as np

from sklearn.mixture import GMM
import os

def score(predict, real):
	return 1 #TODO

if __name__ == "__main__":
	voices,dataM,dataF = FF.getDataSet(os.listdir(samples_path))

    #Getting training and testing data     
	mTrainX, mTrainY, mTestX, mTestY = FF.splitTraining(dataM, onehot = False)     
	fTrainX, fTrainY, fTestX, fTestY = FF.splitTraining(dataF, onehot = False)

	model = GMM()
	model.fit(fTrainX)

	predict = model.predict_proba(fTestX)
	print predict
	score(predict, fTestY)



