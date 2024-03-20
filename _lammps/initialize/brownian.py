import numpy as np
import matplotlib.pyplot as plt

def write_header(f,num_atoms,boxhw):

    f.write("# LAMMPS configuration file\n")
    f.write("\n")
    f.write(f'{num_atoms} atoms\n')
    f.write("\n")
    f.write('1 atom types\n')
    f.write("\n")
    f.write(f"{-boxhw} {boxhw} xlo xhi\n")
    f.write(f"{-boxhw} {boxhw} ylo yhi\n")
    f.write(f"{-boxhw} {boxhw} zlo zhi\n")
    f.write("\n")
    f.write('Masses\n')
    f.write("\n")
    f.write('1 1\n')
    return f
    
def write_atoms(f,num_atoms,ax=None,sigma=1.0):
    f.write("\n")
    f.write("Atoms\n")
    f.write("\n")    
    atom_id = 1
    pos = [0,0,0]
    for n in range(num_atoms):
        f.write(f"{atom_id} 1 1 {pos[0]} {pos[1]} {pos[2]}\n")
        atom_id += 1
    return f
                         
def initialize_brownian(f,config):
    f = write_header(f,config['num_atoms'],config['boxhw'])
    f = write_atoms(f,config['num_atoms'])
    
