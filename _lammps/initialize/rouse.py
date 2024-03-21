import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_polymer(pos, ax):
    ax.scatter(pos[:,0], pos[:,1], pos[:,2], s=10)
    for i in range(len(pos) - 1):
        ax.plot([pos[i][0], pos[i + 1][0]],
                [pos[i][1], pos[i + 1][1]],
                [pos[i][2], pos[i + 1][2]],
                color='black',alpha=0.3)
    plt.show()

def generate_polymer(center,num_atoms_per_polymer,sigma=1.0):
    positions = np.zeros((num_atoms_per_polymer, 3))
    displacements = np.random.normal(scale=sigma, size=(num_atoms_per_polymer, 3))
    magnitudes = np.linalg.norm(displacements, axis=1)
    displacements = (displacements.T / magnitudes * sigma).T
    for i in range(1, num_atoms_per_polymer):
        positions[i] = displacements[i]
    positions += center
    return positions

def write_header(f,num_atoms_per_polymer,boxhw):

    f.write("# LAMMPS configuration file\n")
    f.write("\n")
    f.write(f'{num_atoms_per_polymer} atoms\n')
    f.write(f'{(num_atoms_per_polymer-2)} bonds\n')
    f.write(f'{(num_atoms_per_polymer-2)} angles\n')
    f.write("\n")
    f.write('1 atom types\n')
    f.write('1 bond types\n')
    f.write('1 angle types\n')
    f.write("\n")
    f.write(f"{-boxhw} {boxhw} xlo xhi\n")
    f.write(f"{-boxhw} {boxhw} ylo yhi\n")
    f.write(f"{-boxhw} {boxhw} zlo zhi\n")
    f.write("\n")
    f.write('Masses\n')
    f.write("\n")
    f.write('1 1\n')
    return f
    
def write_atoms(f,num_atoms_per_polymer,scale,ax=None):
    f.write("\n")
    f.write("Atoms\n")
    f.write("\n")    
    atom_id = 1
    polymer_positions = generate_polymer(0.0,num_atoms_per_polymer)
    polymer_positions *= scale
    if ax is not None:
        plot_polymer(polymer_positions,ax)
    for pos in polymer_positions:
        f.write(f"{atom_id} 1 1 {pos[0]} {pos[1]} {pos[2]}\n")
        atom_id += 1
    return f
            
def write_bonds(f,num_atoms_per_polymer):
    f.write("\n")
    f.write("Bonds\n")
    f.write("\n")    
    bond_id = 1
    start = 1; stop = num_atoms_per_polymer - 1
    for n in range(start,stop):
        line = f"{bond_id} 1 {n} {n+1}\n"
        f.write(line)
        bond_id += 1
    return f
    
def write_angles(f,num_atoms_per_polymer):
    f.write("\n")
    f.write("Angles\n")
    f.write("\n")

    angle_id = 1
    start = 1; stop = num_atoms_per_polymer - 1
    for n in range(start,stop):
        line = f"{angle_id} 1 {n} {n+1} {n+2}\n"
        f.write(line)
        angle_id += 1  
    return f  
             
def initialize_rouse(f,config,ax=None):
    f = write_header(f,config['num_atoms_per_polymer'],config['boxhw'])
    f = write_atoms(f,config['num_atoms_per_polymer'],config['polymer_scale'],ax=ax)
    f = write_bonds(f,config['num_atoms_per_polymer'])
    f = write_angles(f,config['num_atoms_per_polymer'])   
    
