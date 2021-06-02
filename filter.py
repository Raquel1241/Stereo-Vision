"""
Filtering functions enacted on the measurements
"""

import numpy as np
from scipy import signal

def LPF(iSig: list):
	order = 4
	norm_cut_freq = 0.5
	coefN, coefD = signal.butter(order, norm_cut_freq, analog=False,fs=14)
	fSig = signal.lfilter(coefN,coefD,iSig)
	#fSig = iSig
	return fSig