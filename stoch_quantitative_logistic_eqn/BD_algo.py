#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Shikhara Bhat
Email ID: shikharabhat@gmail.com
Date created: 2022-11-21 16:59:54
Date last modified: 2022-11-21 16:59:54
Purpose: Approximate simulation of a birth-death process.
From https://www.normalesup.org/~doulcier/teaching/adaptive_dynamics/dyad02.html
'''
import numpy as np
from itertools import chain


def bd_process(T, steps, skip, state,
                         phenotypes, mutation_rate,
                         mutation_effect, get_rates,
                         umin=0, umax=1):
    """ Perform a stochastic simulation of the birth-death process with mutations. 
    
    Args:
        T (float): Final time. The process is simulated on [0,T].
        steps (int): number of time division. 
        skip (int): only save one every `skip` state
        state (np.array of int): the number of individual of each type.
        phenotypes (np.array of floats): the value of the trait of each type.       
        get_rates (function): a functio that maps state,phenotypes to a list of growth rate. (ecological model).
        
    Returns:
        trajectory (np.array of int, shape= (len(state), steps)) 
        pheno_traj (np.array of floats, shape= (len(state), steps)) 
    """
    M = len(state) # number of different phenotypes
    
    # Initialize the data structure for the trajectory 
    trajectory = np.zeros((M,steps//skip), dtype=int)
    pheno_traj = np.zeros((M,steps//skip))
    trajectory[:,0] = state
    pheno_traj[:,0] = phenotypes
    new_state = np.zeros(M,dtype=np.float64)
    tlist = np.zeros(steps//skip)
    dt = T/steps 
    for t in range(1,steps):
        # at each time step we compute the new rates
        rates = get_rates(phenotypes, state)
        nmutants = np.zeros(M, dtype=int)
        
        # for each type, we compute the new number of individuals, and the number of mutants.
        for i in range(M):        
            if state[i]:
                try:
                    new_state[i] = np.random.poisson(state[i]*np.exp(rates[i]*dt))
                except ValueError: #Pois doesn't work if lambda too large. In this case, use normal approx
                    new_state[i] = np.random.normal(state[i]*np.exp(rates[i]*dt),state[i]*np.exp(rates[i]*dt))
                birth = new_state[i] - state[i]
                if birth>0:
                    nmutants[i] = np.random.binomial(birth, mutation_rate)
        
        # Treat the mutations. 
        if mutation_rate and nmutants.sum(): 
            
            # Create a list that contains the index of the phenotype of 
            # every individual that mutated during the last time interval.
            # i.e. if nmutant = [1,3,2], parent_list = [0,1,1,1,2,2].
            parent_list = list(chain(*[[i]*n for i,n in enumerate(nmutants)]))
            
            # List the empty phenotype slots, this is where we will put the mutants.
            mutants_list = np.arange(M)[state==0]
                        
            # If we have too many potential parents compared to the number of open slots 
            # for phenotype, we select them uniformely at random.
            # Note: this is quit an important restriction of our simulation !
            if len(parent_list) > len(mutants_list):
                parent_list = np.random.choice(parent_list, size=len(mutants_list),replace=False)
                
            # Go through the mutations and do the mutation. 
            for pos_parent, pos_mutant in zip(parent_list, mutants_list):
                phenotypes[pos_mutant] = np.clip(phenotypes[pos_parent] + np.random.normal(0,mutation_effect),umin,umax)
                new_state[pos_mutant] = 1
                new_state[pos_parent] -= 1
                
        # We copy the content of new_state in state. 
        state[:] = new_state[:]
        
        # We save once in a while. 
        if t%skip == 0:
            trajectory[:,t//skip] = state
            pheno_traj[:,t//skip] = phenotypes
            tlist[t//skip] = t*dt
    return trajectory, pheno_traj, tlist
