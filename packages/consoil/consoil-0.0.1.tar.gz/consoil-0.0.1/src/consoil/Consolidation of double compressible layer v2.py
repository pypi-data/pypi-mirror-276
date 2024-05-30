# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 13:08:31 2024

@author: imyouri
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib import cm
import matplotlib as mpl
import os
import pandas as pd

#definition of variables for Layer1 and Layer2
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
##Water level 
hwater = 15

##Layer1 (Top)
pw, ps = 1e+03, 2.60e+03
C01    = 200
e01    = 6.0
LG1    = 0.513
#LG1    = 1.6416
visc   = 1e-03
H1     = LG1 *(1 + e01)
g      = 9.81e+0
kbt    = 1.38e-23 * (273.15 + 20)
visc   = 1e-03
radius = 30e-06
v0 = 2*radius**(2) * (ps-pw)*g /(9*visc)
D0 = kbt/ (6*3.14*visc*radius)
Pe1 = H1* v0 /D0
###for Merckelbach - Kranenburg (MK) Layer1
Df1 = 2.65
n1  = 2/(3-Df1)
Ksig1 = 1e+06
Kk1   = 2e-13
###For Znidarcic (Zn) Layer1
Bp1 = 0.15
Ap1 = 28.18383
Ak1 = 5.0e-10
Bk1 = 5.0
#KDELsig01 = -Ap1**(1/Bp1) * e01**(-1/Bp1)
KDELsig01 =  0
##Layer2 (bottom)
pw, ps = 1e+03, 2.60e+03
C02    = 200
e02    = 4.818
LG2    = 0.513
visc   = 1e-03
H2     = LG2 *(1 + e02)
g      = 9.81e+0
kbt    = 1.38e-23 * (273.15 + 20)
visc   = 1e-03
radius = 30e-06
v0 = 2*radius**(2) * (ps-pw)*g /(9*visc)
D0 = kbt/ (6*3.14*visc*radius)
Pe2 = H2* v0 /D0
###for Merckelbach - Kranenburg (MK) Layer2
Df2 = 2.65
n2  = 2/(3-Df1)
Ksig2 = 1e+06
Kk2   = 2e-13
##For Znidarcic (Zn) Layer2
Bp2 = 0.22501
Ap2 = 37.85472
Ak2 = 4.7e-10
Bk2 = 4.64116
#KDELsig02 = -Ap2**(1/Bp2) * e02**(-1/Bp2)
KDELsig02 = 0

t2c = float(input('The settling and consolidation time in days : '))
#t2c = t2c*3600*24
t2c = t2c*3600*24
#Selecting the model in which the gibson equations will base on
mode = "Zn"

#Step in space in Layer 1
nh1 = int(5e2)
z0  = 0   #z0 initial height at the bottom of the column 
zbin1 = np.linspace(z0, H1, num= nh1) # Creating nh number of z points

#Step in space in Layer 2
nh2 = int(5e2)
z0  = 0   #z0 initial height at the bottom of the column 
zbin2 = np.linspace(z0, H2, num= nh2) # Creating nh number of z points

#Step in time
nt = int(1e3)
t0 = 0
time = np.linspace(t0,t2c, nt)

#The initial volume fraction of solid for Layer 1
kmax1 = nh1-1
#volinit1 = C01/ps
volinit1 =  1/(1 + e01)
vol01 = np.ones(kmax1)* volinit1
print("the initial volume fraction for Layer 1 is : ", volinit1)

#The initial volume fraction of solid for Layer 2
kmax2 = nh2-1
#volinit2 = C02/ps
volinit2 =  1/(1 + e02)
vol02 = np.ones(kmax2)* volinit2
print("the initial volume fraction for Layer 2 is : ", volinit2)

#We solve now the Gibson equation for any given time and compare the solution
#for Layer 1 and Layer 2 and plot them separately

def advection(phi0k, mode, n, Kk, Ak, Bk):
    eps = 0
    if mode == "CS" :
        m = 4
        return v0 * (1 - phi0k)**(m)
    if mode == "MK" :
        return Kk * ((max(phi0k,eps))**(1-n)) * ((ps - pw)/(v0*pw)) 
    if mode == "Zn" :
        return Ak * ((1-phi0k)/max(eps,phi0k))**(Bk) * ((ps-pw)/(v0*pw)) * phi0k
    
