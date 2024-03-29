# -*- coding: utf-8 -*-
"""
Created on Mon May 16 14:19:49 2016

@author: hossam
"""
import random
import numpy
import math
from solution import solution
import time




def WOAAC(objf,lb,ub,dim,SearchAgents_no,Max_iter,Positions,best_all,best_position,t):
    
    #dim=30
    #SearchAgents_no=50
    #lb=-100
    #ub=100
    #Max_iter=500
    if not isinstance(lb, list):
        lb = [lb] * dim
    if not isinstance(ub, list):
        ub = [ub] * dim
            
        
    # initialize position vector and score for the leader
    Leader_pos=best_position
    Leader_score=best_all  #change this to -inf for maximization problems
        
    print("WOAAC is optimizing  \""+objf.__name__+"\"")          
   
    for i in range(0,SearchAgents_no):
                
        # Return back the search agents that go beyond the boundaries of the search space
               
        #Positions[i,:]=checkBounds(Positions[i,:],lb,ub)
        for j in range(dim):        
            Positions[i,j]=numpy.clip(Positions[i,j], lb[j], ub[j])
                
        # Calculate objective function for each search agent
        fitness=objf(Positions[i,:])
               
        # Update the leader
        if fitness<Leader_score: # Change this to > for maximization problem
            Leader_score=fitness; # Update alpha
            Leader_pos=Positions[i,:].copy() # copy current whale position into the leader position

    a2=-1+t*((-1)/Max_iter);
                    
    # Update the Position of search agents 
    for i in range(0,SearchAgents_no):
        r1=random.random() # r1 is a random number in [0,1]
        r2=random.random() # r2 is a random number in [0,1]

        a = 2-math.cos(r1)*(t-1/Max_iter-1) # A-C Parametric

        A=2*a*r1-a  # Eq. (2.3) in the paper           
            
        # A-C Parametric
        Cmin = 0.4
        Cmax = 0.9
        C = Cmin + (Cmax - Cmin) * (t-1 / Max_iter -1)

        w = 0.5+0.5*r1 # Inertia weight from A-C Parametric

        b=1;               #  parameters in Eq. (2.5)
        l=(a2-1)*random.random()+1   #  parameters in Eq. (2.5)
                
        p = random.random()        # p in Eq. (2.6)
                
        for j in range(0,dim):
            D_Leader = Positions[i, j] # fix algorithm problem

            if Positions[i,j] == Leader_pos[j]:
                D_Leader=abs(C*Leader_pos[j])    
            if p>=0.5:
                if Positions[i,j] != Leader_pos[j]:
                    D_Leader=abs(C*Leader_pos[j]-Positions[i,j])
                    # Eq. (2.5)                        
                Positions[i,j]=D_Leader*math.exp(b*l)*math.cos(l*2*math.pi)+Leader_pos[j]*w 
                
            else:
                if abs(A)<1:
                    if Positions[i,j] != Leader_pos[j]:
                        D_Leader=abs(C*Leader_pos[j]-Positions[i,j]) 
                     
                    Positions[i,j]=w*Leader_pos[j]-A*D_Leader  
                        
                elif abs(A)>=1:
                    rand_leader_index = math.floor(SearchAgents_no*random.random());
                    X_rand = Positions[rand_leader_index, :]
                    if X_rand[j] != Leader_pos[j]:
                        D_Leader=abs(C*X_rand[j]-Positions[i,j])             

                    Positions[i,j]=w*X_rand[j]-A*D_Leader  

    return Leader_score, Leader_pos, Positions