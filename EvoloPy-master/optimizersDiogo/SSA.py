import random
import numpy
import math
from solution import solution
import time



  
def SSA(objf,lb,ub,dim,N,Max_iteration,Positions, best_all, best_position,t):


    #Max_iteration=1000
    #lb=-100
    #ub=100
    #dim=30
    N=dim # Number of search agents
           
    #Initialize the positions of salps
    SalpPositions = Positions
    
    SalpFitness=numpy.full(N,float("inf"))
    
    FoodPosition=best_position
    FoodFitness=best_all
    #Moth_fitness=numpy.fell(float("inf"))
    
    print("SSA is optimizing  \""+objf.__name__+"\"")    

    timerStart=time.time()     
    
    for i in range(0,N):
       # evaluate moths
        SalpFitness[i]=objf(SalpPositions[i,:]) 
        
        
    sorted_salps_fitness=numpy.sort(SalpFitness)
    I=numpy.argsort(SalpFitness)
    
    Sorted_salps=numpy.copy(SalpPositions[I,:])
       
    
    FoodPosition=numpy.copy(Sorted_salps[0,:])
    FoodFitness=sorted_salps_fitness[0]
    
   
    
        
    Iteration=t;    
    
    # Main loop
    #while (Iteration<Max_iteration):
        
    # Number of flames Eq. (3.14) in the paper
    #Flame_no=round(N-Iteration*((N-1)/Max_iteration));
        
    c1 = 2*math.exp(-(4*Iteration/Max_iteration)**2); # Eq. (3.2) in the paper

    for i in range(0,N):
            
        SalpPositions= numpy.transpose(SalpPositions);

        if i<N/2:
            for j in range(0,dim):
                c2=random.random()
                c3=random.random()
                #Eq. (3.1) in the paper 
                if c3<0.5:
                    SalpPositions[j,i]=FoodPosition[j]+c1*((ub[j]-lb[j])*c2+lb[j]);
                else:
                    SalpPositions[j,i]=FoodPosition[j]-c1*((ub[j]-lb[j])*c2+lb[j]);

                ####################
            
            
        elif i>=N/2 and i<N+1:
            point1=SalpPositions[:,i-1];
            point2=SalpPositions[:,i];
                
            SalpPositions[:,i]=(point2+point1)/2; # Eq. (3.4) in the paper
        
        
        SalpPositions= numpy.transpose(SalpPositions);
        
           
    for i in range(0,N):
        
        # Check if salps go out of the search spaceand bring it back
        for j in range(dim):
            SalpPositions[i,j]=numpy.clip(SalpPositions[i,j], lb[j], ub[j])            
         
        SalpFitness[i]=objf(SalpPositions[i,:]);
          
        if SalpFitness[i]<FoodFitness:
            FoodPosition=numpy.copy(SalpPositions[i,:])
            FoodFitness=SalpFitness[i]


    #Display best fitness along the iteration
    #if (Iteration%1==0):
            
    
    
    return FoodFitness, FoodPosition, SalpPositions
    




