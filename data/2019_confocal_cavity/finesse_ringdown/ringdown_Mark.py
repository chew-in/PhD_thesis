import numpy as np
import scipy
import os
from scipy import optimize
import matplotlib.pyplot as plt

c=3e8 # m/s

def ringdown_intensity(t,F,deltaDot,t0,A,offset):
	delta=deltaDot*(t-t0)
	# delta = f0 d/L, f0 = c/wl
	# d/wl = L * delta / c
	# v = deltaDot*L/f0

	# phi1 = 2*np.pi*d/wl
	phi1=2*np.pi*L*delta/c
	# Omega = 2*v/wl
	Omega=2*deltaDot*L/c
	OOF=Omega/OmegaF
	tau=F/(2*np.pi*OmegaF)
	l=((1-1j)/(2*np.sqrt(2))*(1/(np.pi*OOF))**0.5*np.pi/F
		-(1+1j)/(2*np.sqrt(2))*((1/(np.pi*OOF))**0.5*2*phi1-(np.pi*OOF)**0.5))
	I=A*np.exp(-(t-t0)/tau)*np.abs(scipy.special.erfc(l))**2+offset
	return I



cutoff1=0
cutoff2=-1
### LOAD DATA

folder='./'
filename='DS0058.CSV'
header_rows=27
cutoff1=0
cutoff2=-1
dither_rate=2e3
#p0=[35000,dither_rate*4e9,2e-7,1.8e-1,-9e-3]
p0=[10000,2237390503089,-5e-07,0.4,0.046]
p0=[8000,3.0e12,-4.5e-07,0.45,0.046]
wl=780e-9 # m
L=5e-2 # m

OmegaF=c/(2*L)

#p[0] finesse changes both amplitude and number of rings
#p[1] deltaDot
#p[2] t0 shifts plot left or right
#p[3] A changes amplitude
#p[4] offset 


data=np.loadtxt(os.path.join(folder,filename),delimiter=',',usecols=(0,1),skiprows=header_rows)
t=data[:,0]
V=data[:,1]

# p0[-1]=V[-1]
print("the guess of (F, deltadot, t0, A, offset is)",p0)

# perform fit
fit_error_flag=False
try:
	popt,pcov=optimize.curve_fit(ringdown_intensity,t,V,p0=p0,maxfev=8000)
	print("The fitted Finesse is: ", popt[0])
	print("The fitted deltaDot is: ", popt[1])
	print("The fitted t0 is: ", popt[2])
	print("The fitted A is: ", popt[3])
	print("The fitted offset is: ", popt[4])
	print("The fitted OmegaF/popt[0] is: ", OmegaF/popt[0])
	print("The goodness of fit, I guess, is: ", np.sqrt(pcov[0,0]))
	print("The fitted popt[1]/dither_rate is: ", popt[1]/dither_rate)
except:
	print('fit error')
	fit_error_flag=True

### PLOT
# plot guess
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(t*10**6,V)	# data in dark blue
ax.plot(t*10**6,ringdown_intensity(t,*p0),'c')  # guess in cyan

# plot fit
if not fit_error_flag:
	ax.plot(t*10**6,ringdown_intensity(t,*popt),'r')	# fit in red

plt.show()
