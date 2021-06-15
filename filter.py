"""
Filtering functions enacted on the measurements
"""

import numpy as np
from scipy import signal
import math

an = None
a1 = 1
wn = None
w0 = [1,1,1,1,1,1,1,1,1,1]
w1 = [1,2,3,4,5,6,7,8,9,10]
w2 = [1,2,4,8,16,32,64,128,256,512]
w3 = [math.exp(0),math.exp(1),math.exp(2),math.exp(3),math.exp(4),math.exp(5),math.exp(6),math.exp(7),math.exp(8),math.exp(9)]

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