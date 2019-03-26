##################################################################################################################
#This python code takes in information about what data to use and what variables to plot and what kind of plots  #
#the user wants to plot. It then uses other python modules to perform the needed actions                         #
#														 #
#			Written by Eirikur Orn Johannesson spring 2019						 #
#														 #
##################################################################################################################
import imp
import readmodel
import lineplot
import contourplot
import scatterplot
#from scipy.stats import norm
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from collections import defaultdict
imp.reload(readmodel)
imp.reload(lineplot)
imp.reload(contourplot)
imp.reload(scatterplot)


#Choosing model and observation site, timeframe and variable

######### Variables used to read data to be analysed #########
modeldir1 = 'ifs_sodankyla/'		#Directory for model data
modeldir2 = 'arpege_sodankyla/'		#Directory for model data
obsdir = 'sodankyla_obs/'		#Directory to observations
model1 = 'IFS-ECMWF'			#What model is in use
model2 = 'ARPEGE'			#What model is in use
site = 'sodankyla'			#Observational site in use
no = 1					#Number of models used in analyze

################# Variables used for plottint ################
outdir = 'test'			#Directory to save plots in
var1 = 'ta'				#Shortname for variable from model 1 to plot
var2 = 't'				#Shortname for variable from model 2 to plot
obsvar = 'ta'				#Shortname for variable from observations to plot
obsvar2 = 'Tforest'
period = 3				#Choose what time period of forcast should be use for the analise. 1=First 12 hours of forecast, 2=First 24 hours of forecast made at midnight, 3=First 24 hours of forecast made at noon, 4=Starts 12 hours after beginning of forecast and ends after 24 hours
#start = 1				#How many 12 hour periods into each forecast to use in analyze
#end = 2					#After how many 12 hour periods into each forecast to stop
startdate = '2018-02-01'		#Start date for plotting
enddate = '2018-03-31'			#End date for plotting
shortsdate = '2018-02-10'
shortedate = '2018-02-18'
model1_lvl = 137			#1 is the highest level and 137 is the lowest
model2_lvl = 105			#1 is the highest level and 105 is the lowest
obs_lvl = 2				#1 is the lowest level and 5 is the highest
filtervar1 = 'N'
filter1 = 3
filtervar2 = 'WS'
filter2 = 2
filterby = 'obs'
no_filters = 2
whole_period = True
forecast = 3

############### Calling plotting functions, comment out the plots that are not to be made #############

data1,data2,obs,wind_vert,winddir_vert,temp_vert,dew_vert,names1,names2,dummy1,dummy2 = readmodel.readin(modeldir1,modeldir2,obsdir,site,startdate,enddate,model1,model2,period,no)

print 'Finished reading in data'

#for i in range(329787,len(temp_vert),4):
#	temp_vert[i,8] = float(temp_vert[i,8])


#day = str(data1[35].time.dt.day[0].values)
#month = str(data1[35].time.dt.month[0].values)
#year = str(data1[35].time.dt.year[0].values)
#if len(day) == 1:
#	day = '0'+day
#if len(month) == 1:
#	month = '0'+month
#days = year+month+day

#print temp_vert.shape
#obs_plot = temp_vert[temp_vert.DATE == days]
#print obs_plot.shape
#obs_plot = obs_plot[obs_plot.TIME == '00']
#print obs_plot.shape
#obs_plot = obs_plot[obs_plot.ALTITUDE.values < 2100]
#print obs_plot.shape

#print obs_plot.ALTITUDE



#plt.plot(obs_plot.DATA_VALUE+273,obs_plot.ALTITUDE)
#plt.show()

#exit()



#contourplot.plot(model1,model2,site,var1,var2,obsvar,obsvar2,data1,data2,data4,obs,names1,names2,model1_lvl,model2_lvl,obs_lvl,outdir,period,no,dummy,filtervar1,filter1,filtervar2,filter2,filterby,no_filters)

lineplot.plot(model1,model2,site,var1,var2,obsvar,obsvar2,data1,data2,obs,wind_vert,temp_vert,dew_vert,names1,names2,model1_lvl,model2_lvl,obs_lvl,outdir,period,no,dummy1,dummy2,filtervar1,filter1,filtervar2,filter2,filterby,no_filters,whole_period,startdate,enddate,shortsdate,shortedate,forecast)

#scatterplot.plot(model1,model2,site,var1,var2,obsvar,data1,data2,obs,names1,names2,model1_lvl,model2_lvl,obs_lvl,outdir,period,no,dummy1,dummy2,filtervar1,filtervar2,filter1,filter2,filterby,no_filters)
