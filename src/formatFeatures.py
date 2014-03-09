"""
main.py
Testing voiceID methods

author: chris
"""

from config import *

import os
import numpy as np
import signal_processing as sp
import features as fs

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn import metrics


"""
Model Notes:
Gaussian Mixture model?
	Separate models for each speaker. 
"""

@debug
def getFeatures(signal, rate):
	"""
	Extracts Important Vocal Features

	author: chris
	"""
	if signal.shape[0] > mem_cut_off:
		mfcc = getFeatures(signal[mem_cut_off:], rate)
		return np.concatenate((fs.mfcc(signal[:mem_cut_off],rate),mfcc))
	else:
		return fs.mfcc(signal,rate)#, fs.logfbank(signal,rate)

@debug
def formatForTraining(data, voice):
	"""
	Formats data received from getFeatures for format
	returns numpy array of data:voice

	author: chris
	"""
	target = np.ones(shape=(data.shape[0],1)) * voice
	return np.concatenate((data,target), axis = 1)

@debug
def getDataSet(files):
	"""
	Loops through files and generates features for each
	Formats data of each file for modeling

	author: chris
	"""
	dataM = np.zeros(shape=(1,14))
	voices = []
	for i,afile in enumerate(files):
		print afile
		voices.append(i)
		rate,signal = sp.loadAudio(afile)
		mfcc = getFeatures(signal,rate)
		dataM = np.concatenate((dataM, formatForTraining(mfcc,i)), axis = 0) 
	return voices, dataM

@debug
def extractFeatures(afile):
	"""
	Extracts Feature from audio file
	"""
	rate,signal = sp.loadAudio(afile)
	mfcc = getFeatures(signal,rate)
	return mfcc
	
@debug
def splitTraining(data, split= .1, onehot = True):
	"""
	Splits the data into training and target features for testing and training sets
	Takes in the training:target feature array and splits based on split ratio (0<1)

	author: chris
	"""
	cutoff = int(data.shape[0]*.1)
	np.random.shuffle(data)
	X = data[:,:-1]
	if onehot:
		Y = one_hot(data[:,-1])
	else:
		Y = data[:,-1]

	return  X[:-cutoff,:], Y[:-cutoff], X[-cutoff:,:], Y[-cutoff:]

@debug
def one_hot(array):
	"""
	One Hotting class values for classifcation problem
	"""
	array = array.flatten().astype("int")
	output = np.zeros(shape = (len(array),np.max(array) + 1))
	output[np.arange(len(array)),array] = 1
	return output

@debug
def main():
	voices,dataM = getDataSet(os.listdir(samples_path))

	#Getting training and testing data
	mTrainX, mTrainY, mTestX, mTestY = splitTraining(dataM)


	# print mTrainX.shape
	# print mTrainY.shape
	# print mTestX.shape
	# print mTestY.shape
	
	#MFCC
	Mmodel = RandomForestClassifier(n_estimators = 300)
	Mmodel.fit(mTrainX, mTrainY)

	Mprediction =  Mmodel.predict(mTestX)
	Maccuracy = metrics.accuracy_score(mTestY, Mprediction)

	print "MFCC", Maccuracy
	

if __name__ == "__main__":
	main()