def diffusion(phi0k, mode, n, Ksig, Ap, Bp, KDELsig0):
    eps = 0
    if mode == "CS" :
        return (D0/v0) * ((1+ phi0k + (phi0k)**(2) - (phi0k)**(3))/(1 - (phi0k)**(3)))
    if mode == "MK" :
        return Ksig * (v0/D0)*((phi0k)**(n-1)) * (1/(g*(ps - pw)))
    if mode == "Zn" :
        KDELsig= (Ap*phi0k/(1-phi0k))**(1/Bp) - KDELsig0
        return v0/(D0*g*(ps-pw))*(KDELsig)/max(eps,phi0k)

def Ddiffusion(phi0k, mode, n, Ksig, Ap, Bp, KDELsig0):
    eps = 0
    if mode == "CS" :
        return (D0/v0) * ((1+ phi0k + (phi0k)**(2) - (phi0k)**(3))/(1 - (phi0k)**(3)))
    if mode == "MK" :
        dg= (v0/D0)*(n-1)*Ksig * ((phi0k)**(n-2)) * (1/(g*(ps - pw)))
        return (dg * phi0k) + diffusion(phi0k, mode, n, Ksig, Ap, Bp, KDELsig0)
        
    if mode == "Zn" :
        KDELsig= (Ap*phi0k/(1-phi0k))**(1/Bp) - KDELsig0
        dg = v0/(D0*g*(ps-pw))*(Ap**(1/Bp) * (1/Bp) * (1/(1-phi0k))**(2) * (phi0k/(1-phi0k))**(1/Bp - 1) * (1/phi0k) - KDELsig * (1/phi0k)**(2))
        return (dg * phi0k) + diffusion(phi0k, mode,n, Ksig, Ap, Bp, KDELsig0) 


#                        Solving the consolidation equation 
#                                  IMPLICIT METHOD
#                        SOLVING  AXn = Yn + Cextn => Xn = inv(A) Yn + inv(A) Cextn

##initial condition Layer 1
Y1 = vol01
gradientu1 = 0
##initial condition Layer 2
Y2 = vol02


