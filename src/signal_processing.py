"""
signal_processing.py
contains methods to process audio signals
author: chris
"""

from config import *
from scipy.io import wavfile

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
	srate,data = wavfile.read(os.path.join(samples,filename))
	return srate,data

def frame_signal(signal, frame_length, frame_step, a_func = lambda x:np.ones(size=(1,x))):
	"""
	Adapted from James Lyons 2012

	Description:
	Frames a signal into overlapping frames.

	:param signal 		- the input audio signal 
	:param frame_length - the length of each frame (in samples)
	:param frame_step 	- number of samples for each step
	:param a_func		- analysis window to apply each frame

	:returns 			- an array of frames
	"""

	signal_length = len(signal)
	num_frames = 1 if signal_length <= frame_length else np.ceil((signal_length - frame_length)/frame_step)
	
	padded_length = (num_frames - 1) * frame_step + frame_length
	padded_signal = np.concatenate((signal, np.zeros(size = (padded_length - signal_length,))))

	indices = np.tile(np.arange(0,frame_length), (num_frames,1)) + np.tile(np.arange(0,num_frames*frame_step,frame_step),(frame_length,1)).T
	indices = indicies.astype(np.int32)
	
	frames = padded_signal[indicies]
	window = np.tile(a_func(frame_length),(num_frames,1))

	return frames * window

