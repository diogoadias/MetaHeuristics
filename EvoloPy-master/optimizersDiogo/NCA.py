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
        algorithm = ["PSO", "GWO", "WOA", "FFA", "MFO", "MPA", "SSA", "BAT"]          
        
        while len(algorithm) > 0:
            prob = numpy.random.random_sample(len(algorithm))
            prob /= prob.sum() # normalize distribution           

            choice = numpy.random.choice(algorithm,p=prob)
            
            #PSO
            if(choice == "PSO" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = pso.PSO(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("PSO")
                algorithm.remove("PSO")               
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all
                                    
            
            #GWO
            if(choice == "GWO" and t < Max_iter):                         
                best_so_far, best_position_so_far, Positions = gwo.GWO(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)               
                index = algorithm.index("GWO")
                algorithm.remove("GWO")                
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all
                                     
            
            #WOA
            if(choice == "WOA" and t < Max_iter):                 
                best_so_far, best_position_so_far, Positions = woa.WOA(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("WOA")
                algorithm.remove("WOA")
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all
                

            #FFA
            if(choice == "FFA" and t < Max_iter):                
                best_so_far, best_position_so_far, Positions = ffa.FFA(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("FFA")
                algorithm.remove("FFA")
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all
                

            #MFO
            if(choice == "MFO" and t < Max_iter):                
                best_so_far, best_position_so_far, Positions = mfo.MFO(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("MFO")
                algorithm.remove("MFO")
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all
                

            #MPA
            if(choice == "MPA" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = mpa.MPA(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("MPA")
                algorithm.remove("MPA")
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all
                

            #SSA
            if(choice == "SSA" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = ssa.SSA(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("SSA")
                algorithm.remove("SSA")
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all
                

            #BAT
            if(choice == "BAT" and t < Max_iter):
                best_so_far, best_position_so_far, Positions = bat.BAT(objf, lb, ub, dim, SearchAgents_no, Max_iter, Positions, best_all, best_position,t)
                index = algorithm.index("BAT")
                algorithm.remove("BAT")
                prob = numpy.delete(prob, index)
                convergence_curve[t]=best_all
                                                                                 

            # #IWOA
            # if(choice == "IWOA" and t < Max_iter):                
            #     if Leader_score > best_all:
            #         Leader_score = best_all
            #         Leader_pos = best_position   
            #     best_all, best_position, Positions = f.iwoa(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Leader_pos, Leader_score)  
            #     index = algorithm.index("IWOA")
            #     algorithm.remove("IWOA")                
            #     prob = numpy.delete(prob, index)
            #     convergence_curve[t]=best_all 
            #     t=t+1

            # #CWOA
            # if(choice == "CWOA" and t < Max_iter):                
            #     if Leader_score > best_all:
            #         Leader_score = best_all
            #         Leader_pos = best_position   
            #     best_all, best_position, Positions = f.cwoa(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Leader_pos, Leader_score)  
            #     index = algorithm.index("CWOA")
            #     algorithm.remove("CWOA")                
            #     prob = numpy.delete(prob, index)
            #     convergence_curve[t]=best_all 
            #     t=t+1

            # #WOANL
            # if(choice == "WOANL" and t < Max_iter):                
            #     if Leader_score > best_all:
            #         Leader_score = best_all
            #         Leader_pos = best_position   
            #     best_all, best_position, Positions = f.woanl(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Leader_pos, Leader_score)  
            #     index = algorithm.index("WOANL")
            #     algorithm.remove("WOANL")                
            #     prob = numpy.delete(prob, index)
            #     convergence_curve[t]=best_all 
            #     t=t+1

            # #WOAAC
            # if(choice == "WOAAC" and t < Max_iter):                
            #     if Leader_score > best_all:
            #         Leader_score = best_all
            #         Leader_pos = best_position   
            #     best_all, best_position, Positions = f.woaac(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Leader_pos, Leader_score)  
            #     index = algorithm.index("WOAAC")
            #     algorithm.remove("WOAAC")                
            #     prob = numpy.delete(prob, index)
            #     convergence_curve[t]=best_all 
            #     t=t+1

            if(best_so_far < best_all):
                best_all = best_so_far
                best_position = best_position_so_far    

            if (t%1==0):
                print(['At iteration '+ str(t)+ ' the best fitness is '+ str(best_all)]); 

            if (t == Max_iter):
                break

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