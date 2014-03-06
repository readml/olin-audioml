"""
main.py
Testing voiceID methods

author: chris
"""
from config import *
import signal_processing as sp
import features as fs

def main():
	(rate,signal) = sp.loadAudio("18.wav")
	mfcc_feat = fs.mfcc(signal,rate)
	fbank_feat = fs.logfbank(signal,rate)
	print fbank_feat[1:3,:]

if __name__ == "__main__":
	main()