# -*- coding: utf-8 -*-
"""
Created on Thu May 26 02:00:55 2016

@author: hossam
"""
import math
import numpy
import random
import time
from solution import solution
    

def BAT(objf,lb,ub,dim,N,Max_iteration,Positions, best_all, best_position,t):
    
    n=N;      # Population size

    if not isinstance(lb, list):
        lb = [lb] * dim
    if not isinstance(ub, list):
        ub = [ub] * dim
    N_gen=Max_iteration  # Number of generations
    
    A=0.5;      # Loudness  (constant or decreasing)
    r=0.5;      # Pulse rate (constant or decreasing)
    
    Qmin=0         # Frequency minimum
    Qmax=2         # Frequency maximum
    
    
    d=dim           # Number of dimensions 
    
    # Initializing arrays
    Q=numpy.zeros(n)  # Frequency
    v=numpy.zeros((n,d))  # Velocities
    convergence_curve=[];
    fmin = float("inf")
    
    # Initialize the population/solutions
    Sol = Positions   

    S=numpy.zeros((n,d))
    S=numpy.copy(Sol)
    Fitness=numpy.zeros(n)
    
    
    # initialize solution for the final results   
    s=solution()
    print("BAT is optimizing  \""+objf.__name__+"\"")    
    
    # Initialize timer for the experiment
    timerStart=time.time() 
    s.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    
    #Evaluate initial random solutions
    for i in range(0,n):
      Fitness[i]=objf(Sol[i,:])
    
    
    # Find the initial best solution
    I=numpy.argmin(Fitness)
    best=Sol[I,:]
           
    # Main loop
       
    # Loop over all bats(solutions)
    for i in range (0,n):
      Q[i]=Qmin+(Qmin-Qmax)*random.random()
      v[i,:]=v[i,:]+(Sol[i,:]-best)*Q[i]
      S[i,:]=Sol[i,:]+v[i,:]
          
      # Check boundaries
      for j in range(d):
        Sol[i,j] = numpy.clip(Sol[i,j], lb[j], ub[j])

        # Pulse rate
        if random.random()>r:
          S[i,:]=best+0.001*numpy.random.randn(d)
          
    
        # Evaluate new solutions
        Fnew=objf(S[i,:])
          
        # Update if the solution improves
        if ((Fnew<=Fitness[i]) and (random.random()<A) ):
          Sol[i,:]=numpy.copy(S[i,:])
          Fitness[i]=Fnew;
           
    
        # Update the current best solution
        if Fnew<=fmin:
          best=numpy.copy(S[i,:])
          fmin=Fnew
                
        #update convergence curve
        #convergence_curve.append(fmin)        

        #if (t%1==0):
        #  print(['At iteration '+ str(t)+ ' the best fitness is '+ str(fmin)])
    
        
    return fmin, best, Sol
