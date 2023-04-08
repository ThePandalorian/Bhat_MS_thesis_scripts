############################
# Conduct Gillespie simulations of an evol matrix game in finite pops
# To illustrate noise-induced selection
# Written by Shikhara Bhat
# IISER Pune, India
# Date: Tue Apr 04 11:34:09 2023
###########################

library(GillespieSSA2) #for stochastic simulations
library(dplyr) #for manipulating dataframes
library(ggplot2) #for plotting


model_params <- c(
  
  
  #Intrinsic rates  
  b1 = 1, #intrinsic per capita birth rate of type 1 inds
  b2 = 1, #intrinsic per capita birth rate of type 2 inds
  delta11 = 1, #per capita death rate due to intraspecific competition of type 1 inds
  delta22 = 1, #per capita death rate due to intraspecific competition in type 2 inds
  
  #Interaction effects on birth rates            
  beta12 = -1, #per capita effect of type 2 on birth rate of type 1
  beta21 = 0,  #per capita effect of type 1 on birth rate of type 2
  
  #Interaction effects on death rates              
  delta12 = 0, #per capita effect of type 2 inds on death rate of type 1
  delta21 = 1, #per capita effect of type 1 inds on death rate of type 2
  
  #mutation rate
  mu = 0.05, #mutation rate (assumed symmetric) from one type to the other
  
  #Carrying capacity/density dependence factor  
  K = 1000 #System-size parameter
)


#Define total birth and death rates
reactions <- list(
  
  #                     rate                                   effect
  
  
  #births
  #       intrinsic     interactions       mutation
  reaction("b1*N1   +   beta12*N2*N1/K  +   mu*N2",          c(N1 = +1)),
  reaction("b2*N2   +   beta21*N1*N2/K  +   mu*N2",          c(N2 = +1)),
  
  #deaths
  #            intrinsic            interactions        
  reaction("delta11*N1*N1/K   +   delta12*N2*N1/K",          c(N1 = -1)),
  reaction("delta22*N2*N2/K   +   delta21*N1*N2/K",          c(N2 = -1))
)

##########################
#In terms of predictions, we have:
#classical selection (increased fitness): neutral
#noise-induced selection (reduced turnover): species 1 favored over species 2
########################

#Initial conditions
#Start with equal no. of inds of each type
initial_state <- c(
  N1 = round(as.integer(model_params['K'])/2),
  N2 = round(as.integer(model_params['K'])/2)
)


final_time <- 1e4 #time at which the Gillespie simulation stops
runs <- 100        #no. of independent realizations to simulate


#Run the SSA

set.seed(2878) #for reproducibility

start_time = Sys.time() #for timing how long running the code takes


#Time complexity: This should scale linearly with time but exponentially with K :(
sim_run <- ssa(
  initial_state = initial_state,
  reactions = reactions,
  params = model_params,
  final_time = final_time,
  method = ssa_exact(),
  census_interval = 10, #how often to store data. 0 means store everything.
  sim_name = 'Finite pop matrix game'
)

sim_data <- as.data.frame(cbind(sim_run[['time']], sim_run[['state']]))
rm(sim_run)#to save memory

for (i in 1:runs-1){
  sim_run <- ssa(
    initial_state = initial_state,
    reactions = reactions,
    params = model_params,
    final_time = final_time,
    method = ssa_exact(),
    census_interval = 10, #how often to store data. 0 means store everything.
    sim_name = 'Finite pop matrix game'
  )
  
  sim_data <- rbind(sim_data,as.data.frame(cbind(sim_run[['time']], sim_run[['state']])))
  
  rm(sim_run)#to save memory
}

running_time = Sys.time() - start_time
running_time


#Collate to dataframe

colnames(sim_data) <- c('time','N1','N2')

#move from (N1,N2) space to (p, N1+N2) space
sim_data %>% 
  mutate(Ntot = N1+N2) %>% #total population size
  mutate(p = N1/(Ntot)) %>% #proportion of type 1 individuals
  filter(p < 0.9) %>% #condition on non-extinction
  filter(p > 0.1) %>% #condition on non-extinction
  select(time,p,Ntot) -> transformed_data

#save to file
write.csv(transformed_data,paste('./data/K_',as.integer(model_params['K']),'_time_',final_time,'_num_runs_',runs,'.csv',sep=''),row.names=FALSE)

###########################
#Plotting
#create the plot

dens <- ggplot(data=transformed_data,aes(x=p,y=after_stat(count)/sum(after_stat(count))))
dens <- dens + geom_density(color='red',fill='#ff00006d',alpha=0.2,bounds=c(0,1))


#aesthetics
dens <- dens + theme_light() + xlab('Proportion of Type 1 individuals') + ylab("Probability Density")
dens <- dens + theme(panel.border = element_blank(), axis.line = element_line(colour = "black"), panel.grid.major = element_blank(), panel.grid.minor = element_blank())
dens <- dens + theme(axis.text = element_text(face = 'bold', color = 'black',size = 30))
dens <- dens + theme(axis.title = element_text(face = 'bold',color = 'black',size = 35))
dens <- dens + theme(legend.position = 'none') #remove legend
dens <- dens + theme(aspect.ratio = 1) #set aspect ratio
dens <- dens + theme(axis.ticks.length = unit(.15, "cm")) + theme(axis.ticks = element_line(color='black',linewidth=0.5))
dens <- dens + scale_y_continuous(expand = c(0, 0)) #this removes the gap between plot and x axis
dens <- dens + scale_x_continuous(limits = c(0,1),breaks=seq(0,1,by=0.1))
dens <- dens + geom_vline(xintercept = 0.5,linetype='dashed',linewidth=1.2,alpha=0.5) #add a vertical line at x=0.5
#dens #view the plot

ggsave(paste('./plots/K_',as.integer(model_params['K']),'_time_',final_time,'_num_runs_',runs,'.svg',sep=''),dens,width=12,height=12,dpi=600)
