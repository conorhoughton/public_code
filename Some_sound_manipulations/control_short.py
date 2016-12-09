
#http://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter

import matplotlib.pyplot as plt
from pylab import *
from scipy.io import wavfile
import numpy as np

filename="Karen_trim.wav"

from scipy.signal import butter, lfilter, hilbert

def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


samp_freq, snd = wavfile.read(filename)


s0=np.concatenate([zeros((2000)),snd,zeros((2000))])
print s0.shape

bands=[[230, 270.0], [270.0, 320.0], [320.0, 380.0], [380.0, 450.0], [450.0, 540.0], [540.0, 650.0], [650.0, 780.0], [780.0, 930.0], [930.0, 1110.0], [1110.0, 1330.0], [1330.0, 1590.0], [1590.0, 1890.0], [1890.0, 2250.0], [2250.0, 2680.0], [2680.0, 3200.0], [3200.0, 3800.0]]

s0_bp=[]

print "bandpass",
for i,band in enumerate(bands):
    print i,
    s0_bp.append(butter_bandpass_filter(s0,band[0],band[1],samp_freq,2))
print "\n"

envelopes=[]
carriers=[]

print "hilbert",
for i,bp_signal in enumerate(s0_bp):
    print i,
    analytic_signal = hilbert(bp_signal)
    envelopes.append(np.abs(analytic_signal))
    carriers.append(np.real(analytic_signal/np.abs(analytic_signal)))
print "\n"


short_envelopes=[]

offset=len(snd)%2

for e in envelopes:
    this_envelope=[]
    for i in range(0,len(e)-offset,2):
        this_envelope.append(0.5*(e[i]+e[i+1]))
    short_envelopes.append(this_envelope)

s_control=zeros((len(s0)/2))

for i,envelope in enumerate(short_envelopes):
    freq=0.5*(bands[i][1]+bands[i][0])
    nu=2*np.pi*freq/samp_freq
    for t,e in enumerate(envelope):
        s_control[t]+=np.sin(nu*t)*e

#this messing is needed to cast back to int16 for .wav
control_snd=zeros((s_control.shape[0]),dtype='int16')
for i in range(0,s_control.shape[0]):
    control_snd[i]=s_control[i]

wavfile.write('control_short_'+filename,samp_freq,control_snd)

