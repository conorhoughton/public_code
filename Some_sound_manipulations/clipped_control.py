
#http://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter

#http://stackoverflow.com/questions/33933842/how-to-generate-noise-in-frequency-range-with-numpy

import matplotlib.pyplot as plt
from pylab import *
from scipy.io import wavfile
import numpy as np

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
print "\n"

s_control=zeros((len(s0)))


cut_level=1
high=False

for i,envelope in enumerate(envelopes):
    noise=band_limited_noise(bands[i][0],bands[i][1], len(envelope),
                             samp_freq)
    noise=louden(noise)
    cut=cut_level*np.average(envelope)
    for t,e in enumerate(envelope):
        if high and e>cut:
            s_control[t]+=noise[t]*e
        elif not high and e<cut:
            s_control[t]+=noise[t]*e

#this messing is needed to cast back to int16 for .wav
control_snd=zeros((s_control.shape[0]),dtype='int16')
for i in range(0,s_control.shape[0]):
    control_snd[i]=s_control[i]
############

cut_side="low"
if high:
    cut_side="high"

wavfile.write('clipped_control_'+cut_side+'_'+str(cut_level)+'_'+filename,samp_freq,control_snd)



