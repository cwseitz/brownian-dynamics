from lammps import IPyLammps
from .initialize import rouse
import os

class Brownian:
    def __init__(self,config):
        self.config = config
        self.file = '_lammps/scripts/brownian.lam'
    def initialize(self):
        pass  
    def run(self):
        config = self.config
        with open(self.file, 'r') as f:
            mod = f.read() 
        dump_name = config['savepath']+f'dump_{T}-{rep}.DNA'
        mod = mod.replace("DUMPNAME", dump_name)   
        mod = mod.replace("TEMPERATURE", config['T']) 
        mod = mod.replace("CUTOFF", config['cutoff']) 
        mod = mod.replace("NEIGHBOR", config['neighbor']) 
        mod = mod.replace("GAMMA", config['gamma']) 
        mod = mod.replace("TIMESTEP", config['timestep'])
        mod = mod.replace("NSTEPS", config['nsteps']) 
        temp = 'temp.lam'
        with open(temp, 'w') as file:
            file.write(mod)
        lmp = IPyLammps()
        lmp.file(temp); lmp.run(1)
        lmp.close(); os.remove(temp)
                    
class Rouse:
    def __init__(self,config):
        self.config = config
        self.file = '_lammps/scripts/rouse.lam'
        self.initialize()
    def initialize(self):
        config = self.config
        with open("_lammps/initialize/init_rouse.txt", "w") as f:
            f = rouse.initialize_rouse(f,self.config)  
    def run(self):
        config = self.config
        with open(self.file, 'r') as f:
            mod = f.read() 
        T = config['T']
        dump_name = config['savepath']+f'dump_{T}.DNA'
        mod = mod.replace("DUMPNAME", dump_name)   
        mod = mod.replace("TEMPERATURE", str(config['T']))
        mod = mod.replace("CUTOFF", str(config['cutoff']))
        mod = mod.replace("SIGMA", str(config['sigma']))
        mod = mod.replace("KAPPA", str(config['kappa']))
        mod = mod.replace("NEIGHBOR", str(config['neighbor']))
        mod = mod.replace("GAMMA", str(config['gamma']))
        mod = mod.replace("TIMESTEP", str(config['timestep']))
        mod = mod.replace("NSTEPS", str(config['nsteps']))
        mod = mod.replace("EVERY", str(config['dump_every']))
        temp = 'temp.lam'
        with open(temp, 'w') as file:
            file.write(mod)
        lmp = IPyLammps()
        lmp.file(temp); lmp.run(1)
        lmp.close(); os.remove(temp)



