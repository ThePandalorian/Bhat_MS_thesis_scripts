#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Shikhara Bhat
Email ID: shikharabhat@gmail.com
Date created: 2022-11-24 14:56:04
Date last modified: 2022-11-24 14:56:04
Purpose: List of ecological models to supply to BD_sim
'''
import numpy as np


def logistic(ulist,nlist,K0,sigma_K,sigma_alpha,beta=0):
    
    '''
    Frequency-dependent competition with Gaussian carrying capacity and Gaussian competition kernel
    sigma_K (non-negative float) is the std dev of the carrying capacity (centered at 0)
    sigma_alpha (non-negative float) is the std dev of the competition kernel.
    beta (non-negative float) is the degree of asymmetry of the competition.
    beta = 0 corresponds to symmetric competition.
    
    Deterministic AD predicts branching iff sigma_alpha < sigma_K

    This model is from section 3.2 of Doebeli 2011 ('Adaptive Diversification')
    '''
    
    dens = nlist/K0
    
    alpha = lambda u,v: np.exp(-((u-v+(sigma_alpha**2)*beta)**2)/(2*(sigma_alpha**2)))
    K = lambda u: np.exp(-(u**2)/(2*(sigma_K**2)))
    
    death = lambda u: (np.sum([alpha(u,v)*phi for v,phi in zip(ulist,dens)]))/(K(u))
    
    return (np.array([(1 - death(u)) for u in ulist]))
    #return (np.array([((nlist[i])/(K0+nlist[i])) for i in range(len(nlist))]))


def claessen2007(ulist, nlist, a1, a2, b1,b2, d1, d2, K1, K2,mu,K0):
    
    '''
    Implements the model presented in Claessen 2007.
    http://www.evolutionary-ecology.com/abstracts/v09/2073.html

    This is a model for resource competition in fish. K0 is V in their notation.
    
    '''
    density = nlist / K0
    A1 = lambda u: a1 + u*b1
    A2 = lambda u: a2 + u*b2 
    F1 = (d1*K1)/(np.sum([A1(u)*u*N for u,N in zip(ulist,density)]) + d1)
    F2 = (d2*K2)/(np.sum([A2(u)*(1-u)*N for u,N in zip(ulist,density)])  + d2)
    bet = lambda u: (F1 * A1(u) * u) + (F2 * A2(u) * (1-u)) - mu
    return np.array([bet(u) for u in ulist])


def debarre_otto_2016(ulist,nlist,B1,B2,C1,C2,d,K0):

    '''
    Implements the model presented in Debarre and Otto 2016
    https://www.sciencedirect.com/science/article/pii/S0040580915001240?via%3Dihub

    This is a model for a public goods game. K0 is B0 in their notation
    '''
    
    denslist = nlist/K0
    
    ubar = np.mean([u*n for u,n in zip(ulist,denslist)]) #weighted mean trait value
    v = np.var([u*n for u,n in zip(ulist,denslist)]) #variance of traits
    F = lambda u: K0*(1+B1*(u+ubar)+B2*((u+ubar)**2 + v) - C1*u - C2*(u**2)) #fecundity function
    
    return (np.array([(F(u)-d) for u in ulist]))
    
