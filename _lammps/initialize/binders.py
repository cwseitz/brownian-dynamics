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

def generate_polymer(center, num_atoms_per_polymer, R=0.5, sigma=0.1):
    positions = np.zeros((num_atoms_per_polymer, 3))
    displacements = np.random.normal(scale=sigma, size=(num_atoms_per_polymer, 3))
    for i in range(1, num_atoms_per_polymer):
        new_position = displacements[i] + positions[i-1]
        r = np.linalg.norm(new_position)
        if r > R:
            displacements[i] *= -1
            new_position = displacements[i] + positions[i-1]
        positions[i] = new_position
    positions += center
    return positions

def write_header(f,num_atoms_per_polymer,num_c,num_d,boxhw):

    f.write("# LAMMPS configuration file\n")
    f.write("\n")
    f.write(f'{num_atoms_per_polymer + num_c + num_d} atoms\n')
    f.write(f'{(num_atoms_per_polymer-2)} bonds\n')
    f.write(f'{(num_atoms_per_polymer-2)} angles\n')
    f.write("\n")
    f.write('4 atom types\n')
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
    f.write('2 1\n')
    f.write('3 1\n')
    f.write('4 1\n')
    return f
    
def write_atoms(f,num_c,num_d,num_atoms_per_polymer,scale,
                boxhw=1.0,boxhw_binders=1.0,ax=None,p_acetyl=0.2):
    f.write("\n")
    f.write("Atoms\n")
    f.write("\n")    
    atom_id = 1
    center = [boxhw,boxhw,boxhw]
    polymer_positions = generate_polymer(center,num_atoms_per_polymer)
    polymer_positions *= scale
    if ax is not None:
        plot_polymer(polymer_positions,ax)
    for pos in polymer_positions:
        ptype = 1
        if np.random.uniform(0,1) < p_acetyl:
            ptype = 2
        f.write(f"{atom_id} {1} {ptype} {pos[0]} {pos[1]} {pos[2]}\n")
        atom_id += 1
    for n in range(num_c):
        r = np.random.uniform(-boxhw_binders,boxhw_binders,size=(3,))
        f.write(f"{atom_id} {n + 2} 3 {r[0]} {r[1]} {r[2]}\n")
        atom_id += 1
    for n in range(num_d):
        r = np.random.uniform(-boxhw_binders,boxhw_binders,size=(3,))
        f.write(f"{atom_id} {n + 2} 4 {r[0]} {r[1]} {r[2]}\n")
        atom_id += 1
    plt.show()
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
             
def initialize_binders(f,config,ax=None):
    f = write_header(f,config['num_atoms_per_polymer'],
                     config['num_c'],config['num_d'],config['boxhw'])
    f = write_atoms(f,config['num_c'],config['num_d'],
                      config['num_atoms_per_polymer'],
                      config['polymer_scale'],
                      boxhw=config['boxhw'],
                      boxhw_binders=config['boxhw_binders'],
                      p_acetyl=config['p_acetyl'],ax=ax)
    f = write_bonds(f,config['num_atoms_per_polymer'])
    f = write_angles(f,config['num_atoms_per_polymer'])   
    
    
