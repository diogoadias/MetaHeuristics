# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:50:25 2016

@author: hossam
"""

from optimizer import run
import numpy

# Select optimizers
# "SSA","PSO","GA","BAT","FFA","GWO","WOA","MVO","MFO","CS","HHO","SCA","JAYA","DE"
#optimizer=["BAT", "FFA", "GWO", "MFO", "MPA", "PSO", "SSA", "WOA"]
optimizer=["NCA"]

# Select benchmark function"
# "F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","F13","F14","F15","F16","F17","F18","F19","F20","F21","F22","F23"
objectivefunc=["F14","F15","F16","F17","F18","F19","F20","F21","F22","F23"] 

# Select number of repetitions for each experiment. 
# To obtain meaningful statistical results, usually 30 independent runs are executed for each algorithm.
NumOfRuns=30

# Select general parameters for all optimizers (population size, number of iterations) ....
params = {'PopulationSize' : 30, 'Iterations' : 500}

#Choose whether to Export the results in different formats
export_flags = {'Export_avg':True, 'Export_details':True, 
'Export_convergence':True, 'Export_boxplot':False}

run(optimizer, objectivefunc, NumOfRuns, params, export_flags)