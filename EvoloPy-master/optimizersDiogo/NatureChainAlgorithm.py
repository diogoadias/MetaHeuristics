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
import optimizersDiogo.WOA as woaOriginal

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
    A=0.5;      # Loudness  (constant or decreasing)
    r=0.5;      # Pulse rate (constant or decreasing)
    
    Qmin=0         # Frequency minimum
    Qmax=2         # Frequency maximum

    Q=numpy.zeros(SearchAgents_no)  # Frequency
    v=numpy.zeros((SearchAgents_no,dim))  # Velocities
    fmin = float("inf")
        
        
    # #Initialize the positions of search agents
    Positions = numpy.zeros((SearchAgents_no, dim))
    for i in range(dim):
        Positions[:, i] = numpy.random.uniform(0,1,SearchAgents_no) *(ub[i]-lb[i])+lb[i]
  

    #Initialize convergence
    convergence_curve=numpy.zeros(Max_iter)        
        
    ############################
    s=solution()

    print("NCA is optimizing  \""+objf.__name__+"\"")    

    timerStart=time.time() 
    s.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    ############################
        
    t=0  # Loop counter
        
    # Main loop
    while t<Max_iter:
        
         #PSO
        if gBestScore > best_all:
            gBestScore = best_all
            gBest = best_position        
        best_all, best_position, Positions = pso(objf, t, Max_iter, SearchAgents_no, dim, Positions, lb, ub, Vmax, wMax, wMin, c1, c2, vel, pBest, gBest, pBestScore, gBestScore)            

        #GWO
        if Alpha_score > best_all:
            Alpha_score = best_all
            Alpha_pos = best_position            
        best_all, best_position, Positions = gwo(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Alpha_pos, Beta_pos, Delta_pos, Alpha_score,  Beta_score,  Delta_score)               
        
        #WOA
        if Leader_score > best_all:
            Leader_score = best_all
            Leader_pos = best_position   
        best_all, best_position, Positions = woa(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Leader_pos, Leader_score)        
        
        #Inertia WOA
        if Leader_score > best_all:
            Leader_score = best_all
            Leader_pos = best_position   
        best_all, best_position, Positions = iwoa(objf, t, Max_iter, SearchAgents_no, dim, Positions,lb, ub, Leader_pos, Leader_score)        
        

        #BAT
        # if fmin > best_all:
        #     fmin = best_all
        #     best = best_position
        # best_all, best_position, Positions = bat(objf, t, Max_iter, SearchAgents_no, dim, Positions, lb, ub,A, r, Qmin, Qmax, Q, v, fmin, best)


        convergence_curve[t]=best_all
        if (t%1==0):
            print(['At iteration '+ str(t)+ ' the best fitness is '+ str(best_all)]);
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
    s.mean = numpy.mean(convergence_curve)
       
    return s

def gwo(objf, t, Max_iter, SearchAgents_no, dim, Positions, lb, ub, Alpha_pos, Beta_pos, Delta_pos, Alpha_score, Beta_score, Delta_score):
    for i in range(0,SearchAgents_no):
        #Positions[i,:]=checkBounds(Positions[i,:],lb,ub)
            for j in range(dim):        
                Positions[i,j]=numpy.clip(Positions[i,j], lb[j], ub[j])
                
            # Calculate objective function for each search agent
            fitness=objf(Positions[i,:])

        # Update Alpha, Beta, and Delta (gwo)
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
    
    return Alpha_score,Alpha_pos, Positions

def woa(objf, t, Max_iter, SearchAgents_no, dim, Positions, lb, ub, Leader_pos, Leader_score):
    for i in range(0,SearchAgents_no):         
               
            #Positions[i,:]=checkBounds(Positions[i,:],lb,ub)
            for j in range(dim):        
                Positions[i,j]=numpy.clip(Positions[i,j], lb[j], ub[j])
                
            # Calculate objective function for each search agent
            fitness=objf(Positions[i,:])
               
            # Update the leader (woa)
            if fitness<Leader_score: # Change this to > for maximization problem
                Leader_score=fitness; # Update alpha
                Leader_pos=Positions[i,:].copy() # copy current whale position into the leader position
    
    a=2-t*((2)/Max_iter); # a decreases linearly fron 2 to 0 in Eq. (2.3)

    # a2 linearly decreases from -1 to -2 to calculate t in Eq. (3.12)
    a2=-1+t*((-1)/Max_iter);       

    # Update the Position of search agents 
    for i in range(0,SearchAgents_no):
        r1=random.random() # r1 is a random number in [0,1]
        r2=random.random() # r2 is a random number in [0,1]

        A=2*a*r1-a  # Eq. (2.3) in the paper
        C=2*r2      # Eq. (2.4) in the paper

        b=1;               #  parameters in Eq. (2.5)
        l=(a2-1)*random.random()+1   #  parameters in Eq. (2.5)

        p = random.random()        # p in Eq. (2.6)

        for j in range(0,dim):

            if p<0.5:
                if abs(A)>=1:
                    rand_leader_index = math.floor(SearchAgents_no*random.random());
                    X_rand = Positions[rand_leader_index, :]
                    D_X_rand=abs(C*X_rand[j]-Positions[i,j]) 
                    Positions[i,j]=X_rand[j]-A*D_X_rand      

                elif abs(A)<1:
                    D_Leader=abs(C*Leader_pos[j]-Positions[i,j]) 
                    Positions[i,j]=Leader_pos[j]-A*D_Leader      


            elif p>=0.5:

                distance2Leader=abs(Leader_pos[j]-Positions[i,j])
                # Eq. (2.5)
                Positions[i,j]=distance2Leader*math.exp(b*l)*math.cos(l*2*math.pi)+Leader_pos[j]
    
    return Leader_score, Leader_pos, Positions

