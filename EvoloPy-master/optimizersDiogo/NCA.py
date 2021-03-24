# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 22:00: 2020

@author: diogo

NCA with random choice and random probabilities
"""
import random
import numpy
import math
import cmath
from solution import solution
import time
import optimizersDiogo.WOA as woaOriginal
import optimizersDiogo.functions as f

def NCA(objf,lb,ub,dim,SearchAgents_no,Max_iter):
    
   # create upper and lower bundaries
    if not isinstance(lb, list):
        lb = [lb] * dim
    if not isinstance(ub, list):
        ub = [ub] * dim
            
    # Best of all times
    best_all=float("inf")
    best_position =numpy.zeros(dim)

    # initialize position vector and score for the leader (WOA)
    Leader_pos=numpy.zeros(dim)
    Leader_score=float("inf")  #change this to -inf for maximization problems

    # initialize alpha, beta, and delta_pos (GWO)
    Alpha_pos=numpy.zeros(dim)
    Alpha_score=float("inf")
    
    Beta_pos=numpy.zeros(dim)
    Beta_score=float("inf")
    
    Delta_pos=numpy.zeros(dim)
    Delta_score=float("inf")

    # PSO parameters    
    Vmax=6
    wMax=0.9
    wMin=0.2
    c1=2
    c2=2

    vel=numpy.zeros((SearchAgents_no,dim))
    
    pBestScore=numpy.zeros(SearchAgents_no) 
    pBestScore.fill(float("inf"))
    
    pBest=numpy.zeros((SearchAgents_no,dim))
    gBest=numpy.zeros(dim)

    gBestScore=float("inf")

    #BAT parameters
    # A=0.5;      # Loudness  (constant or decreasing)
    # r=0.5;      # Pulse rate (constant or decreasing)
    
    # Qmin=0         # Frequency minimum
    # Qmax=2         # Frequency maximum

    # Q=numpy.zeros(SearchAgents_no)  # Frequency
    # v=numpy.zeros((SearchAgents_no,dim))  # Velocities
    # fmin = float("inf")     
        
        
    # #Initialize the positions of search agents
    Positions = numpy.zeros((SearchAgents_no, dim))
    for i in range(dim):
        Positions[:, i] = numpy.random.uniform(0,1,SearchAgents_no) *(ub[i]-lb[i])+lb[i]
  

    #Initialize convergence
    convergence_curve=numpy.zeros(Max_iter)
    
    # Calculate objective function for each search agent
    fitness=objf(Positions[i,:])        
    convergence_curve[0]=fitness    
    ############################
    s=solution()

    print("NCA is optimizing  \""+objf.__name__+"\"")    

    timerStart=time.time() 
    s.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    ############################
        
    t=1  # Loop counter
        
    # Main loop
    while t<=Max_iter-1:
        
        # algorithm = ["PSO", "GWO", "WOA", "IWOA", "CWOA", "WOANL", "WOAAC"]
        algorithm = ["PSO", "GWO", "WOA"]          
        
        while len(algorithm) > 0:
            prob = numpy.random.random_sample(len(algorithm))
            prob /= prob.sum() # normalize distribution           

            choice = numpy.random.choice(algorithm,p=prob)
            
            #PSO
            if(choice == "PSO" and t < Max_iter):
                if gBestScore > best_all:
                    gBestScore = best_all
                    gBest = best_position        
                best_all, best_position, Positions = f.pso(objf, t, Max_iter, SearchAgents_no, dim, Positions, lb, ub, Vmax, wMax, wMin, c1, c2, vel, pBest, gBest, pBestScore, gBestScore)            
                index = algorithm.index("PSO")
                algorithm.remove("PSO")               
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all
                t=t+1                     
            
            #GWO
            if(choice == "GWO" and t < Max_iter):
                if Alpha_score > best_all:
                    Alpha_score = best_all
                    Alpha_pos = best_position            
                best_all, best_position, Positions = f.gwo(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Alpha_pos, Beta_pos, Delta_pos, Alpha_score,  Beta_score,  Delta_score)               
                index = algorithm.index("GWO")
                algorithm.remove("GWO")                
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all
                t=t+1                     
            
            #WOA
            if(choice == "WOA" and t < Max_iter):
                if Leader_score > best_all:
                    Leader_score = best_all
                    Leader_pos = best_position   
                best_all, best_position, Positions = f.woa(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Leader_pos, Leader_score)
                index = algorithm.index("WOA")
                algorithm.remove("WOA")
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all
                t=t+1               

            #IWOA
            if(choice == "IWOA" and t < Max_iter):                
                if Leader_score > best_all:
                    Leader_score = best_all
                    Leader_pos = best_position   
                best_all, best_position, Positions = f.iwoa(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Leader_pos, Leader_score)  
                index = algorithm.index("IWOA")
                algorithm.remove("IWOA")                
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all 
                t=t+1

            #CWOA
            if(choice == "CWOA" and t < Max_iter):                
                if Leader_score > best_all:
                    Leader_score = best_all
                    Leader_pos = best_position   
                best_all, best_position, Positions = f.cwoa(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Leader_pos, Leader_score)  
                index = algorithm.index("CWOA")
                algorithm.remove("CWOA")                
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all 
                t=t+1

            #WOANL
            if(choice == "WOANL" and t < Max_iter):                
                if Leader_score > best_all:
                    Leader_score = best_all
                    Leader_pos = best_position   
                best_all, best_position, Positions = f.woanl(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Leader_pos, Leader_score)  
                index = algorithm.index("WOANL")
                algorithm.remove("WOANL")                
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all 
                t=t+1

            #WOAAC
            if(choice == "WOAAC" and t < Max_iter):                
                if Leader_score > best_all:
                    Leader_score = best_all
                    Leader_pos = best_position   
                best_all, best_position, Positions = f.woaac(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Leader_pos, Leader_score)  
                index = algorithm.index("WOAAC")
                algorithm.remove("WOAAC")                
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all 
                t=t+1    

            if (t%1==0):
                print(['At iteration '+ str(t)+ ' the best fitness is '+ str(best_all)]); 

            if (t == Max_iter):
                break                       

         
        
        
        
        
    timerEnd=time.time()  
    s.endTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime=timerEnd-timerStart
    s.convergence=convergence_curve
    s.optimizer="NCA"   
    s.objfname=objf.__name__
    s.best = best_all
    s.bestIndividual = best_position
    s.std = numpy.std(convergence_curve)
    s.mean = numpy.average(convergence_curve)
       
    return s