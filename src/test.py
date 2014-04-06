"""
signal_processing.py
contains methods to process audio signals
author: chris
"""

from config import *
from scipy.io import wavfile
import scipy.fftpack as SF
import numpy as np
from signal_processing import framesig

@debug
def loadAudio(filename):
	"""
	author: chris
	Description:
	Uses scipy (python module) to load an audio file

	:param filename		- filename of audio file
						(samples path can be edited in config.py`)

	:returns 			- returns sample rate, numpy data
	"""
	srate,data = wavfile.read(os.path.join(samples_path,filename))
	return srate,data

@debug
def frameSignal(sig, frameLen, step):
	sig_len = sig.shape[0]
	num_frames = int(np.ceil((sig_len - frameLen)/step) + 1)
	result = np.zeros(shape=(num_frames, frameLen))
	for i in xrange(num_frames):
		result[i] = sig[i*step:i*step+frameLen]
	return result		

@debug
def filterBank(frames, rate):
	for frame in frames:
		SF.fftfreq(frame.shape[0], d = 1.0/rate)
		


if __name__ == "__main__":
	rate, data = loadAudio("19.wav")
	array_frames = frameSignal(data, 100, 10)
	# other_frames = framesig(data, 100, 10)
	filterBank(array_frames, rate)

