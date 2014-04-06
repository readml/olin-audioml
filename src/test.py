from config import debug
import alsaaudio as aa
import numpy as np
import wave, time
import pandas as pd

import formatFeatures as FF

from sklearn.mixture import GMM
from sklearn.preprocessing import OneHotEncoder

@debug
def openAudioInputStream():
	"""
	Opens stream to get Audio input from microphone
	"""
	inp = aa.PCM(aa.PCM_CAPTURE)
	inp.setchannels(1)
	inp.setrate(44100)
	inp.setformat(aa.PCM_FORMAT_S16_LE)
	inp.setperiodsize(1024)
	return inp

@debug
def openWavStream(wavFile):
	"""
	Opens a wav stream to write sound to file
	"""
	w = wave.open(wavFile, 'w')
	w.setnchannels(1)
	w.setsampwidth(2)
	w.setframerate(rate)

	#Use w.writeframes(data)
	return w

@debug
def recordAudio(inp, dur):
	"""
	"""
	start = time.time()
	audioData = np.array([0])
	while (time.time() - start < dur):
		l, data = inp.read()
		audioData = np.append(audioData,np.fromstring(data, dtype = 'int16'))
	return audioData

@debug
def createTrainingData(inputData):
	dataM = np.zeros(shape=(1,14))
	dataF = np.zeros(shape=(1,27))
	for i,data in enumerate(inputData):
		mfcc, fbank = FF.getFeatures(data,rate)
		dataM = np.concatenate((dataM, FF.formatForTraining(mfcc,i)), axis = 0) 
		dataF = np.concatenate((dataF, FF.formatForTraining(fbank, i)), axis = 0)
	return dataM, dataF



dataF = np.concatenate((dataF, formatForTraining(fbank, i)), axis = 0)



if __name__ == "__main__":
	rate = 44100

	voices = []
	data = []

	inp = openAudioInputStream()
	while True:
		command = raw_input("Command?")
		if command == "r":
			voices.append(raw_input("name of voice"))
			data.append(recordAudio(inp, 5))
		if command == "m":
			model = GMM(len(voices))
			mfcc,fbank = createTrainingData(data)
			model.fit(mfcc[:,:-1], OneHotEncoder(mfcc[:,-1]))
			print 'Ready to test'
			while raw_input() != "q":
				testData = recordAudio(inp, 5)
				test_mfcc, test_fbank = createTrainingData(testData)
				print model.predict(test_mfcc[:,:-1])








# l, data = inp.read()
# a = numpy.fromstring(data, dtype='int16')
# print numpy.abs(a).mean()
# w.writeframes(data)