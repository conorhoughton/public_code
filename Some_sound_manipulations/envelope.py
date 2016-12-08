
#http://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter

import matplotlib.pyplot as plt
from pylab import *
from scipy.io import wavfile
import numpy as np

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


filename="Karen_trim.wav"

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
sines=[]

print "hilbert",
for i,bp_signal in enumerate(s0_bp):
    print i,
    analytic_signal = hilbert(bp_signal)
    envelopes.append(np.abs(analytic_signal))
    carriers.append(np.real(analytic_signal/np.abs(analytic_signal)))

    this_sine=[]
    freq=(bands[i][1]+bands[i][0])*0.5
    nu=2*np.pi*freq/samp_freq
    for t,c in enumerate(carriers[-1]):
        this_sine.append(sin(nu*t))
    sines.append(this_sine)
print "\n"



for i,signal in enumerate(s0_bp):
    plt.subplot(4,1,1)
    plt.title(str(bands[i]))
    plt.plot(signal)
    plt.subplot(4,1,2)
    plt.plot(envelopes[i])
    plt.subplot(4,1,3)
    plt.plot(signal)
    plt.plot(envelopes[i])
    plt.subplot(4,1,4)
    plt.plot(carriers[i][5000:6000])
    plt.show()

np_envelopes=np.asarray(envelopes)
plt.plot(np.sum(np_envelopes,axis=0))
plt.plot(s0)
plt.show()

for i,signal in enumerate(s0_bp):
    plt.plot(np.abs(np.fft.rfft(signal)))

plt.show()
