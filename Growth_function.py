#%%
# Useful libraries
import math as m
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import pandas as pd

# User imput variables
time = 200 #s  - input desired duration
n_0 = 0  #input how many nucleations are already present
c_k = 1.1 #concentratiosn of precipitant - should be in kmol/m³
co_k = 1 #100% saturation - should be in kmol/m³
S = c_k/co_k

#growth
k_grow =3 #mol/m²/s
n = 2 #reaction constant

#constants
R = 8314.4 #J/K / kmol
T = 298 #K
surf_energy = 0.54 #J / m² temp data for lithium... (http://crystalium.materialsvirtuallab.org/)
MW = 45.881 #kg/kmol
den =2310 #kg/m³ 2.31 #g/cm³
mol_vol = MW/den #m³/kmol
timespan = [0,time]

#intializing constants
initial = {}
initial['r_0'] = 2**surf_energy*(1/mol_vol)/(R*T*m.log(S)) #m
#initial['n_0'] =0 #nuclations
initial['S'] = c_k/co_k #unitless
sol_vec = list(initial.values())  # solution vector
print(sol_vec)

V_elect = 0.0005  #volume electrolyte m³
#will vary at some point?
A_spec = (10*initial['r_0'])**2/(V_elect) #Specific surface of reaction (m²/m³) using r_0 for scale
int_volume =  2/3*initial['r_0']**3
nuclii = 10
print (A_spec)

#%%

def growth(t,varbs_array):
    radius, conc = varbs_array #indicates variable array because I forget
    drad_dt = m.tanh(4*conc)*mol_vol*k_grow*(conc-1)**n
    dconc_dt = - m.tanh(4*conc)*nuclii*(drad_dt*2*m.pi*radius**2)/mol_vol/V_elect/co_k # distrute change in mass to electrolyte
    return [drad_dt, dconc_dt]

growth_sen = solve_ivp(growth, timespan, sol_vec) #growth senario

radius = growth_sen.y[0]
con = growth_sen.y[1]
t = growth_sen.t
plt.figure(0)
plt.plot(t,radius)
plt.figure(1)
plt.plot(t,con)

# %%