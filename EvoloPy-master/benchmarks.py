# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:46:20 2016

@author: Hossam Faris
"""
import sys
sys.path.append(".")

import numpy as np
import math
import random
import csv


# define the function blocks
def prod( it ):
    p= 1
    for n in it:
        p *= n
    return p

def Ufun(x,a,k,m):
    y=k*((x-a)**m)*(x>a)+k*((-x-a)**m)*(x<(-a));
    return y
    
def F1(x):
    s=np.sum(x**2);
    return s

def F2(x):
    o=sum(abs(x))+prod(abs(x));
    return o;     
           
def F3(x):
    dim=len(x)+1;
    o=0;
    for i in range(1,dim):
        o=o+(np.sum(x[0:i]))**2; 
    return o; 
    
def F4(x):
    o=max(abs(x));
    return o;     

def F5(x):
    dim=len(x);
    o=np.sum(100*(x[1:dim]-(x[0:dim-1]**2))**2+(x[0:dim-1]-1)**2);
    return o; 

def F6(x):
    o=np.sum(abs((x+.5))**2);
    return o;

def F7(x):
   dim=len(x);
   w=[i for i in range(len(x))]
   for i in range(0,dim):
        w[i]=i+1;
   o=np.sum(w*(x**4))+np.random.uniform(0,1);
   return o;

def F8(x):
    o=np.sum(-x*(np.sin(np.sqrt(abs(x)))));
    return o;

def F9(x):
    dim=len(x);
    o=np.sum(x**2-10*np.cos(2*math.pi*x))+10*dim;
    return o;


def F10(x):
    dim=len(x);
    o=-20*np.exp(-.2*np.sqrt(np.sum(x**2)/dim))-np.exp(np.sum(np.cos(2*math.pi*x))/dim)+20+np.exp(1);
    return o;

def F11(x):
    dim=len(x);
    w=[i for i in range(len(x))]
    w=[i+1 for i in w];
    o=np.sum(x**2)/4000-prod(np.cos(x/np.sqrt(w)))+1;   
    return o;
    
def F12(x):
    dim=len(x);
    o=(math.pi/dim)*(10*((np.sin(math.pi*(1+(x[0]+1)/4)))**2)+np.sum((((x[1:dim-1]+1)/4)**2)*(1+10*((np.sin(math.pi*(1+(x[1:dim-1]+1)/4))))**2))+((x[dim-1]+1)/4)**2)+np.sum(Ufun(x,10,100,4));   
    return o;
    
def F13(x): 
    dim=len(x);
    o=.1*((np.sin(3*math.pi*x[1]))**2+sum((x[0:dim-2]-1)**2*(1+(np.sin(3*math.pi*x[1:dim-1]))**2))+ 
    ((x[dim-1]-1)**2)*(1+(np.sin(2*math.pi*x[dim-1]))**2))+np.sum(Ufun(x,5,100,4));
    return o;
    
def F14(x): 
     aS=[[-32,-16,0,16,32,-32,-16,0,16,32,-32,-16,0,16,32,-32,-16,0,16,32,-32,-16,0,16,32],[-32,-32,-32,-32,-32,-16,-16,-16,-16,-16,0,0,0,0,0,16,16,16,16,16,32,32,32,32,32]];     
     aS=np.asarray(aS);
     bS = np.zeros(25)
     v=np.matrix(x)
     for i in range(0,25):
         H=v-aS[:,i];
         bS[i]=np.sum((np.power(H,6)));   
     w=[i for i in range(25)]   
     for i in range(0,24):
        w[i]=i+1;
     o=((1./500)+np.sum(1./(w+bS)))**(-1);
     return o;  
     
def F15(L):  
    aK=[.1957,.1947,.1735,.16,.0844,.0627,.0456,.0342,.0323,.0235,.0246];
    bK=[.25,.5,1,2,4,6,8,10,12,14,16];
    aK=np.asarray(aK);
    bK=np.asarray(bK);
    bK = 1/bK;  
    fit=np.sum((aK-((L[0]*(bK**2+L[1]*bK))/(bK**2+L[2]*bK+L[3])))**2);
    return fit

def F16(L):  
     o=4*(L[0]**2)-2.1*(L[0]**4)+(L[0]**6)/3+L[0]*L[1]-4*(L[1]**2)+4*(L[1]**4);
     return o

def F17(L):  
    o=(L[1]-(L[0]**2)*5.1/(4*(np.pi**2))+5/np.pi*L[0]-6)**2+10*(1-1/(8*np.pi))*np.cos(L[0])+10;
    return o
    
def F18(L):  
    o=(1+(L[0]+L[1]+1)**2*(19-14*L[0]+3*(L[0]**2)-14*L[1]+6*L[0]*L[1]+3*L[1]**2))*(30+(2*L[0]-3*L[1])**2*(18-32*L[0]+12*(L[0]**2)+48*L[1]-36*L[0]*L[1]+27*(L[1]**2)));
    return o
# map the inputs to the function blocks
def F19(L):    
    aH=[[3,10,30],[.1,10,35],[3,10,30],[.1,10,35]];
    aH=np.asarray(aH);
    cH=[1,1.2,3,3.2];
    cH=np.asarray(cH);
    pH=[[.3689,.117,.2673],[.4699,.4387,.747],[.1091,.8732,.5547],[.03815,.5743,.8828]];
    pH=np.asarray(pH);
    o=0;
    for i in range(0,4):
     o=o-cH[i]*np.exp(-(np.sum(aH[i,:]*((L-pH[i,:])**2))));   
    return o
    

def F20(L):    
    aH=[[10,3,17,3.5,1.7,8],[.05,10,17,.1,8,14],[3,3.5,1.7,10,17,8],[17,8,.05,10,.1,14]];
    aH=np.asarray(aH);
    cH=[1,1.2,3,3.2];
    cH=np.asarray(cH);
    pH=[[.1312,.1696,.5569,.0124,.8283,.5886],[.2329,.4135,.8307,.3736,.1004,.9991],[.2348,.1415,.3522,.2883,.3047,.6650],[.4047,.8828,.8732,.5743,.1091,.0381]];
    pH=np.asarray(pH);
    o=0;
    for i in range(0,4):
     o=o-cH[i]*np.exp(-(np.sum(aH[i,:]*((L-pH[i,:])**2))));
    return o

def F21(L):
    aSH=[[4,4,4,4],[1,1,1,1],[8,8,8,8],[6,6,6,6],[3,7,3,7],[2,9,2,9],[5,5,3,3],[8,1,8,1],[6,2,6,2],[7,3.6,7,3.6]];
    cSH=[.1,.2,.2,.4,.4,.6,.3,.7,.5,.5];
    aSH=np.asarray(aSH);
    cSH=np.asarray(cSH);
    fit=0;
    for i in range(0,4):
      v=np.matrix(L-aSH[i,:])
      fit=fit-((v)*(v.T)+cSH[i])**(-1);
    o=fit.item(0);
    return o
  
def F22(L):
    aSH=[[4,4,4,4],[1,1,1,1],[8,8,8,8],[6,6,6,6],[3,7,3,7],[2,9,2,9],[5,5,3,3],[8,1,8,1],[6,2,6,2],[7,3.6,7,3.6]];
    cSH=[.1,.2,.2,.4,.4,.6,.3,.7,.5,.5];
    aSH=np.asarray(aSH);
    cSH=np.asarray(cSH);
    fit=0;
    for i in range(0,6):
      v=np.matrix(L-aSH[i,:])
      fit=fit-((v)*(v.T)+cSH[i])**(-1);
    o=fit.item(0);
    return o  

def F23(L):
    aSH=[[4,4,4,4],[1,1,1,1],[8,8,8,8],[6,6,6,6],[3,7,3,7],[2,9,2,9],[5,5,3,3],[8,1,8,1],[6,2,6,2],[7,3.6,7,3.6]];
    cSH=[.1,.2,.2,.4,.4,.6,.3,.7,.5,.5];
    aSH=np.asarray(aSH);
    cSH=np.asarray(cSH);
    fit=0;
    for i in range(0,9):
      v=np.matrix(L-aSH[i,:])
      fit=fit-((v)*(v.T)+cSH[i])**(-1);
    o=fit.item(0);
    return o  

def welded_beam_cost(x):
    # Design variables
    h, l, t, b = x
    
    # Boundary limits for the design variables
    h_min, h_max = 0.1, 2.0
    l_min, l_max = 0.1, 10.0
    t_min, t_max = 0.1, 10.0
    b_min, b_max = 0.1, 2.0

    # Apply penalties if design variables are out of bounds
    penalty = 0
    if h < h_min or h > h_max:
        penalty += 1e6  # Large penalty for h out of bounds
    if l < l_min or l > l_max:
        penalty += 1e6  # Large penalty for l out of bounds
    if t < t_min or t > t_max:
        penalty += 1e6  # Large penalty for t out of bounds
    if b < b_min or b > b_max:
        penalty += 1e6  # Large penalty for b out of bounds

    # If any variable is out of bounds, return a high penalty cost
    if penalty > 0:
        return penalty

    # Problem constants
    P = 6000.0  # Applied load in lb
    L = 14.0    # Length in inches
    E = 30e6    # Modulus of elasticity in psi
    G = 12e6    # Shear modulus in psi
    tau_max = 13600.0  # Max shear stress in psi
    sigma_max = 30000.0  # Max normal stress in psi
    delta_max = 0.25  # Max deflection in inches

    # Objective function (cost)
    cost = 1.10471 * h**2 * l + 0.04811 * t * b * (14.0 + l)
    
    # Shear stress calculation
    M = P * (L + l / 2)
    tau_prime = P / (np.sqrt(2) * h * b)
    R = np.sqrt((t**2 / 4.0) + ((h + t)**2 / 4.0))
    tau_double_prime = M * R / (2 * 0.707 * h * t**2)
    tau = np.sqrt(tau_prime**2 + tau_double_prime**2 + (l * tau_prime * tau_double_prime) / np.sqrt(0.25 * l**2 + (h + t)**2 / 4.0))
    
    # Normal stress calculation
    sigma = 6 * P * L / (b * t**2)
    
    # Deflection calculation
    delta = 4 * P * L**3 / (E * b * t**3)
    
    # Buckling load calculation
    buckling_constraint = (P / (h * l)) - tau_max
    
    # Constraints
    g1 = tau - tau_max  # Shear stress constraint
    g2 = sigma - sigma_max  # Normal stress constraint
    g3 = delta - delta_max  # Deflection constraint
    g4 = h - b  # Width to height ratio constraint
    g5 = buckling_constraint  # Buckling load constraint
    g6 = P / (h * l) - tau_max  # Shear force constraint
    g7 = 1.10471 * l**2 + 0.04811 * t * b * (14.0 + l) - 5.0  # Additional constraint
    
    # Sum of squared constraint violations
    penalty += sum(g**2 for g in [g1, g2, g3, g4, g5, g6, g7] if g > 0)
    
    # Total cost with penalty
    total_cost = cost + penalty

    data = [[h,l,t,b]]
    with open('data_pipe_delimited.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerows(data)
    
    return max(total_cost, 0)  # Ensure the total cost is non-negative
   
   
def getFunctionDetails(a):
    
    # [name, lb, ub, dim]
    param = {  "F1": ["F1",-5.12,5.12,30],
               "F2" : ["F2",-10,10,30],
               "F3" : ["F3",-100,100,30],
               "F4" : ["F4",-100,100,30] ,
               "F5" : ["F5",-30,30,30],
               "F6" : ["F6",-100,100,30],
               "F7" : ["F7",-1.28,1.28,30],
               "F8" : ["F8",-500,500,30],
               "F9" : ["F9",-5.12,5.12,30],
               "F10" : ["F10",-32.768,32.768,30],
               "F11" : ["F11",-600,600,30] ,
               "F12" : ["F12",-50,50,30],
               "F13" : ["F13",-50,50,30],
               "F14" : ["F14",-65.536,65.536,2],
               "F15" : ["F15",-5,5,4],
               "F16" : ["F16",-5,5,2],
               "F17" : ["F17",-5,15,2],
               "F18" : ["F18",-2,2,2] ,
               "F19" : ["F19",0,1,3],
               "F20" : ["F20",0,1,6],
               "F21" : ["F21",0,10,4],
               "F22" : ["F22",0,10,4],
               "F23" : ["F23",0,10,4],
               "welded_beam_cost" : ["welded_beam_cost", [0.125, 0.1, 0.1, 0.125], [2.0, 10.0, 10.0, 2.0], 4],              
            }
    return param.get(a, "nothing")



