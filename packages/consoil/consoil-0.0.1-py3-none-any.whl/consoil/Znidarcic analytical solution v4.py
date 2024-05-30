# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 12:31:20 2023

@author: imyouri
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib import cm
import matplotlib as mpl
import os
import pandas as pd


#Defintions of variables
"""
pw, ps : densities of water and soil (g/L= kg/m**3)
vol0   : total volume fraction of clay in water (-)
C0     : total concentration of clay in water (g/L) = vol0*ps
Df, n  : Fractal dimensin and n = 2/ (3-Df)
Ksig   : constant with effective stress (Pa)
Kk     : constant with dimension of permeability (m/s)
visc   : viscosity of the medium (water) (Pa.s)
g      : gravity constant (m/s**2)
H, LG  : height of water in column and Gibson length (m)
tgel   : gelling time (s)


hws    : interface water/suspension (m)
hbs    : interface bed/suspension   (m)

timefin, dt : final time and time step (s)
nh, nt : number of step in space and time
t2c : total time until the end of consolidation

"""
pw, ps = 1e+03, 2.60e+03
C0     = 200
e0     = 4.818
LG     = 2*0.513
visc   = 1e-03
H      = LG *(1 + e0)
g      = 9.81e+0
kbt    = 1.38e-23 * (273.15 + 20)
visc   = 1e-03
radius = 30e-06

t2c = float(input('The settling and consolidation time in days : '))
t2c = t2c*3600*24

#Selecting the model in which the gibson equations will base on
mode = "Zn"


#for Merckelbach - Kranenburg (MK)
Df = 2.65
n  = 2/(3-Df)
Ksig = 1e+06
Kk   = 2e-13
'''
#For Znidarcic (Zn)
KDELsig0 = 0
Bp = 1/n
Ap = (Ksig)**(Bp)
Ak = Kk 
Bk = n
'''

Bp = 0.22501
Ap = 13.536
Ak = 4.7e-10 
Bk = 4.64116
KDELsig0 = 0



v0 = 2*radius**(2) * (ps-pw)*g /(9*visc)
D0 = kbt/ (6*3.14*visc*radius)
Pe = H* v0 /D0



#Step in space
nh = int(5e2)
z0 = 0   #z0 initial height at the bottom of the column 
zbin = np.linspace(z0, H, num= nh) # Creating nh number of z points

#Step in time
nt = int(1e3)

dttime =np.linspace(2e-1,t2c,nt)/nt
t0 = dttime[0]
time =[]
time.append(t0)
for kt in range(1,nt):
    time.append(time[kt-1]+dttime[kt])
#time = np.array(time)
#time = np.arange(z0, t2c,86.4)
time = np.linspace(z0,t2c, nt)

#The initial volume fraction of solid vol0
kmax = nh-1
volinit = C0/ps
volinit =  1/(1 + e0)
#volinit = 1/(1 + 4.818)
vol0 = np.ones(kmax)* volinit
print("the initial volume fraction is : ", volinit)

#We solve now the Gibson equation for any given time and compare the solution
#to the analytical solution MK; the permeability and effective skeleton stress
#are given by the expressions of MK, but other options are available.

def Settling_column(zbin, Phis) :
    Phis = list(Phis)
    rmax = max(Phis)
    
    norm = mpl.colors.Normalize(vmin=0,vmax= 0.175)
    cmap = cm.jet
    m = cm.ScalarMappable(norm=norm, cmap=cmap)

    fig , ax= plt.subplots()
    step = (H-z0)/(nh-1)
    for k in range(len(zbin)-1) :
        step = zbin[k+1] - zbin[k]
        c = Phis[k]
        color = m.to_rgba(c, alpha = None)
        rectangle = plt.Rectangle((0,zbin[k]), 5, step , edgecolor='black', linewidth= 0.25, fc= color)
        ax.add_patch(rectangle)
    ax.set_ylabel("Height of the column z")
    ax.set_ylim(0,H)
    ax.set_xlim(0,H/4)
    plt.xticks([])
    plt.colorbar(m)
    plt.title("Volume fraction in term of Height of soil based on Euler Model")
    
        

