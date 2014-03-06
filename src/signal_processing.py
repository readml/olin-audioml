"""
signal_processing.py
contains methods to process audio signals
author: chris
"""

from config import *
from scipy.io import wavfile
import numpy as np

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
def framesig(sig,frame_len,frame_step,winfunc=lambda x:np.ones((1,x))):
    """Frame a signal into overlapping frames.

    :param sig: the audio signal to frame.
    :param frame_len: length of each frame measured in samples.
    :param frame_step: number of samples after the start of the previous frame that the next frame should begin.
    :param winfunc: the analysis window to apply to each frame. By default no window is applied.    
    :returns: an array of frames. Size is NUMFRAMES by frame_len.
    """
    slen = len(sig)
    frame_len = round(frame_len)
    frame_step = round(frame_step)
    if slen <= frame_len: 
        numframes = 1
    else:
        numframes = 1 + np.ceil((1.0*slen - frame_len)/frame_step)
        
    padlen = (numframes-1)*frame_step + frame_len
    
    zeros = np.zeros((padlen - slen,))
    padsignal = np.concatenate((sig,zeros))
    
    indices = np.tile(np.arange(0,frame_len),(numframes,1)) + np.tile(np.arange(0,numframes*frame_step,frame_step),(frame_len,1)).T
    indices = np.array(indices,dtype=np.int32)
    frames = padsignal[indices]
    win = np.tile(winfunc(frame_len),(numframes,1))
    return frames*win

@debug
def deframesig(frames,siglen,frame_len,frame_step,winfunc=lambda x:np.ones((1,x))):
    """Does overlap-add procedure to undo the action of framesig. 

    :param frames: the array of frames.
    :param siglen: the length of the desired signal, use 0 if unknown. Output will be truncated to siglen samples.    
    :param frame_len: length of each frame measured in samples.
    :param frame_step: number of samples after the start of the previous frame that the next frame should begin.
    :param winfunc: the analysis window to apply to each frame. By default no window is applied.    
    :returns: a 1-D signal.
    """
    frame_len = round(frame_len)
    frame_step = round(frame_step)
    numframes = np.shape(frames)[0]
    assert np.shape(frames)[1] == frame_len, '"frames" matrix is wrong size, 2nd dim is not equal to frame_len'
 
    indices = np.tile(np.arange(0,frame_len),(numframes,1)) + np.tile(np.arange(0,numframes*frame_step,frame_step),(frame_len,1)).T
    indices = np.array(indices,dtype=np.int32)
    padlen = (numframes-1)*frame_step + frame_len   
    
    if siglen <= 0: siglen = padlen
    
    rec_signal = np.zeros((1,padlen))
    window_correction = np.zeros((1,padlen))
    win = winfunc(frame_len)
    
    for i in range(0,numframes):
        window_correction[indices[i,:]] = window_correction[indices[i,:]] + win + 1e-15 #add a little bit so it is never zero
        rec_signal[indices[i,:]] = rec_signal[indices[i,:]] + frames[i,:]
        
    rec_signal = rec_signal/window_correction
    return rec_signal[0:siglen]
   
@debug
def magspec(frames,NFFT):
    """Compute the magnitude spectrum of each frame in frames. If frames is an NxD matrix, output will be NxNFFT. 

    :param frames: the array of frames. Each row is a frame.
    :param NFFT: the FFT length to use. If NFFT > frame_len, the frames are zero-padded. 
    :returns: If frames is an NxD matrix, output will be NxNFFT. Each row will be the magnitude spectrum of the corresponding frame.
    """    
    complex_spec = np.fft.rfft(frames,NFFT)
    return np.absolute(complex_spec)

@debug
def powspec(frames,NFFT):
    """Compute the power spectrum of each frame in frames. If frames is an NxD matrix, output will be NxNFFT. 

    :param frames: the array of frames. Each row is a frame.
    :param NFFT: the FFT length to use. If NFFT > frame_len, the frames are zero-padded. 
    :returns: If frames is an NxD matrix, output will be NxNFFT. Each row will be the power spectrum of the corresponding frame.
    """    
    return 1.0/NFFT * np.square(magspec(frames,NFFT))

@debug
def logpowspec(frames,NFFT,norm=1):
    """Compute the log power spectrum of each frame in frames. If frames is an NxD matrix, output will be NxNFFT. 

    :param frames: the array of frames. Each row is a frame.
    :param NFFT: the FFT length to use. If NFFT > frame_len, the frames are zero-padded. 
    :param norm: If norm=1, the log power spectrum is normalised so that the max value (across all frames) is 1.
    :returns: If frames is an NxD matrix, output will be NxNFFT. Each row will be the log power spectrum of the corresponding frame.
    """    
    ps = powspec(frames,NFFT);
    ps[ps<=1e-30] = 1e-30
    lps = 10*np.log10(ps)
    if norm:
        return lps - np.max(lps)
    else:
        return lps

@debug
def preemphasis(signal,coeff=0.95):
    """perform preemphasis on the input signal.
    
    :param signal: The signal to filter.
    :param coeff: The preemphasis coefficient. 0 is no filter, default is 0.95.
    :returns: the filtered signal.
    """    
    return np.append(signal[0],signal[1:]-coeff*signal[:-1])



