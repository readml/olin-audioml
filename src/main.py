"""
main.py
Testing voiceID methods

author: chris
"""
from config import *
import os, string
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
def main():
	voices = dict()
	for i,afile in enumerate(os.listdir(samples_path)):
		voices[afile] = string.letters[i]
		if int(afile[:-4]) <= 3000:
			data = getFeatures(afile)
			#TODO - addTargetFeature(data, string.letters)
		else:
			#TODO - split larger audio files down to smaller ones
			pass
	

if __name__ == "__main__":
	main()