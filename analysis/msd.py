import pandas as pd
import numpy as np
import trackpy as tp
import matplotlib.pyplot as plt
import json
from glob import glob
from utils import *

with open('msd.json', 'r') as f:
    config = json.load(f)
    
imsd(config,types=[1,2])
#plot_imsd(config,multiplier=1e12)

temps = [280,290,300,310,320]
fig,ax=plt.subplots(figsize=(3,3))
config['path'] = '/home/cwseitz/Desktop/MD/Free/'
plot_D(config,ax,temps)
config['path'] = '/home/cwseitz/Desktop/MD/500_0/'
plot_D(config,ax,temps,color='black',marker='^')
config['path'] = '/home/cwseitz/Desktop/MD/0_500/'
plot_D(config,ax,temps,color='blue',marker='^')
ax.set_xlabel('T (K)')
ax.set_ylabel(r'$\gamma \langle D \rangle \; (\mu m^{2} /s^{2})$')
ymin,ymax = ax.get_ylim()
ax.vlines(310,ymin,ymax,linestyle='--',color='black',alpha=0.5)
ax.grid()
plt.tight_layout()
plt.show()

