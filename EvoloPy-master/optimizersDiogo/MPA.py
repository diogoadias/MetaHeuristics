import random
import numpy
import math
from solution import solution
import time
import optimizersDiogo.functions as f
from numpy import matlib as mb

def MPA(objf,lb,ub,dim,SearchAgents_no,Max_iter, Prey, best_all, best_position,t):
    
    if not isinstance(lb, list):
        lb = [lb] * dim
    if not isinstance(ub, list):
        ub = [ub] * dim
            
    Top_predator_pos = numpy.zeros(dim)
    Top_predator_fit = float("inf")  

    stepsize = numpy.zeros((SearchAgents_no, dim))
    fitness = numpy.ones(dim) * numpy.inf

    Xmin = mb.repmat(numpy.ones(dim)*lb, SearchAgents_no, 1)
    Xmax = mb.repmat(numpy.ones(dim)*ub, SearchAgents_no, 1)

    FADs=0.2
    P=0.5 

    ############################ 

    print("MPA is optimizing  \""+objf.__name__+"\"")    

    timerStart=time.time() 
    ############################
        
    #t=0  # Loop counter
        
    # Main loop
    #while t<Max_iter:
        # Detecting top predator
    for i in range(0, len(Prey)):

        Flag4ub = Prey[i,:]>ub
        flag4lb = Prey[i,:]<lb
        Prey[i,:] = (Prey[i,:]*(~(Flag4ub+flag4lb)))+ub*Flag4ub+lb*flag4lb

        fitness = objf(Prey[i,:])

        if fitness < Top_predator_fit:
            Top_predator_fit = fitness
            Top_predator_pos = Prey[i,:]

        
    # Marine Memory saving
    fit_old = fitness
    Prey_old = Prey
    if t == 0:
        fit_old = fitness
        Prey_old = Prey

    Inx = (fit_old < fitness)
    Indx = numpy.full(shape=dim, fill_value=Inx)
    Prey = Indx*Prey_old +~Indx*Prey
    fitness = Inx*fit_old+~Inx*fitness

    fit_old = fitness
    Prey_old = Prey
    #############################################
            
    Elite = mb.repmat(Top_predator_pos, SearchAgents_no, 1)
    CF = (1-t/Max_iter)**(2*t/Max_iter)

    RL = 0.05 * f.levy(SearchAgents_no, dim, 1.5)
    RB = numpy.random.randn(SearchAgents_no, dim)

    for i in range(0, len(Prey)):
        for j in range(0, len(Prey[i])):
            R = random.random()

            # Phase 1
            if t < Max_iter/3:
                stepsize[i,j] = RB[i,j]*(Elite[i,j]-RB[i,j]*Prey[i,j])
                Prey[i,j] = Prey[i,j]+P*R*stepsize[i,j]
                
            # Phase 2
            elif t > Max_iter/3 and t<2*Max_iter/3:
                if i>len(Prey)/2:
                    stepsize[i,j] = RB[i,j]*(RB[i,j]*Elite[i,j]-Prey[i,j])
                    Prey[i,j] = Elite[i,j]+P*CF*stepsize[i,j]
                else:
                    stepsize[i,j] = RL[i,j]*(Elite[i,j]-RL[i,j]*Prey[i,j])
                    Prey[i,j] = Prey[i,j]+P*R*stepsize[i,j]
                
            # Phase 3
            else:
                stepsize[i,j] = RL[i,j]*(RL[i,j]*Elite[i,j]-Prey[i,j])
                Prey[i,j] = Elite[i,j]+P*CF*stepsize[i,j]
        
    # Detecting top predator
    for i in range(0, len(Prey)):

        Flag4ub = Prey[i,:] > ub
        flag4lb = Prey[i,:] < lb
        Prey[i,:] = (Prey[i,:]*(~(Flag4ub+flag4lb)))+ub*Flag4ub+lb*flag4lb

        fitness = objf(Prey[i,:])

        if fitness < Top_predator_fit:
            Top_predator_fit = fitness
            Top_predator_pos = Prey[i,:]

        
    # Marine Memory saving
    if t == 0:
        fit_old = fitness
        Prey_old = Prey

    Inx = (fit_old < fitness)
    Indx = numpy.full(shape=dim, fill_value=Inx)
    Prey = Indx*Prey_old+~Indx*Prey
    fitness = Inx*fit_old+~Inx * fitness

    fit_old = fitness
    Prey_old = Prey

    # Eddy formation and FADs
    if random.random() < FADs:
        U = numpy.random.randn(SearchAgents_no, dim) < FADs
        Prey = Prey+CF*((Xmin+numpy.random.randn(SearchAgents_no, dim)*(Xmax-Xmin))*U)
    else:
        r = random.random()
        Rs = len(Prey)
        stepsize = (FADs*(1-r)+r)*(Prey[numpy.random.permutation(Rs), :]-Prey[numpy.random.permutation(Rs), :])
        Prey = Prey+stepsize
        
       
    return Top_predator_fit, Top_predator_pos, Prey