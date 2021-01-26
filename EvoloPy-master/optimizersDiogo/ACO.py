import numpy as np
import time
import math
from solution import solution

def ACO (objf,lb,ub,dim,SearchAgents_no,Max_iter):
    # Parameters
    pheromone = np.ones((SearchAgents_no, dim)) # create pheromone matrix       
    n_ants = SearchAgents_no # number of ants 
    n_best = 1 # quantity of best ants
    evaporation = 0.5 # evaporation tax
    alpha = 1
    beta = 1

    if not isinstance(lb, list):
        lb = [lb] * dim
    if not isinstance(ub, list):
        ub = [ub] * dim
            
        
    # initialize position vector and score for the leader
    best_ant_pos=np.zeros(dim)
    best_ant_score=float("inf")  #change this to -inf for maximization problems
        
        
    # #Initialize the positions of search agents
    Positions = np.zeros((SearchAgents_no, dim))
    for i in range(dim):
        Positions[:, i] = np.random.uniform(0,1,SearchAgents_no) *(ub[i]-lb[i])+lb[i]
    
    #Initialize convergence
    convergence_curve=np.zeros(Max_iter)
        
        
    ############################
    s=solution()

    print("ACO is optimizing  \""+objf.__name__+"\"")    

    timerStart=time.time() 
    s.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    ############################
        
    t=0  # Loop counter

    # Main loop
    while t<Max_iter:
        for i in range(0,SearchAgents_no):
                
            # Return back the search agents that go beyond the boundaries of the search space
               
            #Positions[i,:]=checkBounds(Positions[i,:],lb,ub)
            for j in range(dim):        
                Positions[i,j]=np.clip(Positions[i,j], lb[j], ub[j])
                
            # Calculate objective function for each search agent
            fitness=objf(Positions[i,:])
               
            # Update the leader
            if fitness < best_ant_score: # Change this to > for maximization problem
                best_ant_score=fitness; # Update fitness
                best_ant_pos=Positions[i,:].copy() # copy current ant position into the leader position
            
        # Calculate probabilities
        probs = np.ones((SearchAgents_no, dim))        
        for i in range(0,SearchAgents_no):   
            for j in range(dim):
                total_neighbor = 0.0
                total_pheromone = 0.0
                for k in range(dim):
                    if k > j:
                        total_neighbor += 1.0 / Positions[i][k]
                        total_pheromone += pheromone[i][k]
                                                     
                if i == j:
                    probs[i][j] = 0.0
                else:
                    if total_neighbor <= 0.0:
                        total_neighbor = 1.0
                    
                    a_value = (pheromone[i][j]**alpha) * (1.0 / Positions[i][j])**beta  
                    b_value = (total_pheromone**alpha) * (total_neighbor**beta)
                    if b_value <= 0.0:
                        b_value = 1.0    
                    value = a_value / b_value
                    if value < 0.0:
                        probs[i][j] = abs(value)
                    else:
                        probs[i][j] = value
            
            probs[i][:] /= sum(probs[i][:]) # normalize probabilities

            
            path = []
            route = Positions[i][:].copy()
            p=probs[i][:]
            for j in range(dim):
                if i != j:                
                    next_city = np.random.choice(len(route), p=p)
                    path.append(next_city)
                    # route = np.delete(route, next_city)
                    # p = np.delete(p, next_city)
                    np.put(p, next_city, 0.0)                
                    p /= sum(p)
                    print(sum(p))
                    print(path)
                
            distance1 = sum(Positions[i][:])
            distance2 = 0.0
            for j in range(dim):
                index = path[j]
                distance2 += Positions[i][index]
                Positions[i][j] = Positions[i][index]   

            # Update Pheromone  
            for j in range(dim):
                q = 1.0 / distance2 #quantity of pheromone spread
                pheromone[i][j] += ((1.0 - evaporation) * q) + pheromone[i][j] #update pheromone in the path



        convergence_curve[t]=best_ant_score
        if (t%1==0):
            print(['At iteration '+ str(t)+ ' the best fitness is '+ str(best_ant_score)])
            print(path)
        t=t+1
        
    timerEnd=time.time()  
    s.endTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime=timerEnd-timerStart
    s.convergence=convergence_curve
    s.optimizer="ACO"   
    s.objfname=objf.__name__
    s.best = best_ant_score
    s.bestIndividual = best_ant_pos
    s.std = np.std(convergence_curve)
    s.mean = np.mean(convergence_curve)
       
    return s    