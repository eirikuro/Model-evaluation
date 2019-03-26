from scipy.stats import norm, gaussian_kde
import numpy as np
import pandas as pd
import xarray as xr
import os
import matplotlib.pyplot as plt
#import scipy.stats
from pandas.plotting import register_matplotlib_converters
from collections import OrderedDict
import datetime as dt

def plot(model1,model2,site,var1,var2,obsvar,obsvar2,data1,data2,obs,wind_vert,temp_vert,dew_vert,names1,names2,model1_lvl,model2_lvl,obs_lvl,outdir,period,no,dummy1,dummy2,filtervar1,filter1,filtervar2,filter2,filterby,no_filters,whole_period,startdate,enddate,shortsdate,shortedate,forecast):

	register_matplotlib_converters()

	if outdir[-1] != '/':
		outdir = outdir + '/'

	if not os.path.isdir(outdir):
		os.makedirs(outdir)

#	names1 = np.linspace(0,1,67)

#	dummy1 = 50
#	print dummy1
#	print len(names1)
#	print len(data1)

#	print data1[dummy1]['time'][0]

#	print data1[67]['time'][0]

#	exit()

	# Creating dictionaries for plotting data on one level
	plotvar1 = {}
	plotvar2 = {}
	plotvar3 = {}
	plotvar4 = {}

	# Choosing one level from the model data from model 1
	if period == 5:
		for n in range(dummy1,len(names1)):
#			if len(data1[n][var1].shape) == 3:
#				plotvar1[n] = data1[n][var1][:,0,0]
#			else:
#				plotvar1[n] = data1[n][var1][:,0,0,model1_lvl-1]
			if data1[n].time.dt.hour[0] == 0:
				if len(data1[n][var1].shape) == 3:
					plotvar1[n] = data1[n][var1][:,0,0]
				else:
					plotvar1[n] = data1[n][var1][:,0,0,model1_lvl-1]
			if data1[n].time.dt.hour[0] == 12:
				if len(data1[n][var1].shape) == 3:
					plotvar3[n] = data1[n][var1][:,0,0]
				else:
					plotvar3[n] = data1[n][var1][:,0,0,model1_lvl-1]
#			if len(data4[n][var1].shape) == 3:
#				plotvar4[n] = data4[n][var1][:,0,0]
#			else:
#				plotvar4[n] = data4[n][var1][:,0,0,model1_lvl-1]
	else:
		for n in range(dummy1,len(names1)):
			if len(data1[n][var1].shape) == 3:
				plotvar1[n] = data1[n][var1][:,0,0]
			else:
				plotvar1[n] = data1[n][var1][:,0,0,model1_lvl-1]

	# If model 2 is in use go through this loop
	if no == 2 or no == 3:
		if period == 5:
			for n in range(dummy2,len(names2)):
				if data2[n].time.dt.hour[0] == 0:
					if len(data2[n][var2].shape) == 1:
						plotvar2[n] = data2[n][var2][:]
					else:
						plotvar2[n] = data2[n][var2][:,model2_lvl-1]
				if data2[n].time.dt.hour[0] == 12:
					if len(data2[n][var2].shape) == 1:
						plotvar4[n] = data2[n][var2][:]
					else:
						plotvar4[n] = data2[n][var2][:,model2_lvl-1]
		else:
			for n in range(dummy2,len(names2)):
				if len(data2[n][var2].shape) == 1:
					plotvar2[n] = data2[n][var2][:]
				else:
					plotvar2[n] = data2[n][var2][:,model2_lvl-1]



	# Choosing one level from observations data

	if len(obs[obsvar].shape) == 1:
		obs1 = obs[obsvar][:]
	else:
		obs1 = obs[obsvar][obs_lvl-1,:]

	if len(obs[obsvar2].shape) == 1:
		obs2 = obs[obsvar2][:]
	else:
		obs2 = obs[obsvar2][obs_lvl-1,:]


	if var1 == 'tnt':
		for n in range(dummy1,len(names1)):
			plotvar1[n] = plotvar1[n]*3600
			plotvar1[n] = plotvar1[n][1:]
#			data1[n]['time'] = data1[n]['time'][1:]


	# Plotting lineplots
	if period == 5:	#Plotting the difference between model and obs
		if no == 1 or no == 3:
			for n in range(dummy1,len(names1)):
				if forecast == 1 or forecast == 3:
					if data1[n].time.dt.hour[0] == 00:
						plotvar1[n] = plotvar1[n][7::8]
						plt.plot(data1[n]['time'][7::8],plotvar1[n][:]-obs1[:],linewidth=1,label=model1+' - starting at '+str(data1[n].time.dt.hour[0].values), color='black')
