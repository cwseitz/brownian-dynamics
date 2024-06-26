import pandas as pd
import numpy as np
import trackpy as tp
import matplotlib.pyplot as plt
from glob import glob
from fit_msd import *


def read_dump(path,num_atoms,lhead=9):
    dump_files = glob(path+'*.DNA')
    for xyz in dump_files:
        print(f'Reading dump file: {xyz}')
        with open(xyz,'r') as file:
            lines = file.readlines()
            nlines = len(lines)
        sublist_size = num_atoms+lhead
        sublists = [lines[i:i + sublist_size] for i in range(0, nlines, sublist_size)]
        dfs = []
        for n,timestep_data in enumerate(sublists):
            stripped = [s.strip().split(' ') for s in timestep_data][lhead:]
            df = pd.DataFrame(stripped, columns=["particle", "type", "x", "y", "z"])
            df = df.apply(pd.to_numeric)
            df['x'] = df['x']
            df['y'] = df['y']
            df['z'] = df['z']
            df['frame'] = n
            dfs.append(df)
        out = pd.concat(dfs, ignore_index=True)
        out.to_csv(xyz.replace('.DNA','.csv'))
        
def imsd(config,types=[1]):
    read_dump(config['path'],config['num_atoms'])
    pos = ['x','y','z']
    dump_files = glob(config['path']+'*.csv')
    for xyz in dump_files:
        print(f'Reading dump file: {xyz}')
        df = pd.read_csv(xyz)
        df = df.sort_values('particle')
        df = df.loc[df['frame'] >= config['tburn']]
        df['frame'] = df['frame']-config['tburn']
        df = df[df['type'].isin(types)]
        df = df.sort_values('frame')
        df['x'] = df['x']; df['y'] = df['y']; df['z'] = df['z']
        imsd = tp.imsd(df,config['mpp'],config['fps'],
                       max_lagtime=config['max_lag'],pos_columns=pos)
        imsd.to_csv('-msd.'.join(xyz.split('.')))

def plot_imsd(config,multiplier=1e12):
    msd_files = glob (config['path']+'*-msd.csv')
    msd_files = sorted(set([msd_file.split('-')[0] for msd_file in msd_files]))
    palette = plt.cm.tab10.colors
    avg_msds = []; std_msds = []
    fig,ax=plt.subplots()

    for i, msd_file in enumerate(msd_files):
        print(f'Reading group: {msd_file}')
        group = glob(msd_file+'*-msd.csv')
        imsds = []
        for file in group:
            imsd = pd.read_csv(file)
            tau = imsd['lag time [s]']*config['timestep']
            imsd = imsd.drop('lag time [s]', axis=1)
            imsds.append(imsd)
        imsds = pd.concat(imsds,axis=1)
        thetas = fit_log_msd(tau.values,imsds)
        avg_msd = np.mean(imsds.values, axis=1)
        std_msd = np.std(imsds.values,axis=1)/np.sqrt(imsds.shape[1])
        avg_msds.append(avg_msd[-1]); std_msds.append(std_msd[-1])
        color = palette[i % len(palette)]
        #ax.plot(tau,multiplier*imsds.values,color='black',alpha=0.2)
        ax.plot(tau,multiplier*avg_msd,color=color)
        ax.plot(tau,multiplier*power_law(tau, D, alpha), linestyle='--', color=color,label=f'{D}')
    #ax.set_title(f'D={np.round(D*multiplier,4)},alpha={alpha}')
    ax.set_xlabel(r'lag $\tau$ (sec)')
    ax.set_ylabel(r'$\langle \Delta r^2\rangle [\mu \mathrm{m}^2]$')
    #ax.set_xscale('log')
    #ax.set_yscale('log')
    ax.legend()
    plt.tight_layout()
    plt.show()
    
    
def plot_D(config,ax,temps,color='red',marker='o'):
    msd_files = glob (config['path']+'*-msd.csv')
    msd_files = sorted(set([msd_file.split('-')[0] for msd_file in msd_files]))
    avgD = []; stdD = []
    for i, msd_file in enumerate(msd_files):
        print(f'Reading group: {msd_file}')
        group = glob(msd_file+'*-msd.csv')
        imsds = []
        for file in group:
            imsd = pd.read_csv(file)
            tau = imsd['lag time [s]']*config['timestep']
            imsd = imsd.drop('lag time [s]', axis=1)
            imsds.append(imsd)
        imsds = pd.concat(imsds,axis=1)
        thetas = fit_log_msd(tau.values,imsds.values)
        avgD.append(1e6*np.mean(thetas[:,0]))
        stdD.append(1e6*np.std(thetas[:,0])/np.sqrt(thetas.shape[0]))
    ax.errorbar(temps,avgD,yerr=stdD,capsize=5.0,
                markersize=5,color=color,marker=marker)
