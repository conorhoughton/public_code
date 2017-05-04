
#checking various band passes don't effect the phase

import matplotlib.pyplot as plt
from pylab import *
import numpy as np
import math as m

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

def make_angle(t):
    while t>2*np.pi:
        t-=2*np.pi
    return t

big_t=2000
sample=np.zeros(big_t)



#slope =0.5
# t1,width=800,200
# freq=.25
# for  t in range(t1,t1+width):
#     sample[t]+=slope*(t-t1)
# for t in range(t1+width,t1+2*width):
#     sample[t]+=slope*(t1+2*width-t)

freq1=.05
freq2=.5

angles=[]

for t in range(0,big_t):
    sample[t]+=m.sin(freq1*t)+m.sin(freq2*t)
    angles.append(make_angle(freq1*t)-np.pi)

band0=.0001
band1=.01

sample_bp=butter_bandpass_filter(sample,band0,band1,1.0,4)
sample_bp_r=butter_bandpass_filter(np.flipud(sample),band0,band1,1.0,4)


sample_fft=np.fft.fft(sample)

for k in range(0,len(sample_fft)):
    if k>40:
        sample_fft[k]=0

sample_ifft=np.fft.ifft(sample_fft)



#plt.plot(sample)
#plt.plot(np.abs(sample_ifft))
#plt.plot(sample_ifft)
#plt.plot(sample_bp)
#plt.plot(sample_bp+sample_bp_r)
#plt.show()

#plt.plot(angles)
plt.plot((np.angle(sample_ifft)-angles)/np.pi)
#plt.plot(np.angle(hilbert(sample_bp)))
#plt.plot(np.angle(hilbert(sample_bp+sample_bp_r)))
plt.show()
print 