#					plt.plot(obs['time'][1+(n-dummy)*12:(n-dummy)*12+24],plotvar2[n][:]-obs1[1+(n-dummy)*12:(n-dummy)*12+24],linewidth=0.4,label='IFS - starting at 00', color='blue')

				if forecast == 2 or forecast == 3:
					if data1[n].time.dt.hour[0] == 12:
						plotvar3[n] = plotvar3[n][7::8]
						plt.plot(data1[n]['time'][7::8],plotvar3[n][:]-obs1[:],linewidth=1,label=model1+' - starting at '+str(data1[n].time.dt.hour[0].values), color='red')
#					plt.plot(obs['time'][1+(n-dummy)*12:(n-dummy)*12+24],plotvar3[n][:]-obs1[1+(n-dummy)*12:(n-dummy)*12+24],ls='--',linewidth=0.4,label='IFS - starting at 12', color='green')

		if no == 2 or no == 3:
			for n in range(dummy2,len(names2)):
				if forecast == 1 or forecast == 3:
					if data2[n].time.dt.hour[0] == 00:
						plt.plot(data2[n]['time'][:],plotvar2[n][:]-obs1[:],linewidth=1,label=model2+' - starting at '+str(data2[n].time.dt.hour[0].values), color='brown')
				if forecast == 2 or forecast == 3:
					if data2[n].time.dt.hour[0] == 12:
						plt.plot(data2[n]['time'][:],plotvar4[n][:]-obs1[:],linewidth=1,label=model2+' - starting at '+str(data2[n].time.dt.hour[0].values), color='green')



		if whole_period:
			plt.xlim([startdate,enddate])
		else:
			plt.xlim([shortsdate,shortedate])
		plt.ylim([-14,14])
		plt.xticks(rotation=10,size=8)
		plt.yticks(size=8)
		plt.xlabel('Time')
		plt.ylabel(data1[dummy1][var1].units)
		plt.axhline(y=0, lw='0.8', ls='--',color='gray')
		plt.axhline(y=5, lw='0.8', ls='--',color='gray')
		plt.axhline(y=-5, lw='0.8', ls='--',color='gray')
		plt.axhline(y=10, lw='0.8', ls='--',color='gray')
		plt.axhline(y=-10, lw='0.8', ls='--',color='gray')
#		plt.axhline(y=(np.std(obs['Topen'][:]-obs['Tforest'][:])+(0.176-0.0028*273)), lw='0.8', ls='--',color='gray')
#		plt.axhline(y=(-np.std(obs['Topen'][:]-obs['Tforest'][:])-(0.176-0.0028*273)), lw='0.8', ls='--',color='gray')
		if model1 == 'IFS-ECMWF':
			plt.title('Difference between model and obs for '+data1[dummy1][var1].long_name+' over time')
		else:
			plt.title('Difference between model and obs for '+data2[dummy2][var1].longname+' over time')
		handles, labels = plt.gca().get_legend_handles_labels()
		by_label = OrderedDict(zip(labels, handles))
		plt.legend(by_label.values(), by_label.keys())
		if no == 3:
			plt.savefig(outdir+'line_diff_'+model1.lower()+'_'+model2.lower()+'_'+var1+'.pdf')
		elif no == 1:
			plt.savefig(outdir+'line_diff_'+model1.lower()+'_'+var1+'.pdf')
		elif no == 2:
			plt.savefig(outdir+'line_diff_'+model2.lower()+'_'+var2+'.pdf')

		plt.clf()
	else:	#Plotting basic line plots for both model and obs
		for n in range(dummy1,len(names1)):
			if period == 1:
#				if data1[n]['ta'][0,0,0,136]-obs['ta'][1,(n-dummy)*12] > 2:
				plt.plot(data1[n]['time'][:],plotvar1[n][:],linewidth=0.3,label=model1, color='black')
#				else:
#					plt.plot(data1[n]['time'][0],np.mean(plotvar1[n][1:]),'r*') #,linewidth=0.3,label='IFS', color='black')
			elif period == 2:
#				if n % 2 == 0:
				if data1[n].time.dt.hour[0] == 00:
					plt.plot(data1[n]['time'][:],plotvar1[n][:],linewidth=0.3,label=model1+' - '+str(data1[n].time.dt.hour[0].values), color='black')
