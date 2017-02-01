
import matplotlib.pyplot as plt
from pylab import *
from scipy.io import wavfile
from random import random
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


def short_signal(stride,freq,snd,scale):

    short_sound=[]
    location=0
    index=0

    print len(snd)

    while location<len(snd):
        maybe_sound,location=chomp_on_zero(snd,location,stride,freq)
        if random()<scale:
            short_sound=np.concatenate([short_sound,maybe_sound])
        index+=1

    print float(len(short_sound))/freq,len(short_sound)

    return short_sound

