import pandas as pd
import numpy as np
import trackpy as tp
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob

#def D(temps,gamma=1e-7,K=1.7e-5):
#    kb = 1.38e-23
#    A = 1e12*kb/np.sqrt(np.pi*gamma*K)
#    return [A*temp for temp in temps]

def D(temps,gamma=1e-7):
    kb = 1.38e-23
    A = 1e12*kb/gamma
    return [A*temp for temp in temps]

path = '/research2/shared/cwseitz/Data/MD/'
msd_files = glob (path+'*-msd.csv')
msd_files = sorted(set([msd_file.split('-')[0] for msd_file in msd_files]))

palette = plt.cm.tab10.colors
avg_msds = []
std_msds = []
fig,ax=plt.subplots()

dt = 1e-4
for i, msd_file in enumerate(msd_files):
    print(f'Reading group: {msd_file}')
    group = glob(msd_file+'*-msd.csv')
    imsds = []
    for j,file in enumerate(group):
        imsd = pd.read_csv(file)
        imsds.append(imsd)
    imsds = pd.concat(imsds,axis=1)
    lag = imsds['lag time [s]']
    imsds = imsds.drop('lag time [s]', axis=1)
    avg_msd = np.mean(imsds.values, axis=1)
    std_msd = np.std(imsds.values,axis=1)/np.sqrt(imsd.shape[1])
    avg_msds.append(avg_msd[-1]); std_msds.append(std_msd[-1])
    color = palette[i % len(palette)]
    x = np.arange(0,len(avg_msd),1)*dt
    #ax.errorbar(x,avg_msd,yerr=std_msd,capsize=5,color=color,label=group)
    ax.plot(x,avg_msd,color=color,label=group)
    #ax.plot(x,imsds.values,color=color)

temperatures = [310]
Ds = D(temperatures)
print(Ds)
ax.set_xlabel(r'lag $\tau$ (sec)')
ax.set_ylabel(r'$\langle \Delta r^2\rangle [\mu \mathrm{m}^2]$')
#ax.set_xscale('log')
#ax.set_yscale('log')
#ax.legend()
#ax.set_ylim([0,1.0])
plt.show()

