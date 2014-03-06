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

@debug
def getFeatures(filename):
	"""
	Extracts Important Vocal Features
	"""
	(rate,signal) = sp.loadAudio(filename)
	mfcc_feat = fs.mfcc(signal,rate)
	fbank_feat = fs.logfbank(signal,rate)
	return fbank_feat

@debug
def formatForTraining(data, voice):
	"""
	Formats data received from getFeatures for format
	returns numpy array of data:voice
	"""
	target = np.ones(shape=(data.shape[0],1)) * voice
	return np.concatenate((data,target), axis = 1)

@debug
def main():
	voices = []
	for i,afile in enumerate(os.listdir(samples_path)):
		voices.append(i)
		if int(afile[:-4]) <= 3000:
			formatForTraining(getFeatures(afile), i)
		else:
			#TODO - split larger audio files down to smaller ones
			pass
		raw_input()
	

if __name__ == "__main__":
	main()