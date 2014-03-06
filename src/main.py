"""
main.py
Testing voiceID methods

author: chris
"""
from config import *
import signal_processing as sp

def main():
	print sp.loadAudio("18.wav")

if __name__ == "__main__":
	main()