
import numpy 
import random
import math

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
        w_final = 1
        w_initial = 0.0
        S = 1
        c = 1
        
        iw = numpy.random.choice(numpy.arange(3)) # random between inertia weights formulas 

        if iw == 1:
            w = w_initial - (w_initial - w_final)*(t/Max_iter) # introduced by Shi and Eberhart[12] who introduce a Linear Decreasing Inertia Weight(LDIW) strategy in 1998    
        elif iw == 2:
            w = (1-t/Max_iter) / (1+S*(t/Max_iter)) 
        else:
            w = w_final + ((w_initial-w_final)*math.exp(-(c*t/Max_iter)))

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

def cwoa(objf, t, Max_iter, SearchAgents_no, dim, Positions, lb, ub, Leader_pos, Leader_score):
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

            # Chaotic maps
            # cm = numpy.random.choice(numpy.arange(8))
            cm = 8

            if cm == 1:
                # Logistic
                Positions[i,j] = a*Positions[i,j]*(1-Positions[i,j])
            elif cm == 2:
                # Cubic
                Positions[i,j] = a*Positions[i,j]*(1-(Positions[i,j]**2))
            elif cm == 3:
                # Sine
                Positions[i,j] = (a/4)*math.sin(math.pi*Positions[i,j])
            elif cm == 4:
                # Sinusoidal
                Positions[i,j] = a*(Positions[i,j]**2)*math.sin(math.pi*Positions[i,j])
            elif cm == 5:
                # Singer
                u = 1.07
                Positions[i,j] = u*(7.86*Positions[i,j]-23.31*(Positions[i,j]**2)+28.75*(Positions[i,j]**3)-13.302875*(Positions[i,j]**4))
            elif cm == 6:
                # Circle
                b = 1
                k = dim -1
                Positions[i,j] = math.fmod(Positions[i,j]+b-(a/2*math.pi)*math.sin(2*math.pi*Positions[i,k]), 1)
            elif cm == 7:
                # Iterative
                Positions[i,j] = math.sin((a*math.pi)/Positions[i,j])
            elif cm == 8:
                # Tent Chaotic Map
                if(Positions[i,j] < 0.7):
                    Positions[i,j] = Positions[i,j] / 0.7
                else:
                    Positions[i,j] = (10/3)*(1-Positions[i,j]) 
                    
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

def woanl(objf, t, Max_iter, SearchAgents_no, dim, Positions, lb, ub, Leader_pos, Leader_score):
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
    
    a = 2+2*math.cos(math.pi/2*(1+t/Max_iter)) # a decreases non-linearly

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

def woaac(objf, t, Max_iter, SearchAgents_no, dim, Positions, lb, ub, Leader_pos, Leader_score):
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
       

    #a=2-t*((2)/Max_iter); # a decreases linearly fron 2 to 0 in Eq. (2.3)
                 
    # a2 linearly decreases from -1 to -2 to calculate t in Eq. (3.12)
    a2=-1+t*((-1)/Max_iter);
                    
    # Update the Position of search agents 
    for i in range(0,SearchAgents_no):
        r1=random.random() # r1 is a random number in [0,1]
        r2=random.random() # r2 is a random number in [0,1]

        a = 2-math.cos(r1)*(t-1/Max_iter-1) # A-C Parametric

        A=2*a*r1-a  # Eq. (2.3) in the paper
            
        #C=2*r2      # Eq. (2.4) in the paper
           
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