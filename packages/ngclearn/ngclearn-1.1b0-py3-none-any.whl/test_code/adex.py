import numpy as np
import matplotlib.pyplot as plt
import sys
#import seaborn as sns

# Discretized time
T=1000
dt=.1
time=np.arange(0,T,dt)

# Applied current
Ix=np.zeros_like(time)+19

# Neuron parameters
EL=-72
taum=15
Vth=5
Vre=-75
VT=-55
D=2

# Initial condition
V0=-70

b=.75
a=.1
tauw=400

# Compute V using the forward Euler method
V=np.zeros_like(time)
w=np.zeros_like(time)
SpikeTimes=np.array([])
V[0]=V0
w[0]=0
for i in range(len(time)-1):

    # Euler step
    dv = (1./taum) * (-(V[i] - EL) + D * np.exp((V[i]-VT)/D) + Ix[i] - w[i])
    #print(-(V[i] - EL))
    V[i+1]=V[i]+dv*dt
    #print(dv)
    #sys.exit(0)
    dw = (dt/tauw) * (-w[i] + a * (V[i] - EL))
    w[i+1]=w[i]+dw

    # Threshold-reset condition
    if V[i+1]>=Vth:
        V[i+1]=Vre
        w[i+1]=w[i+1]+b
        V[i]=Vth  # This makes plots nicer
        SpikeTimes=np.append(SpikeTimes,time[i+1])

    print("{}: V {}  W {}".format(i, V[i], w[i]))
    if i == 5:
        sys.exit(0)
