# Code used for simulations presented in my (Shikhara Bhat's) MS thesis.

<p align="justify">
This repository contains the scripts required for replicating the examples presented in Appendix D of my (Shikhara Bhat's) MS thesis, written as part of the BS-MS degree at the Indian Institute of Science Education and Research (IISER) Pune, India, in the year 2022-23. The thesis was conducted under the supervision of <a href='https://teelabiisc.wordpress.com/'>Prof. Vishwesha Guttal</a> and <a href='https://sites.google.com/view/rohinibalakrishnanlab/home'>Prof. Rohini Balakrishnan</a> at the Centre for Ecological Sciences in the Indian Institute of Science, Bengaluru. <a href='https://sites.google.com/a/acads.iiserpune.ac.in/sdlab/pbl-iiser-p'>Prof. Sutirth Dey</a> from IISER Pune acted as the internal expert for evaluating the thesis.
</br>
</br>
The 'stoch_logistic_eqn' folder contains the scripts, plots, and data used in section D.1. This is coded in R.</br>
</br>
The 'stoch_LV_competition' folder contains the scripts, plots, and data used in section D.3. This is coded in R.</br>
</br>
The 'stoch_quantitative_logistic_eqn' folder contains scripts for individual-based simulations of the evolution of a one-dimensional quantitative trait as a stochastic birth-death process using the Gillespie. The code in this folder is written in Python, and is meant to be run on a high-performance computer with SLURM installed. To run the simulation, just execute

```
sbatch run_model.SLURM 
```

on the HPC.

The primary Gillespie algorithm is a slightly modified version of Guilhelm Doulcier's code ([link](https://www.normalesup.org/~doulcier/teaching/adaptive_dynamics/dyad02.html))
</br>
I used a very toned down version of this code on my personal computer to produce figure D.6. This uses the ```logistic``` model from ```eco_models.py``` for the birth and death functionals, with the parameters ```sigma_K = 1.9, sigma_alpha = 0.7```.

