
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

def chaotic(dim, a, k, pos_value):
    # a = linear decreases, k = last position value
    result = float("inf")
    # Chaotic maps
    cm = numpy.random.choice(numpy.arange(8))
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
        result = math.fmod(pos_value+b-(a/2*math.pi)*math.sin(2*math.pi*k, 1))
    elif cm == 7:
        # Iterative
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