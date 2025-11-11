# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:50:25 2016

@author: hossam
"""

from optimizer import run
import numpy

# Select optimizers
# "SSA","PSO","GA","BAT","FFA","GWO","WOA","MVO","MFO","CS","HHO","SCA","JAYA","DE"
#optimizer=["BAT", "FFA", "GWO", "MPA", "PSO", "WOA"]
#optimizer=["MSSWOA","MPA", "IWOA", "IWOA2_original", "IWOA3", "WOAAC", "WOANL", "CWOA"]
#optimizer=["MSSWOA", "MSSWOAv2", "MSSWOAv3", "MSSWOAv4"]
#optimizer=["MSSWOAv4"]
optimizer=["WOANLv2"]

# Select benchmark function"
# "F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","F13","F14","F15","F16","F17","F18","F19","F20","F21","F22","F23"
# "F8","F16","F19","F20","F21","F22","F23"
# "F1","F2","F3","F4","F5","F6","F7","F9","F10","F11","F12","F13","F14","F15","F17","F18"
# "welded_beam_cost"
objectivefunc=["welded_beam_cost"]

# Select number of repetitions for each experiment. 
# To obtain meaningful statistical results, usually 30 independent runs are executed for each algorithm.
NumOfRuns=30

# Select general parameters for all optimizers (population size, number of iterations) ....
params = {'PopulationSize' : 20, 'Iterations' : 500}

#Choose whether to Export the results in different formats
export_flags = {'Export_avg':True, 'Export_details':True, 
'Export_convergence':True, 'Export_boxplot':False, 'Export_details_MSSWOA':False}

run(optimizer, objectivefunc, NumOfRuns, params, export_flags)