library(ggplot2) #for plotting


K = 10000
final_time = 1e6

data <- read.csv(paste('./data/K_',as.integer(K),'_time_',final_time,'.csv',sep=''))

#Just a precaution
data %>% 
  filter(p < 0.9) %>% #condition on non-extinction
  filter(p > 0.1) %>% #condition on non-extinction
  select(time,p,Ntot) -> data

#lineplot of timeseries
lineplot <-  ggplot(data=data,aes(x=time,y=p)) + geom_line(color='#ff0000')


#aesthetics
lineplot <- lineplot + theme_light() + xlab('Time') + ylab("Proportion of Type 1\nindividuals in the population")
lineplot <- lineplot + theme(panel.border = element_blank(), axis.line = element_line(colour = "black"), panel.grid.major = element_blank(), panel.grid.minor = element_blank())
lineplot <- lineplot + theme(axis.text = element_text(face = 'bold', color = 'black',size = 30))
lineplot <- lineplot + theme(axis.title = element_text(face = 'bold',color = 'black',size = 35))
lineplot <- lineplot + theme(legend.position = 'none') #remove legend
lineplot <- lineplot + theme(aspect.ratio = 1) #set aspect ratio
lineplot <- lineplot + theme(axis.ticks.length = unit(.15, "cm")) + theme(axis.ticks = element_line(color='black',linewidth=0.5))
lineplot <- lineplot + scale_y_continuous(expand = c(0, 0),limits = c(0,1),breaks=seq(0,1,by=0.1))

#add a horizontal line at y=0.5
lineplot <- lineplot + geom_hline(yintercept = 0.5,linetype='dashed',linewidth=1.2,alpha=0.5)

ggsave(paste('./plots/timeseries_K_',as.integer(K),'_time_',final_time,'.svg',sep=''),lineplot,width=12,height=12,dpi=600)


#density plots

dens <- ggplot(data=data,aes(x=p,y=after_stat(count)/sum(after_stat(count))))
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
#add a vertical line at x=0.5
dens <- dens + geom_vline(xintercept = 0.5,linetype='dashed',linewidth=1.2,alpha=0.5)
#dens #view the plot

#ggsave(paste('./plots/K_',as.integer(K),'_time_',final_time,'.svg',sep=''),dens,width=12,height=12,dpi=600)
