#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Shikhara Bhat
Email ID: shikharabhat@gmail.com
Date created: 2022-11-25 20:13:07
Date last modified: 2022-11-25 20:13:07
Purpose: Generate K values for the array job
'''
import numpy as np

with open("/scratch/shikharabhat/BD_params/K.txt", 'w') as fil:
            for K in np.arange(500,11500,500):
                fil.write(str(K)+'\n')