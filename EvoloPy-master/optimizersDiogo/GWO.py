# -*- coding: utf-8 -*-
"""
Created on Mon May 16 00:27:50 2016

@author: Hossam Faris
"""

import random
import numpy
import math
from solution import solution
import time
    

def GWO(objf,lb,ub,dim,SearchAgents_no,Max_iter, Positions, best_all, best_position,t):
    
    # initialize alpha, beta, and delta_pos
    Alpha_pos=best_position
    Alpha_score=best_all
    
    Beta_pos=numpy.zeros(dim)
    Beta_score=float("inf")
    
    Delta_pos=numpy.zeros(dim)
    Delta_score=float("inf")

    if not isinstance(lb, list):
        lb = [lb] * dim
    if not isinstance(ub, list):
        ub = [ub] * dim      
    
    # Loop counter
    print("GWO is optimizing  \""+objf.__name__+"\"")    
    
    timerStart=time.time() 
   
    # Main loop
    #for l in range(0,Max_iter):
    for i in range(0,SearchAgents_no):
          
        # Return back the search agents that go beyond the boundaries of the search space
        for j in range(dim):
            Positions[i,j]=numpy.clip(Positions[i,j], lb[j], ub[j])

        # Calculate objective function for each search agent
        fitness=objf(Positions[i,:])
            
        # Update Alpha, Beta, and Delta
        if fitness<Alpha_score :
            Alpha_score=fitness; # Update alpha
            Alpha_pos=Positions[i,:].copy()
            
            
        if (fitness>Alpha_score and fitness<Beta_score ):
            Beta_score=fitness  # Update beta
            Beta_pos=Positions[i,:].copy()
            
            
        if (fitness>Alpha_score and fitness>Beta_score and fitness<Delta_score): 
            Delta_score=fitness # Update delta
            Delta_pos=Positions[i,:].copy()
            
        
                
    a=2-t*((2)/Max_iter); # a decreases linearly fron 2 to 0
        
    # Update the Position of search agents including omegas
    for i in range(0,SearchAgents_no):
        for j in range (0,dim):     
                           
            r1=random.random() # r1 is a random number in [0,1]
            r2=random.random() # r2 is a random number in [0,1]
                
            A1=2*a*r1-a; # Equation (3.3)
            C1=2*r2; # Equation (3.4)
                
            D_alpha=abs(C1*Alpha_pos[j]-Positions[i,j]); # Equation (3.5)-part 1
            X1=Alpha_pos[j]-A1*D_alpha; # Equation (3.6)-part 1
                           
            r1=random.random()
            r2=random.random()
                
            A2=2*a*r1-a; # Equation (3.3)
            C2=2*r2; # Equation (3.4)
                
            D_beta=abs(C2*Beta_pos[j]-Positions[i,j]); # Equation (3.5)-part 2
            X2=Beta_pos[j]-A2*D_beta; # Equation (3.6)-part 2       
                
            r1=random.random()
            r2=random.random() 
                
            A3=2*a*r1-a; # Equation (3.3)
            C3=2*r2; # Equation (3.4)
                
            D_delta=abs(C3*Delta_pos[j]-Positions[i,j]); # Equation (3.5)-part 3
            X3=Delta_pos[j]-A3*D_delta; # Equation (3.5)-part 3             
               
            Positions[i,j]=(X1+X2+X3)/3  # Equation (3.7)           
        
                
    return Alpha_score, Alpha_pos, Positions
    

