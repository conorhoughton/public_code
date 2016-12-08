
#http://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter

import matplotlib.pyplot as plt
from pylab import *
from scipy.io import wavfile
import numpy as np

filename="Karen_trim.wav"

from scipy.signal import butter, lfilter, hilbert


def chomp_on_zero(signal,location,stride,freq):
    new_location=location+stride*freq

    if new_location>=len(signal):
        return signal[location:-1],len(signal)

    if signal[new_location]>0:
        while new_location<len(signal) and signal[new_location]>0:
            new_location+=1
    elif signal[new_location]<0:
        while new_location>location+1 and signal[new_location]<0:
            new_location-=1
    return signal[location:new_location],new_location

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

short_carriers=[]

ms=0.001
stride=50*ms

for c in carriers:
    this_carrier=[]
    location=0
    index=0
    while location<len(c):
        maybe_carrier,location=chomp_on_zero(c,location,stride,samp_freq)
        if index%2==0:
            this_carrier=np.concatenate([this_carrier,maybe_carrier])
        index+=1
        #print len(this_carrier),len(maybe_carrier)
    short_carriers.append(this_carrier)


s_rebuild=zeros((len(s0)/2)+1)

for i,envelope in enumerate(short_envelopes):
    while len(short_carriers[i])<len(envelope):
        short_carriers[i]+=np.asarray([0.0])
    for t,e in enumerate(envelope):
        s_rebuild[t]+=short_carriers[i][t]*e

rebuild_snd=zeros((s_rebuild.shape[0]),dtype='int16')

for i in range(0,s_rebuild.shape[0]):
    rebuild_snd[i]=s_rebuild[i]

wavfile.write('rebuild_short_'+filename,samp_freq,rebuild_snd)

