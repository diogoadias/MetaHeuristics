# -*- coding: utf-8 -*-
"""
Created on Sun May 15 22:37:00 2016

@author: Hossam Faris
"""

import random
import numpy
from colorama import Fore, Back, Style
from solution import solution
import time






def PSO(objf,lb,ub,dim,PopSize,iters,pos,best_all,best_position,t):

    # PSO parameters    
    Vmax=6
    wMax=0.9
    wMin=0.2
    c1=2
    c2=2

    if not isinstance(lb, list):
        lb = [lb] * dim
    if not isinstance(ub, list):
        ub = [ub] * dim
    
    
    ######################## Initializations
    
    vel=numpy.zeros((PopSize,dim))
    
    pBestScore=numpy.zeros(PopSize) 
    pBestScore.fill(float("inf"))
    
    pBest=numpy.zeros((PopSize,dim))
    gBest=best_position
    
    
    gBestScore=best_all
    
        
    ############################################
    print("PSO is optimizing  \""+objf.__name__+"\"")    
    
    timerStart=time.time()     
    
    #for l in range(0,iters):
    for i in range(0,PopSize):
        #pos[i,:]=checkBounds(pos[i,:],lb,ub)
        for j in range(dim):
            pos[i, j] = numpy.clip(pos[i,j], lb[j], ub[j])
        #Calculate objective function for each particle
        fitness=objf(pos[i,:])
    
        if(pBestScore[i]>fitness):
            pBestScore[i]=fitness
            pBest[i,:]=pos[i,:].copy()
                
        if(gBestScore>fitness):
            gBestScore=fitness
            gBest=pos[i,:].copy()
        
    #Update the W of PSO
    w=wMax-t*((wMax-wMin)/iters);
        
    for i in range(0,PopSize):
        for j in range (0,dim):
            r1=random.random()
            r2=random.random()
            vel[i,j]=w*vel[i,j]+c1*r1*(pBest[i,j]-pos[i,j])+c2*r2*(gBest[j]-pos[i,j])
                
            if(vel[i,j]>Vmax):
                vel[i,j]=Vmax
                
            if(vel[i,j]<-Vmax):
                vel[i,j]=-Vmax
                            
            pos[i,j]=pos[i,j]+vel[i,j]
        
        
    return gBestScore, gBest, pos
         
    
