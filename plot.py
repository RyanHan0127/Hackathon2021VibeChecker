# Most of this code is taken from
# Bhar, Shyamal. "Analysis of Fourier series using Python Code"
# Department of Physics, Vidyasagar College for Women, Kolkata - 700 006

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import sawtooth
from scipy.integrate import simps

def plot(cumPOUND_score):
    L=1
    freq=5
    width_range=1
    samples=1000
    cps = (cumPOUND_score+1)/2
    if cps > 0.6:
        terms = 1
    elif cps > 0.4:
        terms = 2
    elif cps > 0.3:
        terms = 3
    elif cps > 0.2:
        terms = 5
    elif cps > 0.1:
        terms = 10
    else:
        terms = 40

    # Periodicity of the periodic function f(x)
    # No of waves in time period L
    # Generation of Sawtooth function
    x=np.linspace(0,L*freq,samples,endpoint=False)
    y=sawtooth(2.0*np.pi*x*freq/L,width=width_range)

    # Calculation of Co-efficients
    a0=2./L*simps(y,x)
    an=lambda n:2.0/L*simps(y*np.cos(2.*np.pi*n*x/L),x)
    bn=lambda n:2.0/L*simps(y*np.sin(2.*np.pi*n*x/L),x)

    # Sum of the series
    s=a0/2.+sum([an(k)*np.cos(2.*np.pi*k*x/L)+bn(k)*np.sin(2.*np.pi*k*x/L) for k in range(1,terms+1)])

    # Plotting
    plt.figure()
    plt.xticks([])
    plt.yticks([])
    plt.plot(x,s)
    plt.savefig("fs_sawtooth.png", bbox_inches="tight", pad_inches=0)
    return "fs_sawtooth.png"
