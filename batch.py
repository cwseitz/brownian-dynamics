from lammps import IPyLammps
from initialize import *

def run_lammps_simulation(input_script,rep,T,num_brd4,num_pbrd4):
    lmp = IPyLammps()
    with open(input_script, 'r') as file:
        script_content = file.read()
    savepath='/research2/shared/cwseitz/Data/MD/'
    dump_filename = savepath+f'dump_100_{num_brd4}_{num_pbrd4}_{T}-{rep}.DNA'
    mod = script_content.replace("dump.DNA", dump_filename)
    Tstring = f'variable T equal {T}'
    mod = mod.replace("variable T equal 310",Tstring)
    temp_script = 'temp_script.lam'
    with open(temp_script, 'w') as file:
        file.write(mod)
    lmp.file(temp_script)
    lmp.run(1)
    lmp.close()

def run_rep(T,num_brd4,num_pbrd4):
    print(f'Simulating BRD4:{num_brd4}, pBRD4:{num_pbrd4}')
    with open("initial_configuration.txt", "w") as f:
        f = write_header(f,num_atoms_per_polymer,num_polymers,
                         num_brd4,num_pbrd4,xlo,xhi,ylo,yhi,zlo,zhi)
        f = write_atoms(f,centers,num_brd4,num_pbrd4,
                        num_polymers,num_atoms_per_polymer,
                        sigma=sigma,ax=ax,p_acetyl=p_acetyl,
                        boxhw_brd4=boxhw_brd4)
        f = write_bonds(f,num_polymers,num_atoms_per_polymer)
        f = write_angles(f,num_polymers,num_atoms_per_polymer)    
    script='polymer.lam'
    run_lammps_simulation(script,rep,T,num_brd4,num_pbrd4)
    
c = 1000.0e-9 #1um
xlo,xhi = -2*c,2*c
ylo,yhi = -2*c,2*c
zlo,zhi = -2*c,2*c
sigma = 150.0e-9 #nm
num_atoms_per_polymer = 80
num_polymers = 4
p_acetyl = 0.3
x = 0.3e-6
boxhw_brd4 = 500e-9
centers = np.array([[-x,x,0],[-x,-x,0],[x,-x,0],[x,x,0]])

num_brd4s = [0]
num_pbrd4s = [0]
temperatures = [310]
ax = plt.figure().add_subplot(projection='3d')
nreps = 10
for T in temperatures:
	for num_brd4 in num_brd4s:
		for num_pbrd4 in num_pbrd4s:
		    for rep in range(nreps):
		        run_rep(T,num_brd4,num_pbrd4)


