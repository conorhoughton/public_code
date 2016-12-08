
#http://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter

import matplotlib.pyplot as plt
from pylab import *
from scipy.io import wavfile
import numpy as np


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


filename="Karen_trim.wav"

ms=0.001
stride=50*ms

samp_freq, snd = wavfile.read(filename)

short_sound=[]
location=0
index=0
while location<len(snd):
    maybe_sound,location=chomp_on_zero(snd,location,stride,samp_freq)
    if index%2==0:
        short_sound=np.concatenate([short_sound,maybe_sound])
    index+=1

print len(snd),len(short_sound)

rebuild_snd=zeros((len(short_sound)),dtype='int16')

for i in range(0,len(short_sound)):
    rebuild_snd[i]=short_sound[i]

wavfile.write('simple_short_'+filename,samp_freq,rebuild_snd)