for k in range(0,nt) :
    ##Layer 1
    al1=[]
    bl1=[]
    cl1=[]
    ddl1=[]
    
    #model parameters for Layer1 
    n = n1
    Kk = Kk1
    Ksig = Ksig1
    Ap = Ap1
    Bp = Bp1
    Ak = Ak1
    Bk = Bk1
    KDELsig0 = KDELsig01
    
    #Defining dz and dt
    deltaZ1 = H1/(nh1-1)
    deltaT = time[1] - time[0]
    #Defining (nh1-1) X (nh1-1) Matrice : M1
    M1 = []
    #first row of M1 matrix
    dZvol1 = deltaZ1 * volinit1
    
    divb = 0
    divt = D0*advection(Y1[0],mode,  n, Kk, Ak, Bk) * Ddiffusion(Y1[1], mode, n, Ksig, Ap, Bp, KDELsig0)* Y1[0]**(2) 
    advb = 0
    advt = v0*advection(Y1[0], mode, n, Kk, Ak, Bk)*Y1[0]**(2) 
    
    a1 = 0
    b1 = divt
    c1 = - divt
    dd1 = dZvol1 * advt * (1 + gradientu1/(Y1[0]*(g*ps - g*pw)))

    al1.append(a1)
    bl1.append(b1)
    cl1.append(c1)
    ddl1.append(dd1)


    #rows from 2nd to (kmax1) row
    for i in range(1,kmax1-1) :
        dZvol1 = deltaZ1 * volinit1
        divb = D0*advection(Y1[i-1],mode, n, Kk, Ak, Bk) * Ddiffusion(Y1[i], mode, n, Ksig, Ap, Bp, KDELsig0)*Y1[i]**(2) / dZvol1
        divt = D0*advection(Y1[i],mode,n, Kk, Ak, Bk) * Ddiffusion(Y1[i+1], mode, n, Ksig, Ap, Bp, KDELsig0)*Y1[i]**(2) / dZvol1
        advb = v0*advection(Y1[i-1], mode,n, Kk, Ak, Bk)*Y1[i]**(2)
        advt = v0*advection(Y1[i], mode,n, Kk, Ak, Bk)*Y1[i]**(2)
        
        ai = -divb
        bi = (dZvol1/deltaT) + divt + divb 
        ci = - divt
        ddi = (dZvol1/deltaT) *Y1[i] - advb + advt
        
        
        al1.append(ai)
        bl1.append(bi)
        cl1.append(ci)
        ddl1.append(ddi)
        
    #Last row of the martix 
    ifinal = kmax1 - 1 
    dZvol1 = deltaZ1 * volinit1
    divb = D0*advection(Y1[ifinal-1],mode, n, Kk, Ak, Bk) * Ddiffusion(Y1[ifinal], mode, n, Ksig, Ap, Bp, KDELsig0) * Y1[ifinal]**(2) / dZvol1
    divt = 0
    advb = v0*advection(Y1[ifinal-1], mode, n, Kk, Ak, Bk)* Y1[ifinal]**(2)
    advt = 0

    af = 0
    bf = 1
    cf = 0
    ddf = volinit1

    

    al1.append(af)
    bl1.append(bf)
    cl1.append(cf)
    ddl1.append(ddf)
    
    ##Layer2 
    al2=[]
    bl2=[]
    cl2=[]
    ddl2=[]
    
    #model parameters for Layer1 
    n = n2
    Kk = Kk2
    Ksig = Ksig2
    Ap = Ap2
    Bp = Bp2
    Ak = Ak2
    Bk = Bk2
    KDELsig0 = KDELsig02
    
    #Defining dz and dt
    deltaZ2 = H2/(nh2-1)
    deltaT = time[1] - time[0]
    #Defining (nh1-1) X (nh1-1) Matrice : M1
    M2 = []
    #first row of M1 matrix
    dZvol2 = deltaZ2 * volinit2
    
    divb = 0
    divt = D0*advection(Y2[0],mode,  n, Kk, Ak, Bk) * Ddiffusion(Y2[1], mode, n, Ksig, Ap, Bp, KDELsig0)* Y2[0]**(2) 
    advb = 0
    advt = v0*advection(Y2[0], mode, n, Kk, Ak, Bk)*Y2[0]**(2) 
    
    a1 = 0
    b1 = divt
    c1 = - divt
    dd1 = dZvol2 * advt 
    
    al2.append(a1)
    bl2.append(b1)
    cl2.append(c1)
    ddl2.append(dd1)


    #rows from 2nd to (kmax2) row
    for i in range(1,kmax2-1) :
        dZvol2 = deltaZ2 * volinit2
        divb = D0*advection(Y2[i-1],mode, n, Kk, Ak, Bk) * Ddiffusion(Y2[i], mode, n, Ksig, Ap, Bp, KDELsig0)*Y2[i]**(2) / dZvol2
        divt = D0*advection(Y2[i],mode,n, Kk, Ak, Bk) * Ddiffusion(Y2[i+1], mode, n, Ksig, Ap, Bp, KDELsig0)*Y2[i]**(2) / dZvol2
        advb = v0*advection(Y2[i-1], mode,n, Kk, Ak, Bk)*Y2[i]**(2)
        advt = v0*advection(Y2[i], mode,n, Kk, Ak, Bk)*Y2[i]**(2)
        
        ai = -divb
        bi = (dZvol2/deltaT) + divt + divb 
        ci = - divt
        ddi = (dZvol2/deltaT) *Y2[i] - advb + advt
        
        
        al2.append(ai)
        bl2.append(bi)
        cl2.append(ci)
        ddl2.append(ddi)
        
    #Last row of the martix 
    ifinal = kmax2 - 1 
    dZvol2 = deltaZ2 * volinit2
    divb = D0*advection(Y2[ifinal-1],mode, n, Kk, Ak, Bk) * Ddiffusion(Y2[ifinal], mode, n, Ksig, Ap, Bp, KDELsig0) * Y2[ifinal]**(2) / dZvol2
    divt = 0
    advb = v0*advection(Y2[ifinal-1], mode, n, Kk, Ak, Bk)* Y2[ifinal]**(2)
    advt = 0
    #Calculate the effective stress based on the value of the volume fraction
    #at the bottom of Layer 1
    phiup = Y1[0]
    sigup = g*(ps -pw)*(D0/v0)* phiup * diffusion(phiup, mode, n1, Ksig1, Ap1, Bp1, KDELsig01)
    #pore pressure at the interface of Layer 1 
    u1 = volinit1 *(ps - pw)*g*H1 + sigup
    #the effective stress at the top of Layer 2 
    sigdown = sigup 
    #volume fraction at the top of Layer 2
    if mode == 'Zn' : 
        voidratio2 = Ap2 * (sigdown + KDELsig02)**(-Bp2)
        phidown    = 1/(1 + voidratio2)
    if mode == 'MK' :
        phidown = (sigdown/Ksig2)**(1/n2)
        
    af = 0
    bf = 1
    cf = 0
    ddf = phidown

    

    al2.append(af)
    bl2.append(bf)
    cl2.append(cf)
    ddl2.append(ddf)
    
    ##Solution for Layer 1
    #SWEEP Method : invert the matrix
    cl1[0] = cl1[0]/bl1[0]
    ddl1[0] = ddl1[0]/bl1[0]

    for m in range(1,len(al1)):
        bl1[m] = bl1[m] - al1[m] * cl1[m-1]
        cl1[m] = cl1[m]/ bl1[m]
        ddl1[m] = (ddl1[m]-ddl1[m-1] * al1[m])/bl1[m]
    
    for m in range(len(al1)-2,-1,-1):
        ddl1[m] = ddl1[m] - cl1[m] * ddl1[m+1]
    
    for m in range(0,len(al1)):
        Y1[m] = ddl1[m]
        
    ##Solution for Layer 2
    #SWEEP Method : invert the matrix
    cl2[0] = cl2[0]/bl2[0]
    ddl2[0] = ddl2[0]/bl2[0]

    for m in range(1,len(al2)):
        bl2[m] = bl2[m] - al2[m] * cl2[m-1]
        cl2[m] = cl2[m]/ bl2[m]
        ddl2[m] = (ddl2[m]-ddl2[m-1] * al2[m])/bl2[m]
    
    for m in range(len(al2)-2,-1,-1):
        ddl2[m] = ddl2[m] - cl2[m] * ddl2[m+1]
    
    for m in range(0,len(al2)):
        Y2[m] = ddl2[m]
    
    #Adjust gradient u to assure continuity of flux
    ##calculate the effective stress at (n2-1) of Layer 2
    phidown_1 = Y2[-2]
    sigdown_1 = g*(ps -pw)*(D0/v0) * diffusion(phidown_1, mode, n2, Ksig2, Ap2, Bp2, KDELsig02)* phidown_1 
    gradientu2       = - phidown_1 * (ps - pw)* g - (phidown_1) * (sigdown - sigdown_1)/dZvol2
    permeability1   = v0 * pw/(Y1[0]*(ps-pw)) * advection(Y1[0], mode,n1, Kk1, Ak1, Bk1)
    permeability2   = v0 * pw/(Y2[-2]*(ps-pw))* advection(Y2[-2], mode,n2, Kk2, Ak2, Bk2)
    gradientu1      = (permeability2/permeability1)*(Y2[-2]/Y1[0]) * gradientu2
    
