
#http://samcarcagno.altervista.org/blog/basic-sound-processing-python/

import matplotlib.pyplot as plt
from pylab import *
from scipy.io import wavfile

filename="Karen_trim.wav"

samp_freq, snd = wavfile.read(filename)

fast_snd=zeros((0.5*snd.shape[0]+1),dtype='int16')
slow_snd=zeros((2*snd.shape[0]),dtype='int16')
copy_snd=zeros((snd.shape[0]),dtype='int16')

for i in range(0,snd.shape[0]):
    if i%2==0:
        fast_snd[i/2]=snd[i]

for i in range(0,snd.shape[0]):
    slow_snd[2*i]=snd[i]
    slow_snd[2*i+1]=snd[i]


for i in range(0,snd.shape[0]):
        copy_snd[i]=snd[i]

print snd.dtype,copy_snd.dtype

wavfile.write('fast_'+filename,samp_freq,fast_snd)
wavfile.write('copy_'+filename,samp_freq,copy_snd)
wavfile.write('slow_'+filename,samp_freq,slow_snd)

