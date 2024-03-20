import pandas as pd
import numpy as np
import trackpy as tp
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob

mpp = fps = 1
max_lag = 100 #frames
pos = ['x','y','z']
path = '/research2/shared/cwseitz/Data/MD/'
dump_files = glob (path+'*.csv')

for xyz in dump_files:
    print(f'Reading dump file: {xyz}')
    df = pd.read_csv(xyz)
    df = df.sort_values('particle')
    df = df.loc[df['frame'] >= 9000]
    df['frame'] = df['frame']-9000
    df = df.loc[(df['type'] == 1) | (df['type'] == 2)]
    df = df.sort_values('frame')
    df['x'] = df['x']*1e6 #convert to microns
    df['y'] = df['y']*1e6
    df['z'] = df['z']*1e6
    imsd = tp.imsd(df,mpp,fps,max_lagtime=max_lag,pos_columns=pos)
    imsd.to_csv('-msd.'.join(xyz.split('.')))