fig1, ax1 = plt.subplots()
ax1.plot(Y1,zbin1[1:])

fig2, ax2= plt.subplots()
ax2.plot(Y2,zbin2[1:])

fig3, ax3=plt.subplots()
#Join the two layers in an unique layer
zbin = []
for i in range(0,len(zbin2)):
    zbin.append(zbin2[i])

for i in range(1,len(zbin1)):
    d = zbin2[-1] + zbin1[i]
    zbin.append(d)
print(len(zbin))
Y = []
for i in range(len(Y2)):
    Y.append(Y2[i])
for i in range(len(Y1)):
    Y.append(Y1[i])
print(len(Y))
#ax3.plot(Y, zbin[1:])
ax3.plot(Y[:len(Y2)], zbin[1:len(Y2)+1] , label = 'Layer 2')
ax3.plot(Y[len(Y2):], zbin[len(Y2)+1:], label = 'Layer 1')
  

#Tansform form Lagrangien to Eulerian Frame 
dzvol2 = volinit2 * (H2/(nh2 - 1))
zf2    = 0
Z      = [zf2] 
for i in range(len(Y2)):
    zf2 = zf2 + dzvol2/Y2[i]
    Z.append(zf2)
dzvol1 = volinit1 * (H1/(nh1 - 1))
zf1   = zf2
for i in range(len(Y1)):
    zf1 = zf1 + dzvol1/Y1[i]
    Z.append(zf1)
fig4, ax4 = plt.subplots()
ax4.plot(Y,Z[1:])
Df = pd.DataFrame()
Df['Height'] = Z[1:]
Df['Volume fraction'] = Y
Df.to_excel("two layers.xlsx")

