############################
# Create animations comparing simulations of an evol matrix game in finite pops
# Written by Shikhara Bhat
# IISER Pune, India
# Date: Sat Apr 01 20:37:24 2023
###########################

library(GillespieSSA2) #for stochastic simulations
library(dplyr) #for manipulating dataframes
library(reshape2) #for changing dataframes from long to wide
library(ggplot2) #for plotting
library(gganimate) #for animating ggplots


model_params <- c(
  
            
              #Intrinsic rates  
              b1 = 1, #intrinsic per capita birth rate of type 1 inds
              b2 = 1, #intrinsic per capita birth rate of type 2 inds
              delta11 = 1, #per capita death rate due to intraspecific competition of type 1 inds
              delta22 = 1, #per capita death rate due to intraspecific competition in type 2 inds

              #Interaction effects on birth rates            
              beta12 = -1, #per capita effect of type 2 on birth rate of type 1
              beta21 = -1,  #per capita effect of type 1 on birth rate of type 2

              #Interaction effects on death rates              
              delta12 = 0, #per capita effect of type 2 inds on death rate of type 1
              delta21 = 0, #per capita effect of type 1 inds on death rate of type 2
            
              #mutation rate
              mu = 0.05, #mutation rate (assumed symmetric) from one type to the other
          
              #Carrying capacity/density dependence factor  
              K = 600 #System-size parameter
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

########################

#Initial conditions
#Start with equal no. of inds of each type
initial_state <- c(
  N1 = 200,
  N2 = 200
)


final_time <- 5000

#Run the SSA

set.seed(2878) #for reproducibility

start_time = Sys.time() #for timing how long running the code takes

sim_run <- ssa(
  initial_state = initial_state,
  reactions = reactions,
  params = model_params,
  final_time = final_time,
  method = ssa_exact(),
  census_interval = 10, #how often to store data. 0 means store everything.
  sim_name = 'Finite pop matrix game'
)

running_time = Sys.time() - start_time
running_time


#Collate to dataframe
sim_data <- as.data.frame(cbind(sim_run[['time']], sim_run[['state']]))
colnames(sim_data) <- c('time','N1','N2')

#condition on non-extinction
sim_data %>% 
  mutate(Ntot = N1+N2) %>% #total population size
  mutate(p = N1/(Ntot)) %>% #proportion of type 1 individuals
  filter(p < 0.9) %>% #condition on non-extinction
  filter(p > 0.1) %>% 
  select(time,N1,N2)-> transformed_data

plot_data <- melt(transformed_data, variable.name = 'state', id.vars = c('time'))
colnames(plot_data) = c('time','state','N')

###########################
#Plotting


#lineplot of timeseries
lineplot <-  ggplot(data=plot_data,aes(x=time,y=N,group=state)) + geom_line(aes(color=state))
lineplot <- lineplot + scale_color_manual(values =  c('#ff0000','#0000ff'))

#aesthetics
lineplot <- lineplot + theme_light() + xlab('Time') + ylab("Proportion of Type 1\nindividuals in the population")
lineplot <- lineplot + theme(panel.border = element_blank(), axis.line = element_line(colour = "black"), panel.grid.major = element_blank(), panel.grid.minor = element_blank())
lineplot <- lineplot + theme(axis.text = element_text(face = 'bold', color = 'black',size = 30))
lineplot <- lineplot + theme(axis.title = element_text(face = 'bold',color = 'black',size = 35))
lineplot <- lineplot + theme(legend.position = 'none') #remove legend
lineplot <- lineplot + theme(aspect.ratio = 1) #set aspect ratio
lineplot <- lineplot + theme(axis.ticks.length = unit(.15, "cm")) + theme(axis.ticks = element_line(color='black',linewidth=0.5))
lineplot #view the plot

#ggsave(paste('./plots/K_',as.integer(model_params['K']),'_time_',final_time,'.svg',sep=''),dens,width=12,height=12,dpi=600)

