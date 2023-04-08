#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Shikhara Bhat
Email ID: shikharabhat@gmail.com
Date created: 2022-11-24 15:13:13
Date last modified: 2022-11-24 15:13:13
Purpose: Run a simulation for a given model/parameters
'''
import numpy as np
import pandas as pd
import multiprocessing as mp
import time
import os
from functools import partial
from BD_algo import bd_process
from plot_results import plot_density


def single_run(run,M,save_dir,eco_model,model_params,sim_params):

    ''''
    Run a Gillespie and save the output to CSV. Also save figures as SVGs in a subfolder.
    args:
    M (int > 0) - How many different kinds of phenotypes can exist at a given time
    run (int > 0) - Just a label for which realization this is. We will change this label when looping.
    save_dir (str) - Location in which to store the results
    eco_model (func) - Function that returns the growth rate of a given phenotype in a given population. This specifies the ecology of the system. See eco_models.py
    model_params (dict) - a dict of kwargs to pass to the ecological model. See eco_model_params.py
    sim_params (dict) - a dict of kwargs to pass to bd_process. We require the following:
                        'T' (float > 0): Final time upto which to run the simulation
                        'step' (int > 0): Divide T into 'step' timesteps, over which birth/death rates are assumed constant
                        'skip' (int > 0): Save the state of the population every 'skip' timesteps
                        'mutation_rate' (float in (0,1)): probability of mutation per unit time
                        'mutation_effect' (float > 0): Mutations are drawn from a normal dist. with SD mutation_effect
    '''
   
    #random seed, to ensure different processes running in parallel do not get the same seed
    np.random.seed((os.getpid() * int(time.time())) % 123456789)

    #initial conditions - Arbitrarily chosen in this case
    init_pheno = np.array([np.random.normal(0,0.015) for i in range(M)])

    #simulate the process
    traj, ptraj, tlist = bd_process(
                                    state=np.array([model_params['K0']]*M), #initial pop numbers
                                    phenotypes=init_pheno, #initial phenotypes
                                    get_rates=partial(eco_model, **model_params), #ecological model
                                    umin=-5, #min allowed phenotype
                                    umax=5, #max allowed phenotype
                                    **sim_params #other simulation parameters
                                    )
    

    #See if a sub-folder exists for the plots. If it does not, then create it.
    if not os.path.exists(save_dir+'/plots/'):
        os.makedirs(save_dir+'/plots/')
    
    #plot trajectory and save to file
    plot_density(traj,ptraj,tlist,plot_dir=save_dir+'/plots/'+'K0_'+str(model_params['K0'])+'_beta_'+str(model_params['beta'])+'_run_'+str(run))

    #convert lists to dataframes to save to CSV
    traj = pd.DataFrame(traj)
    ptraj = pd.DataFrame(ptraj)

    #include time as column names (questionable choice)
    #TODO: Figure out a smarter way to store the data

    [traj.rename(mapper={i:tlist[i]},axis='columns',inplace=True) for i in range(len(tlist))]
    [ptraj.rename(mapper={i:tlist[i]},axis='columns',inplace=True) for i in range(len(tlist))]

    save_name = save_dir+'K0_'+str(model_params['K0'])+'_beta_'+str(model_params['beta'])+'_run_'+str(run)
    traj.to_csv(save_name+'_poptraj.csv',index=False)
    ptraj.to_csv(save_name+'_phenotraj.csv',index=False)

    del traj, ptraj, tlist #to save memory

def run_parallel_simulations(M,K0,runs,save_dir,eco_model,model_params,sim_params):

    '''
    Parallelize simulations for different realizations across cores using multiprocessing
    This script will simulate 'runs' number of realizations and save the outputs to file

    We will parallelize this function over nodes for different K0 values using SLURM in the 'main' script.

    args:
    M (int > 0) - How many different kinds of phenotypes can exist at a given time
    K0 (float > 0) - System size
    runs (int > 0) - Number of realizations to simulate
    save_dir (str) - Location in which to store the results
    eco_model (func) - Function that returns the growth rate of a given phenotype in a given population. This specifies the ecology of the system. See eco_models.py
    model_params (dict) - a dict of kwargs to pass to the ecological model. See eco_model_params.py
    sim_params (dict) - a dict of kwargs to pass to bd_process. We require the following:
                        'T' (float > 0): Final time upto which to run the simulation
                        'step' (int > 0): Divide T into 'step' timesteps, over which birth/death rates are assumed constant
                        'skip' (int > 0): Save the state of the population every 'skip' timesteps
                        'mutation_rate' (float in (0,1)): probability of mutation per unit time
                        'mutation_effect' (float > 0): Mutations are drawn from a normal dist. with SD mutation_effect
    '''
    
    #Make a single dict to contain all the params that are common across realizations
    common_params = {'M':M,'save_dir':save_dir,'eco_model':eco_model,'model_params':{'K0':K0,**model_params},'sim_params':sim_params}
    
    partial_func = partial(single_run,**common_params) #create a partial function that has everything other than runs

    #partial_func(1)
    #Parallelize across cores
    usable_cores = len(os.sched_getaffinity(0)) #you need this because mp.cpu_count() doesn't work correctly if CPUs are dynamically activated on linux systems. See https://stackoverflow.com/a/31345046
    pool = mp.Pool(usable_cores) #Initialize a Pool instance that uses all possible cores
    pool.imap(partial_func,range(1,runs+1)) #Execute the different runs in parallel
    pool.close()
    pool.join() #make sure everything runs
