import pandas as pd
import numpy as np
from glob import glob

path = '/research2/shared/cwseitz/Data/MD/'
dump_files = glob(path+'*.DNA')
lhead = 9

for xyz in dump_files:
    print(f'Reading dump file: {xyz}')
    nums = xyz.split('-')[0].split('_')[2:4]
    nums = [int(num) for num in nums]
    num_atoms = sum(nums) + 320

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