#Calculate the hydrostatic pressure 
U0 = []
for i in range(1,len(Z)):
    u0 = pw * g * (hwater - Z[i])
    U0.append(u0)
fig5, ax5 = plt.subplots()
ax5.plot(U0,Z[1:])

#Calculate the total stress
Sigtt = []
h2 = hwater - Z[-1]
for i in range(1,len(Z)):
    integral1 = 0
    integral2 = 0
    for j in range(i,len(Z)) : 
        e = (1-Y[j-1])/Y[j-1]
        dz = Z[j] - Z[j-1]
        integral1 += e * dz 
        integral2 += dz
    sigtt = pw*g * (h2 + integral1) + ps*g*integral2 
    Sigtt.append(sigtt)
fig6,ax6 = plt.subplots()
ax6.plot(Sigtt, Z[1:])

#Calculate the effective stress
Sigeff = []
for i in range(len(Y2)):
    sigeff = (D0/v0)* g*(ps -pw)* Y[i] * diffusion(Y[i], mode, n2, Ksig2, Ap2, Bp2, KDELsig02)
    Sigeff.append(sigeff)
for i in range(len(Y2),len(Y)):
    sigeff = (D0/v0)* g*(ps -pw)* Y[i] * diffusion(Y[i], mode, n1, Ksig1, Ap1, Bp1, KDELsig01)
    Sigeff.append(sigeff)
fig7 , ax7 = plt.subplots()
ax7.plot(Sigeff, Z[1:])
#Calculate the water pressure 
Uw = []
for i in range(len(Y)):
    uw = Sigtt[i] - Sigeff[i]
    Uw.append(uw)
fig8,ax8 = plt.subplots()
ax8.plot(Uw,Z[1:])
#Calculate the excess water pressure
Ue = []
for i in range(len(Y)):
    ue = Uw[i] - U0[i]
    Ue.append(ue)
fig9, ax9 = plt.subplots()
ax9.plot(Ue,Z[1:])

ax1.set_title('Layer 1', fontsize = 20)
ax2.set_title('Layer 2', fontsize = 20)
ax3.set_title('Multilayer ', fontsize = 20)

#title for phis(Euler), u0, sigtt, sigeff, uw and ue
ax4.set_title('Multilayer Euler Volume fraction',fontsize = 20)
ax5.set_title('Multilayer Euler Hydrostatic pressure', fontsize = 20)
ax6.set_title('Multilayer Euler total stress',fontsize = 20)
ax7.set_title('Multilayer Euler effective stress',fontsize = 20)
ax8.set_title('Multilayer Euler water pressure', fontsize = 20)
ax9.set_title('Multilayer Euler Pe at t = '+ str(round(t2c/(24*3600),0)), fontsize = 20)


ax1.set_xlabel('Volume fraction in [-]',fontsize = 20)
ax2.set_xlabel('Volume fraction in [-]',fontsize= 20)
ax3.set_xlabel('Volume fraction in [-]',fontsize= 20)
#xlabel for phis(Euler), u0, sigtt, sigeff, uw and ue
ax4.set_xlabel('Volume fractio in [-]',fontsize = 20)
ax5.set_xlabel('Hydrostatic pressure in Pa',fontsize= 20)
ax6.set_xlabel('total stress in Pa',fontsize= 20)
ax7.set_xlabel('effective stress in Pa',fontsize= 20)
ax8.set_xlabel('water pressure in Pa',fontsize= 20)
ax9.set_xlabel('excess pore water pressure in Pa',fontsize= 20)

ax1.set_ylabel('Gibson Height in m',fontsize= 20)
ax2.set_ylabel('Gibson Height in m',fontsize= 20)
ax3.set_ylabel('Gibson Height in m',fontsize= 20)
#ylabel for phis(Euler), u0, sigtt, sigeff, uw and ue
ax4.set_ylabel('Height in m',fontsize= 20)
ax5.set_ylabel('Height in m',fontsize= 20)
ax6.set_ylabel('Height in m',fontsize= 20)
ax7.set_ylabel('Height in m',fontsize= 20)
ax8.set_ylabel('Height in m',fontsize= 20)
ax9.set_ylabel('Height in m',fontsize= 20)

ax3.legend(fontsize = 15, loc = 'center right')

ax1.set_xlim(0.15,0.40)
ax2.set_xlim(0.15,0.40)
#ax3.set_xlim(0.15,0.40)
ax4.set_ylim(0,7)
ax9.set_xlim(0,1e6)