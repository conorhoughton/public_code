import sys, getopt
import matplotlib.pyplot as plt
from pylab import *
from bands import *
from envelope_noise import *
from stretcher import *
from shortner import *
from scipy.io import wavfile
import numpy as np
from random import gammavariate

class Sentence:

    def __init__(self,sentence_file):
        text_file = open(sentence_file, "r")
        lines = text_file.readlines()
        lines =[s.strip() for s in lines]
        print lines
        print len(lines)
        text_file.close()        
        self.words=[]
        self.word_names=[]
        word_freqs=[]
        self.t_lengths=[]


        for word_name in lines:
            self.word_names.append(word_name)
            word_freq,word=wavfile.read("sound_files/"+word_name+".wav")
            self.words.append(word)
            word_freqs.append(word_freq)
            self.t_lengths.append(double(word.shape[0])/word_freq)
            print word.shape,word_freq,self.t_lengths[-1],word_name
        self.freq=word_freqs[0]
        for freq in word_freqs:
            if freq != self.freq:
                print "not all the freqs the same f/p"

        self.length=len(self.word_names)

    def stretch(self,length):

        for i,w in enumerate(self.words):
            new_w=stretcher(w,self.freq,length)
            self.words[i]=np.asarray(new_w)

    def shorten(self,length,stride):

        for i,w in enumerate(self.words):
            scale=length/self.t_lengths[i]
            new_w=short_signal(stride,self.freq,w,scale)
            self.words[i]=np.asarray(new_w)

class Control_sentence:

    def __init__(self,words,freq,word_names):
        self.words=words
        self.word_names=word_names
        self.t_lengths=[]

        for word in self.words:
            self.t_lengths.append(double(word.shape[0])/freq)
        self.freq=freq
        self.length=len(self.word_names)



def s_concatenate(sentence):

    s=[]

    for word in sentence.words:
        s=concatenate([s,word])

    s_int16=zeros((s.shape[0]),dtype='int16')

    for i in range(0,s.shape[0]):
        s_int16[i]=s[i]

    wavfile.write("test.wav",sentence.freq,s_int16)

def main(argv):

   base_l=0.15
   new_l_av=0.2
   k=5
   theta=new_l_av/k

   sentence_file = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["sfile="])
   except getopt.GetoptError:
      print 'load_sentence.py -i <sentence_file>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
          print 'load_sentence.py -i <sentence_file>'
          sys.exit()
      elif opt in ("-i", "--sfile"):
         sentence_file = arg
   print 'Sentence file is ', sentence_file
   s=Sentence(sentence_file)


   #s.stretch(new_l)

   simple_shorten=False

   if simple_shorten:
       ms=0.001
       stride=15*ms

       s.shorten(new_l,stride)
       
       control_words=[]
       for i in range(0,s.length):
           control_words.append(s.words[i])

       control_s=Control_sentence(control_words,s.freq,s.word_names)
       s_concatenate(control_s)
   
   else:
          
       control_words=[]
       for i in range(0,s.length):
           new_l=base_l+gammavariate(k,theta)
           print new_l,
           control_words.append(control(s.freq,s.words[i],new_l))
       print "\n"

       control_s=Control_sentence(control_words,s.freq,s.word_names)
       s_concatenate(control_s)
       


#   s_concatenate(s)


if __name__ == "__main__":
    main(sys.argv[1:])
