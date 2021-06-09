# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:50:25 2016

@author: hossam
"""
from pathlib import Path
import optimizers.GWO as gwo
import optimizers.WOA as woa
import optimizers.PSO as pso
import optimizersDiogo.WOANL as woanl
import optimizersDiogo.WOA3 as woa3
import optimizersDiogo.IWOA as iwoa
import optimizersDiogo.IWOA2 as iwoa2
import optimizersDiogo.IWOA3 as iwoa3
import optimizersDiogo.WOAAC as woaac
import optimizersDiogo.CWOA as cwoa
import optimizersDiogo.ACO as aco
import optimizersDiogo.NCA as nca
import optimizersDiogo.MPA_original as mpa
import optimizers.BAT as bat
import optimizers.FFA as ffa
import optimizers.MFO as mfo
import optimizers.SSA as ssa
import benchmarks
import csv
import numpy
import time
import warnings
import os
import plot_convergence as conv_plot
import plot_boxplot as box_plot

warnings.simplefilter(action='ignore')


def selector(algo,func_details,popSize,Iter):
    function_name=func_details[0]
    lb=func_details[1]
    ub=func_details[2]
    dim=func_details[3]
    

    if(algo=="PSO"):
        x=pso.PSO(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)       
    elif(algo=="GWO"):
        x=gwo.GWO(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)     
    elif(algo=="WOA"):
        x=woa.WOA(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)
    elif(algo=="WOANL"):
        x=woanl.WOANL(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)
    elif(algo=="WOA3"):
        x=woa3.WOA3(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)    
    elif(algo=="IWOA"):
        x=iwoa.IWOA(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)
    elif(algo=="IWOA2"):
        x=iwoa2.IWOA2(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)
    elif(algo=="IWOA3"):
        x=iwoa3.IWOA3(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)
    elif(algo=="WOAAC"):
        x=woaac.WOAAC(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)    
    elif(algo=="CWOA"):
        x=cwoa.CWOA(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)   
    elif(algo=="NCA"):
        x=nca.NCA(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)
    elif(algo=="MPA"):
        x=mpa.MPA(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter) 
    elif(algo=="BAT"):
        x=bat.BAT(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)          
    elif(algo=="FFA"):
        x=ffa.FFA(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter) 
    elif(algo=="SSA"):
        x=ssa.SSA(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)
    elif(algo=="MFO"):
        x=mfo.MFO(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)  
    
    else:
        return null;
    return x


def run(optimizer, objectivefunc, NumOfRuns, params, export_flags):

    """
    It serves as the main interface of the framework for running the experiments.

    Parameters
    ----------    
    optimizer : list
        The list of optimizers names
    objectivefunc : list
        The list of benchmark functions
    NumOfRuns : int
        The number of independent runs 
    params  : set
        The set of parameters which are: 
        1. Size of population (PopulationSize)
        2. The number of iterations (Iterations)
    export_flags : set
        The set of Boolean flags which are: 
        1. Export (Exporting the results in a file)
        2. Export_details (Exporting the detailed results in files)
        3. Export_convergence (Exporting the covergence plots)
        4. Export_boxplot (Exporting the box plots)
    
    Returns
    -----------
    N/A
    """
    
    # Select general parameters for all optimizers (population size, number of iterations) ....
    PopulationSize = params['PopulationSize']
    Iterations= params['Iterations']
   
    #Export results ?
    Export=export_flags['Export_avg']
    Export_details=export_flags['Export_details']
    Export_convergence = export_flags['Export_convergence']
    Export_boxplot = export_flags['Export_boxplot']

    Flag=False
    Flag_details=False

    # CSV Header for for the cinvergence 
    CnvgHeader=[]

    results_directory = time.strftime("%Y-%m-%d-%H-%M-%S") + '/'
    Path(results_directory).mkdir(parents=True, exist_ok=True)

    for l in range(0,Iterations):
    	CnvgHeader.append("Iter"+str(l+1))


    for i in range (0, len(optimizer)):
        for j in range (0, len(objectivefunc)):
            convergence = [0]*NumOfRuns
            executionTime = [0]*NumOfRuns
            for k in range (0,NumOfRuns):               
                func_details=benchmarks.getFunctionDetails(objectivefunc[j])
                x=selector(optimizer[i],func_details,PopulationSize,Iterations)
                convergence[k] = x.convergence
                optimizerName = x.optimizer
                objfname = x.objfname     
                if(Export_details==True):
                    ExportToFile=results_directory + "experiment_details.csv"
                    with open(ExportToFile, 'a',newline='\n') as out:
                        writer = csv.writer(out,delimiter=',')
                        if (Flag_details==False): # just one time to write the header of the CSV file
                            header= numpy.concatenate([["Optimizer","objfname","ExecutionTime", "AVE", "STD"],CnvgHeader])
                            writer.writerow(header)
                            Flag_details=True # at least one experiment
                        executionTime[k] = x.executionTime
                        a=numpy.concatenate([[x.optimizer,x.objfname,x.executionTime, x.mean, x.std],x.convergence])
                        writer.writerow(a)
                    out.close()
                    
            if(Export==True):
                ExportToFile=results_directory + "experiment.csv"

                with open(ExportToFile, 'a',newline='\n') as out:
                    writer = csv.writer(out,delimiter=',')
                    if (Flag==False): # just one time to write the header of the CSV file
                        header= numpy.concatenate([["Optimizer","objfname","ExecutionTime"],CnvgHeader])
                        writer.writerow(header)
                        Flag=True

                    avgExecutionTime = float("%0.2f"%(sum(executionTime) / NumOfRuns))
                    avgConvergence = numpy.around(numpy.mean(convergence, axis=0, dtype=numpy.float64), decimals=2).tolist()
                    a=numpy.concatenate([[optimizerName,objfname,avgExecutionTime],avgConvergence])
                    writer.writerow(a)
                out.close()
    
    if Export_convergence == True:
        conv_plot.run(results_directory, optimizer, objectivefunc, Iterations)
    
    
    if Export_boxplot == True:
        box_plot.run(results_directory, optimizer, objectivefunc, Iterations)

    if (Flag==False): # Faild to run at least one experiment
        print("No Optomizer or Cost function is selected. Check lists of available optimizers and cost functions") 
            
            
