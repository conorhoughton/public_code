import sys, getopt
import matplotlib.pyplot as plt
from pylab import *
from bands import *
from envelope_noise import *
from scipy.io import wavfile
import numpy as np

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

   

   control_words=[]
   for i in range(0,s.length):
       control_words.append(control(s.freq,s.words[i],s.word_names[i]))

   control_s=Control_sentence(control_words,s.freq,s.word_names)
   s_concatenate(control_s)


if __name__ == "__main__":
    print bands
    main(sys.argv[1:])
