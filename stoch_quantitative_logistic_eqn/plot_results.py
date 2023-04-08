#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Shikhara Bhat
Email ID: shikharabhat@gmail.com
Date created: 2022-11-24 21:59:02
Date last modified: 2022-11-24 21:59:02
Purpose: [description]
'''
import matplotlib.pyplot as plt
import matplotlib.cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from itertools import chain

#make all text bold
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"

#change the font size
plt.rcParams.update({'font.size': 22})

def plot_density(traj, ptraj, tlist, ustep=180, ax=None,umin=None,umax=None,cmap='viridis',plot_dir=''):

    dist = np.zeros((ustep-1,traj.shape[1]+1))
    bin_min, bin_max = ptraj.min(), ptraj.max()
    bins = np.linspace(bin_min, bin_max, ustep)
    
    #set limits to max and min values of population if not provided
    if umin is None:
        umin = ptraj.min()
    
    if umax is None:
        umax = ptraj.max()

    for t, traits in enumerate(ptraj.transpose()):
        dist[:,t], _ = np.histogram(traits, weights=traj[:,t], bins=bins)

    if ax is None:
        fig,ax = plt.subplots(1,1,figsize=(20,5))
    dmask = dist
    dmask[dmask==0] = np.nan
    mp = ax.imshow(dmask,aspect='auto', 
                   extent=[tlist.min(),tlist.max(),bin_min, bin_max],
                   cmap=cmap,
                   origin='lower')
    ax.set(xlabel='Time',ylabel='Trait value',ylim=(umin,umax))
    cax = make_axes_locatable(ax).append_axes("right", size="1%", pad=0.2)
    ax.get_figure().colorbar(label='density', cax=cax, ax=ax, mappable=mp)
    plt.savefig(plot_dir+'.svg',dpi=200) #save to file
    plt.close()
    
def plot_stack(traj, ptraj, tlist, ax=None, lw=0.3, color_over=100):
    if ax is None:
        fig,ax = plt.subplots(1,1,figsize=(20,5))
    bin_min, bin_max = ptraj.min(), ptraj.max()
    transform = lambda x : (x - bin_min) / (bin_max - bin_min)
    df = np.cumsum(traj,axis=0)
    ax.fill_between(tlist, np.zeros_like(df[0]), df[-1], color='grey')
    for i, (y1, y2) in enumerate(zip(chain([np.zeros_like(df[0]),], df[:-1]), df)):
        bkpts = np.nonzero(ptraj[i,:-1] != ptraj[i,1:])[0]
        for t0,t1 in zip(chain([0,], bkpts), chain(bkpts, [ptraj.shape[1],])):
            t = (t0+t1)//2
            if t0-t1 and np.max(y2[t0:t1]-y1[t0:t1]) > color_over :
                ax.fill_between(tlist[t0:t1],  y1[t0:t1], y2[t0:t1],
                                color=matplotlib.cm.viridis(transform(ptraj[i,t])))
        ax.plot(tlist, y2, color='k', lw=lw)