def advection(phi0k, mode):
    eps = 0
    if mode == "CS" :
        m = 4
        return v0 * (1 - phi0k)**(m)
    if mode == "MK" :
        return Kk * ((max(phi0k,eps))**(1-n)) * ((ps - pw)/(v0*pw)) 
    if mode == "Zn" :
        return Ak * ((1-phi0k)/max(eps,phi0k))**(Bk) * ((ps-pw)/(v0*pw)) * phi0k
    
def diffusion(phi0k, mode):
    eps = 0

    if mode == "CS" :
        return (D0/v0) * ((1+ phi0k + (phi0k)**(2) - (phi0k)**(3))/(1 - (phi0k)**(3)))
    if mode == "MK" :
        return Ksig * (v0/D0)*((phi0k)**(n-1)) * (1/(g*(ps - pw)))
    if mode == "Zn" :
        KDELsig= (Ap*phi0k/(1-phi0k))**(1/Bp) - KDELsig0
        return v0/(D0*g*(ps-pw))*(KDELsig)/max(eps,phi0k)

def Ddiffusion(phi0k, mode):
    eps = 0
    if mode == "CS" :
        return (D0/v0) * ((1+ phi0k + (phi0k)**(2) - (phi0k)**(3))/(1 - (phi0k)**(3)))
    if mode == "MK" :
        dg= (v0/D0)*(n-1)*Ksig * ((phi0k)**(n-2)) * (1/(g*(ps - pw)))
        return (dg * phi0k) + diffusion(phi0k, mode)
        
    if mode == "Zn" :
        KDELsig= (Ap*phi0k/(1-phi0k))**(1/Bp) - KDELsig0
        dg = v0/(D0*g*(ps-pw))*(Ap**(1/Bp) * (1/Bp) * (1/(1-phi0k))**(2) * (phi0k/(1-phi0k))**(1/Bp - 1) * (1/phi0k) - KDELsig * (1/phi0k)**(2))
        return (dg * phi0k) + diffusion(phi0k, mode) 
#                        Solving the consolidation equation 
#                                  IMPLICIT METHOD
#                        SOLVING  AXn = Yn + Cextn => Xn = inv(A) Yn + inv(A) Cextn


Cext = np.zeros(nh-1) #Boundary Condition
Y = vol0


hws = []
hsb = []

for k in range(0,nt) :
    a=[]
    b=[]
    c=[]
    dd=[]
    #Defining dz and dt
    deltaZ = H/(nh-1)
    deltaT = time[1]-time[0]
    #Defining (nh-1) X (nh-1) Matrice : M
    M = []
    #first row of M matrix
    
    dZvol = deltaZ * volinit
    
    divb = 0
    divt = D0*advection(Y[0],mode) * Ddiffusion(Y[1], mode)* Y[0]**(2) 
    advb = 0
    advt = v0*advection(Y[0], mode)*Y[0]**(2) 
    
    a1 = 0
    b1 = divt
    c1 = - divt
    dd1 = dZvol * advt 
    
    """
    sigBase = (ps - pw ) *g * volinit * H 
    eBase   = Ap * (sigBase - KDELsig0)**(-Bp)
    a1 = 0 
    b1 = 1
    c1 = 0
    dd1 = 1/(1+eBase)
    """
    a.append(a1)
    b.append(b1)
    c.append(c1)
    dd.append(dd1)


    #rows from 2nd to (kmax) row
    for i in range(1,kmax-1) :
        dZvol = deltaZ * volinit
        divb = D0*advection(Y[i-1],mode) * Ddiffusion(Y[i], mode)*Y[i]**(2) / dZvol
        divt = D0*advection(Y[i],mode) * Ddiffusion(Y[i+1], mode)*Y[i]**(2) / dZvol
        advb = v0*advection(Y[i-1], mode)*Y[i]**(2)
        advt = v0*advection(Y[i], mode)*Y[i]**(2)
        
        ai = -divb
        bi = (dZvol/deltaT) + divt + divb 
        ci = - divt
        ddi = (dZvol/deltaT) *Y[i] - advb + advt
        
        
        a.append(ai)
        b.append(bi)
        c.append(ci)
        dd.append(ddi)
        
        
        

    #Last row of the martix 
    ifinal = kmax - 1 
    dZvol = deltaZ * volinit
    divb = D0*advection(Y[ifinal-1],mode) * Ddiffusion(Y[ifinal], mode) * Y[ifinal]**(2) / dZvol
    divt = 0
    advb = v0*advection(Y[ifinal-1], mode)* Y[ifinal]**(2)
    advt = 0

    af = 0
    bf = 1
    cf = 0
    ddf = volinit

    

    a.append(af)
    b.append(bf)
    c.append(cf)
    dd.append(ddf)
    


    #SWEEP Method : invert the matrix
    c[0] = c[0]/b[0]
    dd[0] = dd[0]/b[0]

    for m in range(1,len(a)):
        b[m] = b[m] - a[m] * c[m-1]
        c[m] = c[m]/ b[m]
        dd[m] = (dd[m]-dd[m-1] * a[m])/b[m]
    
    for m in range(len(a)-2,-1,-1):
        dd[m] = dd[m] - c[m] * dd[m+1]
    
    for m in range(0,len(a)):
        Y[m] = dd[m]
    