def pso(objf, t, Max_iter, SearchAgents_no, dim, Positions, lb, ub, Vmax, wMax, wMin, c1, c2, vel, pBest, gBest, pBestScore, gBestScore):
    for i in range(0,SearchAgents_no):
        #pos[i,:]=checkBounds(pos[i,:],lb,ub)
        for j in range(dim):
            Positions[i, j] = numpy.clip(Positions[i,j], lb[j], ub[j])
        #Calculate objective function for each particle
        fitness=objf(Positions[i,:])
    
        if(pBestScore[i]>fitness):
            pBestScore[i]=fitness
            pBest[i,:]=Positions[i,:].copy()
                
        if(gBestScore>fitness):
            gBestScore=fitness
            gBest=Positions[i,:].copy()
        
    #Update the W of PSO
    w=wMax-t*((wMax-wMin)/Max_iter);
        
    for i in range(0,SearchAgents_no):
        for j in range (0,dim):
            r1=random.random()
            r2=random.random()
            vel[i,j]=w*vel[i,j]+c1*r1*(pBest[i,j]-Positions[i,j])+c2*r2*(gBest[j]-Positions[i,j])
                
            if(vel[i,j]>Vmax):
                vel[i,j]=Vmax
                
            if(vel[i,j]<-Vmax):
                vel[i,j]=-Vmax
                            
            Positions[i,j]=Positions[i,j]+vel[i,j]
    
    return gBestScore, gBest, Positions

def bat(objf, t, Max_iter, SearchAgents_no, dim, Positions, lb, ub,A, r, Qmin, Qmax, Q, v, fmin, best):
    
    S=numpy.zeros((SearchAgents_no,dim))
    S=numpy.copy(Positions)
    Fitness=numpy.zeros(SearchAgents_no)

    # Find the initial best solution
    I=numpy.argmin(Fitness)
    best=Positions[I,:]

   

    # Loop over all bats(solutions)
    for i in range (0,SearchAgents_no):
        Q[i]=Qmin+(Qmin-Qmax)*random.random()
        v[i,:]=v[i,:]+(Positions[i,:]-best)*Q[i]
        S[i,:]=Positions[i,:]+v[i,:]
          
        # Check boundaries
        for j in range(dim):
            Positions[i,j] = numpy.clip(Positions[i,j], lb[j], ub[j])
            
        # Pulse rate
        if random.random()>r:
            S[i,:]=best+0.001*numpy.random.randn(dim)
 
        # Evaluate new solutions
        Fnew=objf(S[i,:])
          
        # Update if the solution improves
        if ((Fnew<=Fitness[i]) and (random.random()<A) ):
            Positions[i,:]=numpy.copy(S[i,:])
            Fitness[i]=Fnew;
   
        # Update the current best solution
        if Fnew<=fmin:
            best=numpy.copy(S[i,:])
            fmin=Fnew

    return fmin, best, Positions

def iwoa(objf, t, Max_iter, SearchAgents_no, dim, Positions, lb, ub, Leader_pos, Leader_score):
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
       
        # Inertia weight
        w_final=0.9
        w_initial=0.2
        w = w_initial - (w_initial - w_final)*(t/Max_iter) # introduced by Shi and Eberhart[12] who introduce a Linear Decreasing Inertia Weight(LDIW) strategy in 1998    
        
        a=2-t*((2)/Max_iter); # a decreases linearly fron 2 to 0 in Eq. (2.3)
                   
        # a2 linearly decreases from -1 to -2 to calculate t in Eq. (3.12)
        a2=-1+t*((-1)/Max_iter);
                    
        # Update the Position of search agents 
        for i in range(0,SearchAgents_no):
            r1=random.random() # r1 is a random number in [0,1]
            r2=random.random() # r2 is a random number in [0,1]
                
            A=2*a*r1-a  # Eq. (2.3) in the paper
            C=2*r2      # Eq. (2.4) in the paper
                    
            b=1;               #  parameters in Eq. (2.5)
            l=(a2-1)*random.random()+1   #  parameters in Eq. (2.5)
                
            p = random.random()        # p in Eq. (2.6)
                
            for j in range(0,dim):
                    
                if p<0.5:
                    if abs(A)>=1:
                        rand_leader_index = math.floor(SearchAgents_no*random.random());
                        X_rand = Positions[rand_leader_index, :]
                        D_X_rand=abs(w*C*X_rand[j]-Positions[i,j]) 
                        Positions[i,j]=w*X_rand[j]-A*D_X_rand      
                            
                    elif abs(A)<1:
                        D_Leader=abs(C*w*Leader_pos[j]-Positions[i,j]) 
                        Positions[i,j]=w*Leader_pos[j]-A*D_Leader     
                        
                        
                elif p>=0.5:
                    
                    distance2Leader=abs(Leader_pos[j]-Positions[i,j])
                    # Eq. (2.5)
                    Positions[i,j]=distance2Leader*math.exp(b*l)*math.cos(l*2*math.pi)+Leader_pos[j]*w
    return Leader_score, Leader_pos, Positions                          