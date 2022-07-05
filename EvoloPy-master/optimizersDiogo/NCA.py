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
import optimizersDiogo.GWO as gwo
import optimizersDiogo.MFO as mfo
import optimizersDiogo.MPA as mpa
import optimizersDiogo.PSO as pso
import optimizersDiogo.WOA as woa
import optimizersDiogo.FFA as ffa
import optimizersDiogo.SSA as ssa
import optimizersDiogo.BAT as bat
import optimizersDiogo.WOAAC as woaac
import optimizersDiogo.IWOA2 as iwoa2
import optimizersDiogo.CWOA as cwoa

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
        
    #Initialize the positions of search agents
    Positions = numpy.zeros((SearchAgents_no, dim))
    for i in range(dim):
        Positions[:, i] = numpy.random.uniform(0,1,SearchAgents_no) *(ub[i]-lb[i])+lb[i]
  

    #Initialize convergence
    convergence_curve=numpy.zeros(Max_iter)
    
    # Calculate objective function for each search agent
    #fitness=objf(Positions[i,:])        
    #convergence_curve[0]=fitness    
    ############################
    s=solution()

    print("NCA is optimizing  \""+objf.__name__+"\"")    

    timerStart=time.time() 
    s.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    ############################
        
    t=0  # Loop counter
        
    # Main loop
    while t<Max_iter:
        
        #algorithm = ["MPA","GWO", "WOA", "IWOA2", "CWOA", "WOAAC"]
        #algorithm = ["MPA", "CWOA", "WOAAC", "IWOA2"] # NCA-MPA
        #algorithm = ["WOA", "PSO", "GWO", "WOAAC"] # NCA A-C
        #algorithm = ["WOA", "CWOA", "IWOA2", "WOAAC"]  #WOA-NCA
        #algorithm = ["CWOA", "IWOA2", "WOAAC", "WOANL"]  #WOA-M
        algorithm = ["FFA"]
        

        choice = None

        while len(algorithm) > 0:
            prob = numpy.random.random_sample(len(algorithm))
            prob /= prob.sum() # normalize distribution           

            if choice is None:
                choice = numpy.random.choice(algorithm,p=prob)
            
            #PSO
            if(choice == "PSO" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = pso.PSO(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("PSO")
            
            #GWO
            if(choice == "GWO" and t < Max_iter):                         
                best_so_far, best_position_so_far, Positions = gwo.GWO(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)               
                index = algorithm.index("GWO")
                                 
            
            #WOA
            if(choice == "WOA" and t < Max_iter):                 
                best_so_far, best_position_so_far, Positions = woa.WOA(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("WOA")
                

            #FFA
            if(choice == "FFA" and t < Max_iter):                
                best_so_far, best_position_so_far, Positions = ffa.FFA(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("FFA")
                

            #MFO
            if(choice == "MFO" and t < Max_iter):                
                best_so_far, best_position_so_far, Positions = mfo.MFO(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("MFO")
                

            #MPA
            if(choice == "MPA" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = mpa.MPA(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("MPA")
               

            #SSA
            if(choice == "SSA" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = ssa.SSA(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("SSA")
               

            #BAT
            if(choice == "BAT" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = bat.BAT(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("BAT")
                            
            #WOAAC
            if(choice == "WOAAC" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = woaac.WOAAC(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("WOAAC")
                

            #IWOA2
            if(choice == "IWOA2" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = iwoa2.IWOA2(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("IWOA2")
               
            
            #CWOA
            if(choice == "CWOA" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = cwoa.CWOA(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("CWOA")
              

            #WOANL
            if(choice == "WOANL" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = cwoa.CWOA(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("WOANL")
           
            
            #DETAILED NCA
            # iteration_values = []
            # iteration_values.append(choice)
            # iteration_values.append(best_so_far)
            # iteration_values.append(best_position_so_far)
            # s.NCA.append(iteration_values)

            if (t == Max_iter):
                break

            if(best_so_far < best_all):
                best_all = best_so_far
                best_position = best_position_so_far
            else: 
                prob = numpy.delete(prob, index)
                algorithm.remove(choice) 
                choice = None            
            

            if (t%1==0):
                print(['At iteration '+ str(t)+ ' the best fitness is '+ str(best_all)]); 
            
            # check = numpy.array_equal(Positions, new_Positions)    
            # if not check:
            #     Positions = new_Positions

            convergence_curve[t]=best_all            
            t=t+1                        
        
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