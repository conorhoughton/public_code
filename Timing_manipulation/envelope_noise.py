
#http://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter

#http://stackoverflow.com/questions/33933842/how-to-generate-noise-in-frequency-range-with-numpy

import matplotlib.pyplot as plt
from pylab import *
from stretcher import *
from scipy.io import wavfile
import numpy as np
from scipy.signal import butter, lfilter, hilbert
from bands import *

def fftnoise(f):
    f = np.array(f, dtype='complex')
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1:Np+1] *= phases
    f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
    return np.fft.ifft(f).real

def band_limited_noise(min_freq, max_freq, samples=1024, samplerate=1):
    freqs = np.abs(np.fft.fftfreq(samples, 1./samplerate))
    f = np.zeros(samples)
    idx = np.where(np.logical_and(freqs>=min_freq, freqs<=max_freq))[0]
    f[idx] = 1
    return fftnoise(f)

def louden(signal):
    this_max=np.amax(abs(signal))
    return signal/this_max

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

       
def control(samp_freq,snd,new_length):
    print snd.shape
#    s0=np.concatenate([zeros((2000)),snd,zeros((2000))])
    s0=snd
    print s0.shape


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
    print "\n"

    s_control=zeros((new_length*samp_freq))

    for i,envelope in enumerate(envelopes):
        new_envelope=stretcher(envelope,samp_freq,new_length)
        noise=band_limited_noise(bands[i][0],bands[i][1], len(new_envelope),samp_freq)
        noise=louden(noise)
        for t,e in enumerate(new_envelope):
            s_control[t]+=noise[t]*e

    return s_control

