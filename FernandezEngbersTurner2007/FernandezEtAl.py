import numpy as np
from scipy.integrate import ode


from Sigma import *
from Channel import *
from Units import *
from Parameters import *


class Somatic_voltage:

    def __init__(self,c,r,g_na,g_ks,g_leak,g_ih,e_na,e_k,e_leak,e_ih,i_e,v_initial):

        self.c=c
        self.r=r
        self.g_na=g_na
        self.g_k=g_ks
        self.g_leak=g_leak
        self.g_ih=g_ih
        self.e_na=e_na
        self.e_k=e_k
        self.e_leak=e_leak
        self.e_ih=e_ih
        self.i_e=i_e

        self.v_initial=v_initial

    def derivative(self,m,h,ih,v_soma,v_dendrite,t):

        i_dend=-(v_soma-v_dendrite)/self.r
        i_na=-self.g_na*m*h*  (v_soma-self.e_na)
        i_k =-self.g_k *(1-h)*(v_soma-self.e_k)
        i_ih=-self.g_ih*ih*   (v_soma-self.e_ih)
        i_leak=-self.g_leak*(v_soma-self.e_leak)

        return (self.i_e(t)+i_dend+i_na+i_k+i_ih+i_leak)/self.c


class Dendritic_voltage:

    def __init__(self,c,r,g_kd,g_leak,e_kd,e_leak,v_initial):

        self.c=c
        self.r=r
        self.g_k=g_kd
        self.g_leak=g_leak
        self.e_k=e_kd
        self.e_leak=e_leak

        self.v_initial=v_initial

    def derivative(self,n_kd,v_soma,v_dendrite):

        i_soma=-(v_dendrite-v_soma)/self.r
        i_k =-self.g_k*n_kd*(v_dendrite-self.e_k)
        i_leak=-self.g_leak*(v_dendrite-self.e_leak)

        return (i_soma+i_k+i_leak)/self.c


class All_derivatives:
    
    def __init__(self,somatic_voltage,dendritic_voltage,m,h,ih,kd):

        self.somatic_voltage=somatic_voltage
        self.dendritic_voltage=dendritic_voltage
        self.m=m
        self.h=h
        self.ih=ih
        self.kd=kd

    def __call__(self,t,y):

        v_soma=y[0]
        v_dendrite=y[1]
        h_val=y[2]
        ih_val=y[3]
        kd_val=y[4]

        v_soma_dot=self.somatic_voltage.derivative(self.m(v_soma),h_val,ih_val,v_soma,v_dendrite,t)
        v_dendrite_dot=self.dendritic_voltage.derivative(kd_val,v_soma,v_dendrite)
        h_dot=self.h.derivative(v_soma,h_val)
        ih_dot=self.ih.derivative(v_soma,ih_val)
        kd_dot=self.kd.derivative(v_soma,kd_val)

        return [v_soma_dot,v_dendrite_dot,h_dot,ih_dot,kd_dot]


m_inf=Sigma(v_half_m,k_m)
h_inf=Sigma(v_half_h,k_h)
ih_inf=Sigma(v_half_ih,k_ih)
kd_inf=Sigma(v_half_kd,k_kd)
        
i_e=Electrode()

h_channel=Channel(h_inf,tau_h,v_initial)
ih_channel=Channel(ih_inf,tau_ih,v_initial)
kd_channel=Channel(kd_inf,tau_kd,v_initial)
somatic_voltage=Somatic_voltage(c_soma,r,g_na,g_ks,g_leak,g_ih,e_na,e_k,e_leak,e_ih,i_e,v_initial)
dendritic_voltage=Dendritic_voltage(c_dendrite,r,g_kd,g_leak,e_k,e_leak,v_initial)

f=All_derivatives(somatic_voltage,dendritic_voltage,m_inf,h_channel,ih_channel,kd_channel)

y_initial=[somatic_voltage.v_initial,dendritic_voltage.v_initial,h_channel.initial,ih_channel.initial,kd_channel.initial]

t0=0
t1=t_run
dt=0.001*ms

integrator = ode(f).set_integrator('vode', method='bdf', with_jacobian=False)
integrator.set_initial_value(y_initial, t0)

while integrator.successful() and integrator.t < t1:
    integrator.integrate(integrator.t+dt)
    print integrator.t, integrator.y[0], integrator.y[1], m_inf(integrator.y[0]),integrator.y[2], integrator.y[3], integrator.y[4]


