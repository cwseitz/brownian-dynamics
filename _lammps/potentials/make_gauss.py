import numpy as np
import matplotlib.pyplot as plt

# Define parameters
num_points = 1000
r = np.linspace(1e-15, 1e-6, num_points)
sigma=200.0e-9
R0=200.0e-9
kbt = 4.2800119e-21
eps0=0.0 #Null-Interaction
eps1=10.0*kbt #AA/BB/AB
eps2=-40.0*kbt #BC
eps3=-100.0*kbt #DD
eps4=-40.0*kbt #BD

def U(r,sigma,eps,R0=1.0):
    low = R0 - sigma
    high = R0 + sigma
    u = eps*(1-((r-R0)/sigma)**2)**3
    if r < low or r > high:
        return 0.0
    else:
        return u
    
def F(r,sigma,eps,R0=1.0):
    low = R0 - sigma
    high = R0 + sigma
    f = (6*eps*(r-R0)/sigma**2)*(1-((r-R0)/sigma)**2)**2
    if r < low or r > high:
        return 0.0
    else:
        return f

fig, ax = plt.subplots(1, 2, figsize=(6, 3), sharex=True, sharey=False)
ax[0].plot(1e9*r, [U(ri, sigma, eps1, R0=R0)/kbt for ri in r], linestyle='--',color='black', label=r'$U_{CC}$')
#ax[1].plot(1e9*r, 1e12*F(r, sigma, eps1, R0=R0), color='red')
ax[0].plot(1e9*r, [U(ri, sigma, eps2, R0=R0)/kbt for ri in r], color='black', label=r'$U_{BC}$')
#ax[1].plot(1e9*r, 1e12*F(r, sigma, eps2, R0=R0), color='blue')
ax[0].plot(1e9*r, [U(ri, sigma, eps3, R0=R0)/kbt for ri in r], color='black', label=r'$U_{B_{p}B_{p}}$')
#ax[1].plot(1e9*r, 1e12*F(r, sigma, eps3, R0=R0), color='orange')
ax[0].plot(1e9*r, [U(ri, sigma, eps4, R0=R0)/kbt for ri in r], color='black', label=r'$U_{B_{p}C}$')
#ax[1].plot(1e9*r, 1e12*F(r, sigma, eps4, R0=R0), color='black')
ax[0].set_xlabel(r'$r_{ij}$ (nm)')
ax[1].set_xlabel(r'$r_{ij}$ (nm)')
ax[0].set_ylabel(r'Energy ($k_{B}T$)')
ax[1].set_ylabel(r'F ($pN$)')

fig.subplots_adjust(right=0.85)  # Adjust the right margin
ax[1].legend(bbox_to_anchor=(1.15, 1))  # Adjust bbox_to_anchor
plt.tight_layout()
plt.show()


with open('gauss.table', 'w') as f:
    f.write('GAUSS0\n')
    f.write(f'N {num_points}\n')
    f.write('\n')
    for n, ri in enumerate(r):
        f.write(f"{n+1} {ri} {U(ri,sigma,eps1,R0=R0)} {F(ri,sigma,eps1,R0=R0)}\n")
    f.write('GAUSS1\n')
    f.write(f'N {num_points}\n')
    f.write('\n')
    for n, ri in enumerate(r):
        f.write(f"{n+1} {ri} {U(ri,sigma,eps1,R0=R0)} {F(ri,sigma,eps1,R0=R0)}\n")
    f.write('GAUSS2\n')
    f.write(f'N {num_points}\n')
    f.write('\n')
    for n, ri in enumerate(r):
        f.write(f"{n+1} {ri} {U(ri,sigma,eps2,R0=R0)} {F(ri,sigma,eps2,R0=R0)}\n")
    f.write('GAUSS3\n')
    f.write(f'N {num_points}\n')
    f.write('\n')
    for n, ri in enumerate(r):
        f.write(f"{n+1} {ri} {U(ri,sigma,eps3,R0=R0)} {F(ri,sigma,eps3,R0=R0)}\n")
    f.write('GAUSS4\n')
    f.write(f'N {num_points}\n')
    f.write('\n')
    for n, ri in enumerate(r):
        f.write(f"{n+1} {ri} {U(ri,sigma,eps4,R0=R0)} {F(ri,sigma,eps4,R0=R0)}\n")
