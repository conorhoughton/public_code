
#checking various band passes don't effect the phase

import matplotlib.pyplot as plt
from pylab import *
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

big_t=2000
sample=np.zeros(big_t)

slope=0.5
t1,width=800,200
freq=10

# for  t in range(t1,t1+width):
#     sample[t]+=slope*(t-t1)
# for t in range(t1+width,t1+2*width):
#     sample[t]+=slope*(t1+2*width-t)

for t in range(0,big_t):
    sample[t]+=30*np.sin(freq*2*np.pi*t)

plt.plot(sample)
plt.show()


# print "bandpass",
# for i,band in enumerate(bands):
#     print i,
#     s0_bp.append(butter_bandpass_filter(s0,band[0],band[1],samp_freq,2))
# print "\n"

# envelopes=[]
# carriers=[]

# print "hilbert",
# for i,bp_signal in enumerate(s0_bp):
#     print i,
#     analytic_signal = hilbert(bp_signal)
#     envelopes.append(np.abs(analytic_signal))
# print "\n"

# s_control=zeros((len(s0)))

# #shift=1.5
# shift=1

# for i,envelope in enumerate(envelopes):
#     noise=band_limited_noise(shift*bands[i][0],shift*bands[i][1], len(envelope),
#                              samp_freq)
#     noise=louden(noise)
#     for t,e in enumerate(envelope):
#         s_control[t]+=noise[t]*e

# control_snd=zeros((s_control.shape[0]),dtype='int16')

# for i in range(0,s_control.shape[0]):
#     control_snd[i]=s_control[i]

# wavfile.write('noise_control_'+str(shift)+"_"+filename,samp_freq,control_snd)



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
