from lammps import IPyLammps
from .initialize import rouse, brownian, binders
import matplotlib.pyplot as plt
import os

class Brownian:
    def __init__(self,config):
        self.config = config
        self.file = '_lammps/scripts/brownian.lam'
        self.initialize()
    def initialize(self):
        config = self.config
        with open("_lammps/initialize/init_brownian.txt", "w") as f:
            f = brownian.initialize_brownian(f,self.config) 
    def scale(self,dump_file):
        new_bounds = "-1.0 1.0"
        with open(dump_file, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if line.startswith("ITEM: BOX BOUNDS"):
                lines[i+1] = lines[i+2] = lines[i+3] = f"{new_bounds}\n"
        with open(dump_file, 'w') as file:
            file.writelines(lines)

    def run(self):
        config = self.config
        for n in range(config['nreps']):
            with open(self.file, 'r') as f:
                mod = f.read() 
                T = config['T']
                mod = mod.replace("TEMPERATURE", str(config['T']))
                mod = mod.replace("CUTOFF", str(config['cutoff']))
                mod = mod.replace("NEIGHBOR", str(config['neighbor']) )
                mod = mod.replace("GAMMA", str(config['gamma']))
                mod = mod.replace("TIMESTEP", str(config['timestep']))
                mod = mod.replace("NSTEPS", str(config['nsteps'])) 
                dump_name = config['savepath']+f'dump_{T}-{n}.DNA'
                sdump_name = config['savepath']+f'dump_scaled_{T}-{n}.DNA'
                mod = mod.replace("DUMPNAME", dump_name)
                mod = mod.replace("SCALED_WRAPPED", sdump_name)
                temp = 'temp.lam'
                with open(temp, 'w') as file:
                    file.write(mod)
                lmp = IPyLammps()
                lmp.file(temp); lmp.run(1)
                lmp.close(); os.remove(temp)
                self.scale(sdump_name)
                    
class Rouse:
    def __init__(self,config):
        self.config = config
        self.file = '_lammps/scripts/rouse.lam'
        self.initialize()
    def initialize(self,ax=None):
        config = self.config
        #ax = plt.figure().add_subplot(projection='3d')
        with open("_lammps/initialize/init_rouse.txt", "w") as f:
            f = rouse.initialize_rouse(f,self.config,ax=ax) 
    def scale(self,dump_file,lheader=9):
        new_bounds = "0.0 1.0"
        with open(dump_file, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if line.startswith("ITEM: BOX BOUNDS"):
                lines[i+1] = lines[i+2] = lines[i+3] = f"{new_bounds}\n"
        with open(dump_file, 'w') as file:
            file.writelines(lines) 
    def run(self):
        config = self.config
        for n in range(config['nreps']):
            with open(self.file, 'r') as f:
                mod = f.read() 
                T = config['T']
                mod = mod.replace("TEMPERATURE", str(config['T']))
                mod = mod.replace("CUTOFF", str(config['cutoff']))
                mod = mod.replace("SIGMA", str(config['sigma']))
                mod = mod.replace("NEIGHBOR", str(config['neighbor']) )
                mod = mod.replace("GAMMA", str(config['gamma']))
                mod = mod.replace("TIMESTEP", str(config['timestep']))
                mod = mod.replace("NSTEPS", str(config['nsteps']))
                mod = mod.replace("KAPPA", str(config['kappa']))
                mod = mod.replace("EVERY", str(config['dump_every']))
                dump_name = config['savepath']+f'dump_{T}-{n}.DNA'
                sdump_name = config['savepath']+f'dump_scaled_{T}-{n}.DNA'
                mod = mod.replace("DUMPNAME", dump_name)
                mod = mod.replace("SCALED_WRAPPED", sdump_name)
                temp = 'temp.lam'
                with open(temp, 'w') as file:
                    file.write(mod)
                lmp = IPyLammps()
                lmp.file(temp); lmp.run(1)
                lmp.close(); os.remove(temp)
                self.scale(sdump_name)

class Binders:
    def __init__(self,config):
        self.config = config
        self.file = '_lammps/scripts/binders.lam'
        self.initialize()
    def initialize(self,ax=None):
        config = self.config
        #ax = plt.figure().add_subplot(projection='3d')
        with open("_lammps/initialize/init_binders.txt", "w") as f:
            f = binders.initialize_binders(f,self.config,ax=ax) 
    def scale(self,dump_file,lheader=9):
        new_bounds = "0.0 1.0"
        with open(dump_file, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if line.startswith("ITEM: BOX BOUNDS"):
                lines[i+1] = lines[i+2] = lines[i+3] = f"{new_bounds}\n"
        with open(dump_file, 'w') as file:
            file.writelines(lines) 
    def run(self):
        config = self.config
        for T in self.config['T']:
            for n in range(config['nreps']):
                with open(self.file, 'r') as f:
                    mod = f.read() 
                    mod = mod.replace("TEMPERATURE", str(T))
                    mod = mod.replace("CUTOFF", str(config['cutoff']))
                    mod = mod.replace("SIGMA", str(config['sigma']))
                    mod = mod.replace("NEIGHBOR", str(config['neighbor']) )
                    mod = mod.replace("GAMMA", str(config['gamma']))
                    mod = mod.replace("TIMESTEP", str(config['timestep']))
                    mod = mod.replace("NSTEPS", str(config['nsteps']))
                    mod = mod.replace("KAPPA", str(config['kappa']))
                    mod = mod.replace("EVERY", str(config['dump_every']))
                    dump_name = config['savepath']+f'dump_{T}-{n}.DNA'
                    sdump_name = config['savepath']+f'dump_scaled_{T}-{n}.DNA'
                    mod = mod.replace("DUMPNAME", dump_name)
                    mod = mod.replace("SCALED_WRAPPED", sdump_name)
                    temp = 'temp.lam'
                    with open(temp, 'w') as file:
                        file.write(mod)
                    lmp = IPyLammps()
                    lmp.file(temp); lmp.run(1)
                    lmp.close(); os.remove(temp)
                    #self.scale(sdump_name)                


