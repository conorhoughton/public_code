#230 and 3800 

bands=[]
a=pow(600/40,1/15.)
from math import *
b=40.
d=b
c=230
old_c=c
for i in range(0,16):
    c=c+b
    bands.append([old_c,c])
    old_c=c
    b=b*a
    d=b
    b=(round(b/10))*10.
    if b==80: 
        b=90
    if b==160:
        b=150
    if b==310:
        b=300
    if b==620:
        b=600

print bands
