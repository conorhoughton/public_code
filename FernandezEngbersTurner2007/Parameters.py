import numpy as np
from Units import *

v_initial=-70*mV

c_soma=1.5*uF
c_dendrite=1.5*uF

r=0.75*kOhm

g_na=40*mS

g_ks=8.75*mS
g_kd=0.6*mS

g_ih=0.03*mS
g_leak=0.032*mS

e_na=45*mv
e_k=-95*mv
e_ih=-20*mv
e_leak=-77*mv

v_half_m=-40*mv
k_m=3*mv

v_half_h=-40*mv
k_h=-3*mv

v_half_ih=-80*mv
k_ih=-3*mv

v_half_kd=-35*mv
k_kd=3*mv


def tau_h(v):
    return (295.4/(4*np.power(v/mv+50.,2)+400)+0.012)*ms

def tau_ih(v):
    return 100*ms  

def tau_kd(v):
    return 15*ms

a_70=0.17*uA


cs_times=[500*ms,1500*ms]

cs_duration=25*ms

t_run=2.5

class Electrode():

    def __call__(self,t):
        for t_cs in cs_times:
            if t>t_cs and t<t_cs+cs_duration:
                return 4.5*uA
        return 0.18*uA

if __name__=="__main__":

    v=-70*mV

    while v<50*mV:
        print v,tau_h(v)
        v+=1*mV
