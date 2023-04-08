#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Shikhara Bhat
Email ID: shikharabhat@gmail.com
Date created: 2022-11-24 14:57:21
Date last modified: 2022-11-24 14:57:21
Purpose: Parameter values for the models in eco_models.py
The system size parameter is NOT PROVIDED. You need to augment these
static parameters with the system size parameter. For example,

logistic_params = {'K0':10000, **logistic_branching}
'''

#for logistic eqn
logistic_branching = {'sigma_K':1.9,'sigma_alpha':0.7,'beta':0}
logistic_branching_asymm = {'sigma_K':1.9,'sigma_alpha':0.7,'beta':0.5}
logistic_no_branching = {'sigma_K':0.7,'sigma_alpha':1.9,'beta':0}

#for claessen 2007. V controls population size
claessen_p_common = {"b2":0, 'd1':1,'d2':1,'K1':1,'K2':1,'mu':0.1}
claessen_p_neutral = {"a1": 1, "b1": 0, "a2":1, **claessen_p_common}
claessen_p_strong = {"a1": 1, "b1": 1, "a2":2, **claessen_p_common}
claessen_p_weak = {"a1": 2, "b1": -1, "a2":1, **claessen_p_common}

#for debarre and otto 2016. B0 controls population size
DO2016_params = {'B1':7,'B2':-1.5,'C1':4.6,'C2':-1,'d':1} #from figure 1 of Debarre and Otto 2016
