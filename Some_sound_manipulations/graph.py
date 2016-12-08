import matplotlib.pyplot as plt
from pylab import *
from scipy.io import wavfile
import numpy as np
import scipy.fftpack

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


def louden(signal):
    this_max=np.amax(abs(signal))
    return signal/this_max

filename="Karen_trim.wav"

from scipy.signal import butter, lfilter, hilbert


samp_freq, snd = wavfile.read(filename)

snd=np.ndarray.astype(snd,float)

plt.plot(snd)
plt.show()

plt.plot(snd)
plt.plot(butter_bandpass_filter(abs(snd),0, 20, samp_freq,2))
plt.show()

w = scipy.fftpack.rfft(snd)
spectrum = w**2

cutoff_idx = spectrum < (spectrum.max()/5)
w2 = w.copy()
w2[cutoff_idx] = 0

plt.plot(snd)
plt.plot(np.abs(scipy.fftpack.irfft(w2)))
plt.show()

n=len(snd)
offset=2000
s0=np.concatenate([zeros((offset)),snd,zeros((offset))])
width=1000

smooth_snd=[]
for i in range(offset,n+offset):
    this_s=0
    for j in range(-width/2,width/2):
        this_s+=abs(s0[i+j])
    smooth_snd.append(abs(this_s/width))

plt.plot(snd)
plt.plot(smooth_snd)
plt.show()


