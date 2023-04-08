#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Shikhara Bhat
Email ID: shikharabhat@gmail.com
Date created: 2022-11-25 19:49:12
Date last modified: 2022-11-25 19:49:12
Purpose: This script puts together everything for running on a HPC like PARAM
This will be parallelized across nodes using an array job on SLURM. Code written
for simulating a stochastic birth-death process for the evolution of a quantitative trait.
Part of an MS thesis under Dr. Vishwesha Guttal and Prof. Rohini Balakrishnan at 
the Centre for Ecological Sciences, Indian Institute of Science.
'''
import argparse
from set_up_parallelization import run_parallel_simulations

#import the specific ecological model you want over here
from eco_models import logistic
from eco_model_params import logistic_branching_asymm as model_params


if __name__ == "__main__": 
     
     #the if condition makes sure that arguments are asked for only when this file is the main program
     #being run i.e ($ python3 filename.py) and not when it is imported in another piece of code (import filename.py)


     parser = argparse.ArgumentParser(description="Stochastic Birth-Death process for the evolution of quantitative traits")
     parser.add_argument("-K", "--system_size", dest="K", help="System size parameter (controls total population size)", required=True)

     args = parser.parse_args() 
     K = float(args.K)

##################################################################################
#simulation parameters
runs = 15 #number of realizations for a given system size
M = 100 #number of distinct phenotypes that can coexist at a given time
sim_params = {'T':100*100,'steps':10000*100,'skip':10,'mutation_rate':0.1,'mutation_effect':0.05}
save_dir = '/scratch/shikharabhat/MS_thesis/output/'

#for local testing (comment out when running on HPC)
#runs = 10 #number of realizations for a given system size
#M = 100 #number of distinct phenotypes that can coexist at a given time
#sim_params = {'T':10,'steps':1000,'skip':10,'mutation_rate':0.1,'mutation_effect':0.05}
#save_dir = 'testing/'

#################################################################################
#Run the model
run_parallel_simulations(K0=K,eco_model=logistic,model_params=model_params,save_dir=save_dir,runs=runs, M=M,sim_params=sim_params)
