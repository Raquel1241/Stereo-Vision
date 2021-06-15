"""
Filtering functions enacted on the measurements
"""

import numpy as np
from scipy import signal
import math

an = None
a1 = 1
wn = None
filLen = 10
w0 = w1 = w2 = w3 = []
for i in range(filLen):
	w0.append(1)
	w1.append(i+1)
	w2.append(2**i)
	w3.append(math.exp(i))

def LPF(iSig: list):
	order = 5
	norm_cut_freq = 0.8
	coefN, coefD = signal.butter(order, norm_cut_freq, analog=False,fs=8)
	fSig = signal.lfilter(coefN,coefD,iSig)
	#fSig = iSig
	return fSig
	
def avg(iSig: list,axis = an, w = w1):
	if len(iSig) > len(w):
		iSig = iSig[len(iSig)-len(w):]
	elif len(iSig) < len(w):
		i = len(w)-len(iSig)
		while i > 0:
			iSig.insert(0, 0)
			i = i - 1
	rSig = np.average(iSig, axis = axis, weights=w)
	return rSig