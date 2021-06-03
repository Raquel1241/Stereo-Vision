"""
Filtering functions enacted on the measurements
"""

import numpy as np
from scipy import signal

def LPF(iSig: list):
	order = 5
	norm_cut_freq = 0.3
	coefN, coefD = signal.butter(order, norm_cut_freq, analog=False,fs=10)
	fSig = signal.lfilter(coefN,coefD,iSig)
	#fSig = iSig
	return fSig