#					ax2.plot(data1[n]['time'][start*96:end*97],data1[n]['clt'][start*96:end*97,0,0],label='IFS',linestyle=':', color='green')
#			elif period == 3:
#				if n % 2 == 1:
				if data1[n].time.dt.hour[0] == 12:
					plt.plot(data1[n]['time'][:],plotvar1[n][:],linewidth=0.3,label=model1+' - '+str(data1[n].time.dt.hour[0].values), color='red')
#					plt.plot(data1[n]['time'][0],np.mean(plotvar1[n][1:]),'r*') #,linewidth=0.3,label='IFS', color='black')

			elif period == 4:
				plt.plot(data1[n]['time'][:],plotvar1[n][:],linewidth=0.3,label=model1, color='black')
		if not var1 == 'tnt':
			plt.plot(obs['time'],obs1[:],label='Sodankyla',linewidth=0.3,linestyle='--', color='green')
#	plt.plot(obs['time'],obs[obsvar2][:],label='Sodankyla',linestyle='--', color='green')
#	ax2.plot(obs['time'],obs['N'][:]/8,label='Sodankyla',linestyle=':', color='green')
#	plt.legend()


		if whole_period:
			plt.xlim([startdate,enddate])
		else:
			plt.xlim([shortsdate,shortedate])
		plt.xticks(rotation=10,size=8)
		plt.yticks(size=8)
		plt.xlabel('Time')
		if var1 == 'tnt':
			plt.ylabel(r'$K/hour$')
		else:
			plt.ylabel(data1[dummy1][var1].units)

		plt.title(data1[dummy1][var1].long_name+' over time')
#		plt.axhline(y=0,lw='0.3')
		handles, labels = plt.gca().get_legend_handles_labels()
		by_label = OrderedDict(zip(labels, handles))
		plt.legend(by_label.values(), by_label.keys())
#		plt.legend()
		if no == 3:
			plt.savefig(outdir+'line_diff_'+model1.lower()+'_'+model2.lower()+'_'+var1+'_'+str(period)+'.pdf')
		elif no == 1:
			plt.savefig(outdir+'line_diff_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf')
		elif no == 2:
			plt.savefig(outdir+'line_diff_'+model2.lower()+'_'+var2+'_'+str(period)+'.pdf')

		plt.clf()



	print 'Lineplot for '+model1+' finished'

	plt.clf()


######### This section is a plot that was only plotted once and does not have to be plotted again ###############

#	plt.plot(obs['time'],obs['Topen'][:]-273, label='open',linewidth=0.5,color='black')
#	plt.plot(obs['time'],obs['Tforest'][:]-273, label='forest',linestyle='--',linewidth=0.5,color='green')
#	plt.savefig(outdir+'open+forest.pdf')

#	plt.clf()

#	plt.plot(obs['time'],obs['Topen'][:]-obs['Tforest'][:],label='open-forest', linewidth=0.3,color='blue')
#	plt.plot(obs['time'],(obs['Topen'][:]-obs['Tforest'][:])-np.std(obs['Topen'][:]-obs['Tforest'][:]),label='std',ls='--', linewidth=0.3,color='green')
#	plt.legend()
#	plt.xlabel(r'$K$')
#	plt.ylabel('Time')
#	plt.title('2m Temperature in Sodankyla as well as the difference')
#	plt.savefig(outdir+'open-forest.pdf')

#	plt.clf()


	'''
#	Plotting pdf for LWN

#	x = np.arange(150,500,0.24717514124)#

	bw_values = [None, 0.1] #, 0.01]

#	kde = [scipy.stats.gaussian_kde(obs['rlds'][:]-obs['rlus'][:],bw_method=bw) for bw in bw_values]#

	kde = [gaussian_kde(obs['rlds'][:]-obs['rlus'][:],bw_method=bw) for bw in bw_values]
	plt.hist(obs['rlds'][:]-obs['rlus'][:], 10, density=1, facecolor='green', alpha=0.5)
	t_range = np.linspace(-100,30,800)
	for i, bw in enumerate(bw_values):
	    plt.plot(t_range,kde[i](t_range),lw=2, label='bw = '+str(bw))
	plt.legend()

#	plt.plot(norm.pdf(obs['rlds'][:]-obs['rlus'][:]))#
#	plt.show()#

	plt.savefig(outdir+'pdf-test.pdf')
	plt.clf()

	'''
################################################################################################################


#	if no == 2:
#		fig, ax3 = plt.subplots()
#		ax4 = ax3.twinx()

