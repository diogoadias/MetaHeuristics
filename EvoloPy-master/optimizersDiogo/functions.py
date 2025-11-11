
from decimal import ROUND_HALF_DOWN
import numpy 
import random
import math

def levy(n, m, beta):
    num = math.gamma(1+beta)*math.sin(math.pi*beta/2)
    den = math.gamma((1+beta)/2)*beta*2**((beta-1)/2)
    sigma_u = (num/den)**(1/beta)
    u = numpy.random.normal(0, sigma_u, (n,m))
    v = numpy.random.normal(0, 1, (n,m))
    z = u/(abs(v)**(1/beta))

    return z

def chaotic(a, pos_value):
    # a = linear decreases, k = last position value
    result = float("inf")
    # Chaotic maps
    #if cm is None:
    #cm = numpy.random.choice(numpy.arange(8))
    cm=1
    if math.isinf(pos_value):
        pos_value = random.randrange(-100, 100)
    if pos_value == 0:
        pos_value = 1    
       

    if cm == 1:
        # Logistic
       result = a*pos_value*(1-pos_value)
    elif cm == 2:
        # Cubic
        result = a*pos_value*(1-(pos_value**2))
    elif cm == 3:
        # Sine
        result = (a/4)*math.sin(math.pi*pos_value)
    elif cm == 4:
        # Sinusoidal
        result = a*(pos_value**2)*math.sin(math.pi*pos_value)
    elif cm == 5:
        # Singer
        u = 1.07
        result = u*(7.86*pos_value-23.31*(pos_value**2)+28.75*(pos_value**3)-13.302875*(pos_value**4))
    elif cm == 6:
        # Circle
        b = 1
        #k = dim -1
        #result = math.fmod(pos_value+b-(a/2*math.pi)*math.sin(2*math.pi*Positions[i,k]), 1)
        result = math.fmod(pos_value+b-(a/2*math.pi)*math.sin(2*math.pi*pos_value), 1)
    elif cm == 7:
        #Iterative
        result = math.sin((a*math.pi)/pos_value)
    elif cm == 8:
        # Tent Chaotic Map
        if(pos_value < 0.7):
            result = pos_value / 0.7
        else:
            result = (10/3)*(1-pos_value)
    
    return result

def inertia(t, Max_iter):
    # Inertia weight
    w_final=1
    w_initial=0.0
    w = w_initial - (w_initial - w_final)*(t/Max_iter) # introduced by Shi and Eberhart[12] who introduce a Linear Decreasing Inertia Weight(LDIW) strategy in 1998
    return w

def generate_chaos(a, pop):
         
    for i in range(0,len(pop)):
        for j in range(0, len([i])):
            pop[i,j] = chaotic(a, pop[i,j])
    
    return pop

def levy_population(pop, best_pop, stepsize, dim, t, Max_iter):
    searchAgents_no = 30
    P=0.5
    beta = 1.5
    RL = 0.05 * levy(searchAgents_no, dim, beta) #beta=1.5
    CF = (1-t/Max_iter)**(2*t/Max_iter)

    for i in range(0, len(pop)):
        for j in range(0, len(pop[i])):
    
            stepsize[i,j] = RL[i,j]*(RL[i,j]*best_pop[j]-pop[i,j])
            pop[i,j] = best_pop[j]+P*CF*stepsize[i,j]

    return pop, stepsize

def brownian(pop, best_pop, stepsize, dim,):
    searchAgents_no = 30
    P=0.5
    R = random.random()
    RB = numpy.random.randn(searchAgents_no, dim)

    for i in range(0, len(pop)):
        for j in range(0, len(pop[i])):
            stepsize[i,j] = RB[i,j]*(best_pop[j]-RB[i,j]*pop[i,j])
            pop[i,j] = pop[i,j]+P*R*stepsize[i,j]

    return pop, stepsize