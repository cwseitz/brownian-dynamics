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

def write_header(f,num_atoms_per_polymer,num_polymers,num_brd4,num_pbrd4,
             xlo,xhi,ylo,yhi,zlo,zhi):

    f.write("# LAMMPS configuration file\n")
    f.write("\n")
    f.write(f'{num_atoms_per_polymer*num_polymers + num_brd4 + num_pbrd4} atoms\n')
    f.write(f'{(num_atoms_per_polymer-2)*num_polymers} bonds\n')
    f.write(f'{(num_atoms_per_polymer-2)*num_polymers} angles\n')
    f.write("\n")
    f.write('4 atom types\n')
    f.write('1 bond types\n')
    f.write('1 angle types\n')
    f.write("\n")
    f.write(f"{xlo} {xhi} xlo xhi\n")
    f.write(f"{ylo} {yhi} ylo yhi\n")
    f.write(f"{zlo} {zhi} zlo zhi\n")
    f.write("\n")
    f.write('Masses\n')
    f.write("\n")
    f.write('1 1\n')
    f.write('2 1\n')
    f.write('3 1\n')
    f.write('4 1\n')
    return f
    
def write_atoms(f,centers,num_brd4,num_pbrd4,num_polymers,num_atoms_per_polymer,
                boxhw_brd4=10.0,ax=None,sigma=1.0,p_acetyl=0.2):
    f.write("\n")
    f.write("Atoms\n")
    f.write("\n")    
    atom_id = 1
    for polymer_id in range(num_polymers):
        polymer_positions = generate_polymer(centers[polymer_id],num_atoms_per_polymer,sigma=sigma)
        if ax is not None:
            plot_polymer(polymer_positions,ax)
        for pos in polymer_positions:
            ptype = 1
            if np.random.uniform(0,1) < p_acetyl:
                ptype = 2
            f.write(f"{atom_id} {polymer_id + 1} {ptype} {pos[0]} {pos[1]} {pos[2]}\n")
            atom_id += 1
    for n in range(num_brd4):
        r = np.random.uniform(-boxhw_brd4,boxhw_brd4,size=(3,))
        f.write(f"{atom_id} {num_polymers + n + 1} 3 {r[0]} {r[1]} {r[2]}\n")
        atom_id += 1
    for n in range(num_pbrd4):
        r = np.random.uniform(-boxhw_brd4,boxhw_brd4,size=(3,))
        f.write(f"{atom_id} {num_polymers + n + 1} 4 {r[0]} {r[1]} {r[2]}\n")
        atom_id += 1
    plt.show()
    return f
            
def write_bonds(f,num_polymers,num_atoms_per_polymer):
    f.write("\n")
    f.write("Bonds\n")
    f.write("\n")    
    bond_id = 1
    for polymer_id in range(num_polymers):
        start = polymer_id*num_atoms_per_polymer + 1
        stop = polymer_id*num_atoms_per_polymer + num_atoms_per_polymer - 1
        for n in range(start,stop):
            line = f"{bond_id} 1 {n} {n+1}\n"
            f.write(line)
            bond_id += 1
    return f
    
def write_angles(f,num_polymers,num_atoms_per_polymer):
    f.write("\n")
    f.write("Angles\n")
    f.write("\n")

    angle_id = 1
    for polymer_id in range(num_polymers):
        start = polymer_id*num_atoms_per_polymer + 1
        stop = polymer_id*num_atoms_per_polymer + num_atoms_per_polymer - 1
        for n in range(start,stop):
            line = f"{angle_id} 1 {n} {n+1} {n+2}\n"
            f.write(line)
            angle_id += 1  
    return f  
             

    
