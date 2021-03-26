import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import sawtooth
from scipy.integrate import simps

def plot(cumPOUND_score):
    L=1
    freq=2
    width_range=1
    samples=1000
    terms=int(np.round(10*(-1*cumPOUND_score+1)+1)) #some sort of mapping from cumpound score

    # Periodicity of the periodic function f(x)
    # No of waves in time period L
    # Generation of Sawtooth function
    x=np.linspace(0,L,samples,endpoint=False)
    y=sawtooth(2.0*np.pi*x*freq/L,width=width_range)

    # Calculation of Co-efficients
    a0=2./L*simps(y,x)
    an=lambda n:2.0/L*simps(y*np.cos(2.*np.pi*n*x/L),x)
    bn=lambda n:2.0/L*simps(y*np.sin(2.*np.pi*n*x/L),x)

    # Sum of the series
    s=a0/2.+sum([an(k)*np.cos(2.*np.pi*k*x/L)+bn(k)*np.sin(2.*np.pi*k*x/L) for k in range(1,terms+1)])

    # Plotting
    plt.plot(x,s,label="Fourier series")
    plt.xlabel("$x$")
    plt.ylabel("$y=f(x)$")
    plt.legend(loc='best',prop={'size':10})
    plt.title("Sawtooth wave signal analysis by Fouries series")
    plt.savefig("fs_sawtooth.png")
    return "fs_sawtooth.png"