#		for n in range(len(names2)):
#			ax3.plot(data2[n]['time'][start*12:end*13],data2[n][var2][start*12:end*13],label='ARPEGE', color='black')
#			ax4.plot(data2[n]['time'][start*12:end*13],data2[n]['cc'][start*12:end*13],label='ARPEGE',linestyle=':', color='green')

#		if var == 'tas':
#			plt.plot(obs['time'],obs['ta'], color='red')
#		else:

#		ax3.plot(obs['time'],obs[obsvar][:],label='Sodankyla',linestyle='--', color='blue')
#		ax3.plot(obs['time'],obs['N'][:]/8,label='Sodankyla',linestyle=':', color='green')
#		ax4.set_ylim([0,1])

#		plt.legend()
#		plt.savefig(outdir+model2+'_'+var2+'.pdf')

#		plt.clf()

	fig, ax = plt.subplots()
	ax.set_color_cycle(['red','red','blue', 'blue', 'green','green','black', 'black', 'yellow','yellow','brown','brown','orange','orange','purple','purple','pink','pink'])


	if len(data1[n][var1].shape) == 4:
		if period == 1 or period == 2 or period == 3 or period == 4:
			for n in range(dummy1,len(names1)):
				if no_filters == 1:
					if period == 1:
#						if data1[n][filtervar][0,0,0] < filter:
						if obs[filtervar1][(n-dummy1)*12] < filter1:
							plt.plot(data1[n][var1][1,0,0,:],data1[n]['zg'][1,0,0,:]-data1[n]['orog'][1,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#							plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],label='obs',c='black')
					elif period == 2:
						if n % 2 == 0:
#							if data1[n][filtervar][0,0,0] < filter:
							if obs[filtervar1][(n-dummy1)*12] < filter1:
								plt.plot(data1[n][var1][1,0,0,:],data1[n]['zg'][1,0,0,:]-data1[n]['orog'][1,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#								plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],label='obs',c='black')
					elif period == 3:
						if n % 2 == 1:
#							if data1[n][filtervar][0,0,0] < filter:
							if obs[filtervar1][(n-dummy1)*12] < filter1:
								plt.plot(data1[n][var1][1,0,0,:],data1[n]['zg'][1,0,0,:]-data1[n]['orog'][1,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#								plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],c='black',label='obs')
#							plt.plot(data1[n][var1][0,0,0,:],data1[n]['zg'][0,0,0,:],linewidth=0.3,label='IFS')
					elif period == 4:
#							if data1[n][filtervar][0,0,0] < filter:
							if obs[filtervar1][(n-dummy1)*12] < filter1:
								plt.plot(data1[n][var1][0,0,0,:],data1[n]['zg'][0,0,0,:]-data1[n]['orog'][0,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
				else:
					if period == 1:
						if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
							plt.plot(data1[n][var1][1,0,0,:]*3600,data1[n]['zg'][1,0,0,:]-data1[n]['orog'][0,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#							if data1[n].time.dt.hour[0] == 12:
							day = str(data1[n].time.dt.day[0].values)
							month = str(data1[n].time.dt.month[0].values)
							year = str(data1[n].time.dt.year[0].values)
							if len(day) == 1:
								day = '0'+day
							if len(month) == 1:
								month = '0'+month
							days = year+month+day

							obs_plot = temp_vert[temp_vert.DATE == days]
							obs_plot = obs_plot[obs_plot.PRESSURE > '850']

							plt.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE)

#							plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],label='obs',c='black')

#						plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='o',color='red')
#					elif obs[filtervar1][(n-dummy)*12] < filter1 and obs[filtervar2][(n-dummy)*12] > filter2:
#						plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=8,marker='o',color='red')
#					elif obs[filtervar1][(n-dummy)*12] > filter1 and obs[filtervar2][(n-dummy)*12] < filter2:
#						plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='o',color='green')
#					else:
#						plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=8,marker='o',color='green')
					elif period == 2:
						if data1[n].time.dt.hour[0] == 00:
#						if n % 2 == 0:
							if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
								if data1[n].time.dt.month[0] == 2:
									plt.plot(data1[n][var1][0,0,0,:],data1[n]['zg'][0,0,0,:]-data1[n]['orog'][0,0,0],linewidth=0.8,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#								plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],c='black')

									day = str(data1[n].time.dt.day[0].values)
									month = str(data1[n].time.dt.month[0].values)
									year = str(data1[n].time.dt.year[0].values)
									if len(day) == 1:
										day = '0'+day
									if len(month) == 1:
										month = '0'+month
									days = year+month+day

									obs_plot = temp_vert[temp_vert.DATE == days]
									obs_plot = obs_plot[obs_plot.TIME == '00']
									obs_plot = obs_plot[obs_plot.ALTITUDE < 2300]
#								print n
									plt.plot(obs_plot.DATA_VALUE+273,obs_plot.ALTITUDE-180,lw=0.8,ls='--',label='obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))


#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='o',color='red')
#						elif obs[filtervar1][(n-dummy)*12] < filter1 and obs[filtervar2][(n-dummy)*12] > filter2:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='*',color='red')
#						elif obs[filtervar1][(n-dummy)*12] > filter1 and obs[filtervar2][(n-dummy)*12] < filter2:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='o',color='green')
#						else:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='*',color='green')
					elif period == 3:
						if data1[n].time.dt.hour[0] == 12:
#						if n % 2 == 1:
							if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
								if data1[n].time.dt.month[0] == 2:
									plt.plot(data1[n][var1][0,0,0,:],data1[n]['zg'][0,0,0,:]-data1[n]['orog'][0,0,0],linewidth=0.8,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#								plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],c='black')

									day = str(data1[n].time.dt.day[0].values)
									month = str(data1[n].time.dt.month[0].values)
									year = str(data1[n].time.dt.year[0].values)
									if len(day) == 1:
										day = '0'+day
									if len(month) == 1:
										month = '0'+month
									days = year+month+day

									obs_plot = temp_vert[temp_vert.DATE == days]
									obs_plot = obs_plot[obs_plot.TIME == '12']
									obs_plot = obs_plot[obs_plot.ALTITUDE < 2300]

									plt.plot(obs_plot.DATA_VALUE+273,obs_plot.ALTITUDE-180,lw=0.8,ls='--',label='obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

#								plt.plot(obs_plot.DATA_VALUE+273,obs_plot.ALTITUDE-180,lw='0.3',color='black',label='obs')

#								plt.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-180, color='black', label='obs')

#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='o',color='red')
#						elif obs[filtervar1][(n-dummy)*12] < filter1 and obs[filtervar2][(n-dummy)*12] > filter2:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='*',color='red')
#						elif obs[filtervar1][(n-dummy)*12] > filter1 and obs[filtervar2][(n-dummy)*12] < filter2:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='o',color='green')
#						else:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='*',color='green')
					elif period == 4:
						if n < len(names1)-1:
							if obs[filtervar1][(n-dummy1)*12+12] < filter1 and obs[filtervar2][(n-dummy1)*12+12] < filter2:
								plt.plot(data1[n][var1][1,0,0,:]*3600,data1[n]['zg'][0,0,0,:]-data1[n]['orog'][0,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12+12],s=4,marker='o',color='red')
#						elif obs[filtervar1][(n-dummy)*12+12] < filter1 and obs[filtervar2][(n-dummy)*12+12] > filter2:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12+12],s=8,marker='o',color='red')
#						elif obs[filtervar1][(n-dummy)*12+12] > filter1 and obs[filtervar2][(n-dummy)*12+12] < filter2:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12+12],s=4,marker='o',color='green')
#						else:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12+12],s=8,marker='o',color='green')



			plt.xlim([230,270])
			plt.ylim([0,250])
			plt.xlabel(data1[dummy1][var1].units)
			plt.ylabel(data1[dummy1]['orog'].units)
			plt.title('Vertical profile of '+data1[dummy1][var1].long_name)
			handles, labels = plt.gca().get_legend_handles_labels()
			by_label = OrderedDict(zip(labels, handles))
			plt.legend(by_label.values(), by_label.keys())
			plt.savefig(outdir+'line_vertical_low'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf')
#			plt.show()

			plt.clf()


#	plt.plot(obs['Topen'][:]-obs['Tforest'][:], norm.pdf(obs['Topen'][:]-obs['Tforest'][:]))
#	plt.show()

#	print plotvar1[dummy1].shape
#	print plotvar1[dummy1]

	diurnal = np.linspace(0.125,24,192)
	diurnal1 = np.linspace(0,24,24)

#	print diurnal.shape
#	print diurnal

#	print len(names1)

	data1_diurnal = {}

	for n in range(dummy1,len(names1)):
		data1_diurnal[n] = data1[n]

		data1_diurnal[n] = data1_diurnal[n].sel(time=slice('2018-02-18','2018-02-26'))

	for n in range(dummy1,len(names1)):
#		try:
		if len(data1_diurnal[n][var1].shape) == 3:
			plotvar1[n] = data1_diurnal[n][var1][:,0,0]
		else:
			plotvar1[n] = data1_diurnal[n][var1][:,0,0,model1_lvl-1]
#		except KeyError:
#			print 'test'
#			print n

	obs1_diurnal = obs1
	obs1_diurnal = obs1_diurnal.sel(time=slice('2018-02-18','2018-02-26'))


	for n in range(dummy1,len(names1)):
		if period == 1:
#			if data1[n]['ta'][0,0,0,136]-obs['ta'][1,(n-dummy)*12] > 2:
			plt.plot(diurnal[:],plotvar1[:],linewidth=0.3,label=model1, color='black')
#			else:
#				plt.plot(data1[n]['time'][0],np.mean(plotvar1[n][1:]),'r*') #,linewidth=0.3,label='IFS', color='black')
		elif period == 2:
#			if n % 2 == 0:
			try:
				if data1_diurnal[n].time.dt.hour[0] == 00:
#					print n
					try:
						plt.plot(diurnal[:],plotvar1[n][:],linewidth=0.3,label=model1+' - '+str(data1[n].time.dt.hour[0].values))
					except ValueError:
						print 'value'
						print n
#				ax2.plot(data1[n]['time'][start*96:end*97],data1[n]['clt'][start*96:end*97,0,0],label='IFS',linestyle=':', color='green')
			except IndexError:
				print 'key'
				print n
		elif period == 3:
#			if n % 2 == 1:
			try:
				if data1[n].time.dt.hour[0] == 12:
#				print n
					try:
						plt.plot(diurnal[:],plotvar1[n][:],linewidth=0.3,label=model1+' - '+str(data1[n].time.dt.hour[0].values))
					except ValueError:
						print 'value'
						print n
			except IndexError:
				print 'key'
				print n
#				plt.plot(data1[n]['time'][0],np.mean(plotvar1[n][1:]),'r*') #,linewidth=0.3,label='IFS', color='black')

		elif period == 4:
			plt.plot(data1[n]['time'][:],plotvar1[n][:],linewidth=0.3,label=model1, color='black')
#	if not var1 == 'tnt':
#		print n
	if period == 2:
		for n in range(0,9):
			plt.plot(diurnal1[:],obs1[n*24:24+n*24],label='Sodankyla',linewidth=0.3,linestyle='--', color='green')
	elif period == 3:
		for n in range(0,8):
			plt.plot(diurnal1[:],obs1[12+n*24:36+n*24],label='Sodankyla',linewidth=0.3,linestyle='--', color='green')
#	plt.plot(obs['time'],obs[obsvar2][:],label='Sodankyla',linestyle='--', color='green')
#	ax2.plot(obs['time'],obs['N'][:]/8,label='Sodankyla',linestyle=':', color='green')
#	plt.legend()


#	if whole_period:
#		plt.xlim([startdate,enddate])
#	else:
#		plt.xlim([shortsdate,shortedate])
	plt.xlim([0,24])
	plt.ylim([240,270])
	if period == 2:
		plt.xticks([0,3,6,9,12,15,18,21,24],[2,5,8,11,14,17,20,23,2],size=8)
	else:
		plt.xticks([0,3,6,9,12,15,18,21,24],[14,17,20,23,2,5,8,11,14],size=8)
#	plt.xticks(rotation=10,size=8)
	plt.yticks(size=8)
	plt.xlabel('Time')
	if var1 == 'tnt':
		plt.ylabel(r'$K/hour$')
	else:
		plt.ylabel(data1[dummy1][var1].units)

	plt.title(data1[dummy1][var1].long_name+' over time')
#	plt.axhline(y=0,lw='0.3')
	handles, labels = plt.gca().get_legend_handles_labels()
	by_label = OrderedDict(zip(labels, handles))
	plt.legend(by_label.values(), by_label.keys())
#		plt.legend()
	if no == 3:
		plt.savefig(outdir+'diurnal_'+model1.lower()+'_'+model2.lower()+'_'+var1+'_'+str(period)+'.pdf')
	elif no == 1:
		plt.savefig(outdir+'diurnal_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf')
	elif no == 2:
		plt.savefig(outdir+'diurnal_'+model2.lower()+'_'+var2+'_'+str(period)+'.pdf')

		plt.clf()



	return
