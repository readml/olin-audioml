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

"""
Model Notes:
Gaussian Mixture model?
	Separate models for each speaker. 
"""

@debug
def getFeatures(signal, rate):
	"""
	Extracts Important Vocal Features
	"""
	if signal.shape[0] > mem_cut_off:
		mfcc,fbank = getFeatures(signal[mem_cut_off:], rate)
		return np.concatenate((fs.mfcc(signal[:mem_cut_off],rate),mfcc)), np.concatenate((fs.logfbank(signal,rate),fbank))
	else:
		return fs.mfcc(signal,rate), fs.logfbank(signal,rate)

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
		rate,signal = sp.loadAudio(afile)
		mfcc, fbank = getFeatures(signal,rate)
		dataM = formatForTraining(mfcc, i)
		dataF = formatForTraining(fbank, i)
		print dataM.shape
		print dataF.shape
	

if __name__ == "__main__":
	main()