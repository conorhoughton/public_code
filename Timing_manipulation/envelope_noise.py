
#http://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter

#http://stackoverflow.com/questions/33933842/how-to-generate-noise-in-frequency-range-with-numpy

import matplotlib.pyplot as plt
from pylab import *
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


def control(samp_freq,snd,filename):
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

    s_control=zeros((len(s0)))

    for i,envelope in enumerate(envelopes):
        noise=band_limited_noise(bands[i][0],bands[i][1], len(envelope),samp_freq)
        noise=louden(noise)
        for t,e in enumerate(envelope):
            s_control[t]+=noise[t]*e

    # for i,envelope in enumerate(envelopes):
    #     freq=0.5*(bands[i][1]+bands[i][0])
    #     nu=2*np.pi*freq/samp_freq
    #     for t,e in enumerate(envelope):
    #         s_control[t]+=np.sin(nu*t)*e

    return s_control


# short_envelopes=[]

# offset=len(snd)%2

# for e in envelopes:
#     this_envelope=[]
#     for i in range(0,len(e)-offset,2):
#         this_envelope.append(0.5*(e[i]+e[i+1]))
#     short_envelopes.append(this_envelope)

# s_control=zeros((len(s0)/2))

# for i,envelope in enumerate(short_envelopes):
#     noise=band_limited_noise(shift*bands[i][0],shift*bands[i][1], len(envelope),
#                              samp_freq)
#     noise=louden(noise)
#     for t,e in enumerate(envelope):
#         s_control[t]+=noise[t]*e

# control_snd=zeros((s_control.shape[0]),dtype='int16')

# for i in range(0,s_control.shape[0]):
#     control_snd[i]=s_control[i]

# wavfile.write('noisy_control_short_'+filename,samp_freq,control_snd)


# long_envelopes=[]

# for e in envelopes:
#     this_envelope=[]
#     for i in range(0,len(e)):
#         this_envelope.append(e[i])
#         this_envelope.append(e[i])
#     long_envelopes.append(this_envelope)

# s_control=zeros((2*len(s0)))

# print len(s_control)

# for i,envelope in enumerate(long_envelopes):
#     noise=band_limited_noise(shift*bands[i][0],shift*bands[i][1], len(envelope),
#                              samp_freq)
#     noise=louden(noise)
#     for t,e in enumerate(envelope):
#         s_control[t]+=noise[t]*e

# control_snd=zeros((s_control.shape[0]),dtype='int16')

# for i in range(0,s_control.shape[0]):
#     control_snd[i]=s_control[i]

# wavfile.write('noisy_control_long_'+filename,samp_freq,control_snd)