Z = []
zs = 0
da = zbin[1]- zbin[0]
for i in range(len(zbin)-1):
    dzs = da * volinit/Y[i]
    zs = zs + dzs
    Z.append(zs)


#effective stress for all (nh-1) sublayers
Sig    = []
Void   = []
Phis   = []
Heights = []
sig0   = 0

for i in range(nh):
    sig = sig0 + ((LG/(nh-1)) * (ps - pw) * g)
    e   = Ap * (sig - KDELsig0)**(-Bp)
    dh  = (LG/(nh-1)) * (1 + e)
    phi = 1/(1+e)
    Heights.append(dh)
    Sig.append(sig)
    Void.append(e)
    Phis.append(phi)
    sig0 = sig
    
print(i)
#Positions for each sublayer 
zi = 0
Z0 = [zi]
for i in range(len(Void)-1, -1 , -1): 
    zi = zi + (LG/(nh-1)) * (1 + Void[i])
    Z0.append(zi)
Z0 = Z0[::-1]

fig, ax_fis_z= plt.subplots()
ax_fis_z.scatter(Y, Z)
ax_fis_z.scatter(Phis,Z0[1:])
ax_fis_z.set_ylim(0,H)
ax_fis_z.set_xlim(0,)




import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib import cm
import matplotlib as mpl
import pandas as pd

f = open('C:/Users/imyouri/OneDrive - Delft University of Technology/Documents/Delcon/transfer_2165292_files_7dd04a47/Test/Python VDRATIO/VoidRatio.txt', 'r')
Heights = []
VR = []
Phis = []
while True : 
    line = f.readline()
    if not line :
        break
    line0 = line.strip()
    L  = line0.split()
    h = float(L[1])
    e = float(L[3])
    fi= 1/(1+e)
    Heights.append(h)
    VR.append(e)
    Phis.append(fi)

ax_fis_z.scatter(Phis, Heights)

#ax.set_ylim(0,0.12)
#ax.set_xlim(0.20,0.40)
       



#ax_fis_z.set_title("Solid volume fraction profil as a function of Height with phi0 = "+ str(round(volinit,3)) +" in "+ mode +"mode", fontsize= '16')
ax_fis_z.set_xlim(0.20,0.40)
ax_fis_z.set_ylim(0,H)
ax_fis_z.set_xlabel("Solid Volume fraction in [-]", fontsize = '16')
ax_fis_z.set_ylabel("Height in m", fontsize = '16')
ax_fis_z.legend([''],loc = 'center right')
ax_fis_z.axvline(x = volinit , color = 'r', )
ax_fis_z.legend(['Numerical solution end of consolidation', 'Analytical solution end of consolidation','Delcon end of consolidation'],loc = 'upper right')

fig0 ,ax0 = plt.subplots()
ax0.plot( Y, zbin[1:])
ax0.set_ylabel('Gibson Height in m',fontsize= 20)
ax0.set_xlabel('Volume fraction in [-]',fontsize = 20)
ax0.set_xlim(0.15,0.40)
plt.show()        