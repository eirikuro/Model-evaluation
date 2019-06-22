from scipy.stats import norm, gaussian_kde
import numpy as np
import pandas as pd
import xarray as xr
import os
import matplotlib.pyplot as plt
#import scipy.stats
from pandas.plotting import register_matplotlib_converters
from collections import OrderedDict
from operator import itemgetter
import datetime as dt
from matplotlib import gridspec

def plot(model1,model2,site,var1,var2,obsvar,obsvar2,data1,data2,obs,wind_vert,temp_vert,dew_vert,names1,names2,model1_lvl,model2_lvl,obs_lvl,outdir,period,no,dummy1,dummy2,filtervar1,filter1,filtervar2,filter2,filterby,no_filters,whole_period,startdate,enddate,shortsdate,shortedate,forecast,diurnal,cumulate,vertical_low,cloud,wind,hur):

	register_matplotlib_converters()

	if outdir[-1] != '/':
		outdir = outdir + '/'

	if not os.path.isdir(outdir):
		os.makedirs(outdir)

#	names1 = np.linspace(0,1,67)

#	dummy1 = 50
#	print dummy1
#	print data1[dummy1]['lat'].values
#	print data1[dummy1]['lon'].values
#	print data1[dummy1]['zg'][0,0,0,121].values

#	exit()


#	print data1[67]['time'][0]

#	exit()

	# Creating dictionaries for plotting data on one level
	plotvar1 = {}
	plotvar2 = {}
	plotvar3 = {}
	plotvar4 = {}
	cloud1 = {}
	cloud2 = {}
	cloud3 = {}
	cloud4 = {}

	plotvar1_vert = {}


	# Choosing one level from the model data from model 1
	if period == 5:
		for n in range(dummy1,len(names1)):
#			if len(data1[n][var1].shape) == 3:
#				plotvar1[n] = data1[n][var1][:,0,0]
#			else:
#				plotvar1[n] = data1[n][var1][:,0,0,model1_lvl-1]
			if data1[n].time.dt.hour[0] == 0:
				if var1 == 'Budget':
					plotvar1[n] = data1[n]['rsds'][:,0,0] - data1[n]['rsus'][:,0,0] + data1[n]['rlds'][:,0,0] - data1[n]['rlus'][:,0,0] - data1[n]['hfls'][:,0,0] - data1[n]['hfss'][:,0,0]
				else:
					if len(data1[n][var1].shape) == 3:
						if var1 == 'uas' or var1 == 'vas':
							plotvar1[n] = np.sqrt(data1[n]['uas'][:,0,0]**2+data1[n]['vas'][:,0,0]**2)
						else:
							plotvar1[n] = data1[n][var1][:,0,0]
					else:
						if var1 == 'ua' or var1 == 'va':
							plotvar1[n] = np.sqrt(data1[n]['ua'][:,0,0,model1_lvl-1]**2+data1[n]['va'][:,0,0,model1_lvl-1]**2)
						else:
							plotvar1[n] = data1[n][var1][:,0,0,model1_lvl-1]
					cloud1[n] = data1[n]['clt'][:,0,0]
			if data1[n].time.dt.hour[0] == 12:
				if var1 == 'Budget':
					plotvar3[n] = data1[n]['rsds'][:,0,0] - data1[n]['rsus'][:,0,0] + data1[n]['rlds'][:,0,0] - data1[n]['rlus'][:,0,0] - data1[n]['hfls'][:,0,0] - data1[n]['hfss'][:,0,0]
				else:
					if len(data1[n][var1].shape) == 3:
						if var1 == 'uas' or var1 == 'vas':
							plotvar3[n] = np.sqrt(data1[n]['uas'][:,0,0]**2+data1[n]['vas'][:,0,0]**2)
						else:
							plotvar3[n] = data1[n][var1][:,0,0]
					else:
						if var1 == 'ua' or var1 == 'va':
							plotvar3[n] = np.sqrt(data1[n]['ua'][:,0,0,model1_lvl-1]**2+data1[n]['va'][:,0,0,model1_lvl-1]**2)
						else:
							plotvar3[n] = data1[n][var1][:,0,0,model1_lvl-1]
					cloud3[n] = data1[n]['clt'][:,0,0]

#			if len(data4[n][var1].shape) == 3:
#				plotvar4[n] = data4[n][var1][:,0,0]
#			else:
#				plotvar4[n] = data4[n][var1][:,0,0,model1_lvl-1]
	else:
		datas1 = {}
		for n in range(dummy1,len(names1)):
			if var1 == 'Budget':
				plotvar1[n] = data1[n]['rsds'][:,0,0] - data1[n]['rsus'][:,0,0] + data1[n]['rlds'][:,0,0] - data1[n]['rlus'][:,0,0] - data1[n]['hfls'][:,0,0] - data1[n]['hfss'][:,0,0]
			else:
				if len(data1[n][var1].shape) == 3:
					if var1 == 'uas' or var1 == 'vas':
						plotvar1[n] = np.sqrt(data1[n]['uas'][:,0,0]**2+data1[n]['vas'][:,0,0]**2)
#					elif var1 == 'hfls' or var1 == 'hfss':
#						plotvar1[n] = -data1[n][var1][:,0,0]
					else:
						plotvar1[n] = data1[n][var1][:,0,0]
				else:
					if var1 == 'ua' or var1 == 'va':
						plotvar1[n] = np.sqrt(data1[n]['ua'][:,0,0,model1_lvl-1]**2+data1[n]['va'][:,0,0,model1_lvl-1]**2)
						plotvar1_vert[n] = np.sqrt(data1[n]['ua'][:,0,0,:]**2+data1[n]['va'][:,0,0,:]**2)
						plotvar1_vert[n] = xr.concat([plotvar1_vert[n],(data1[n]['uas'][:,0,0]-data1[n]['uas'][:,0,0])],dim='level')
#						print plotvar1_vert[40].shape

					else:
						plotvar1[n] = data1[n][var1][:,0,0,model1_lvl-1]
						plotvar1_vert[n] = data1[n][var1][:,0,0,:]
						if var1 == 'ta':
							plotvar1_vert[n] = xr.concat([plotvar1_vert[n],data1[n]['tas'][:,0,0]],dim='level')
						elif var1 == 'hur':
							plotvar1_vert[n] = xr.concat([plotvar1_vert[n],data1[n]['huss'][:,0,0]],dim='level')

	# If model 2 is in use go through this loop
	if no == 2 or no == 3:
		if period == 5:
			for n in range(dummy2,len(names2)):
				if data2[n].time.dt.hour[0] == 0:
					if len(data2[n][var2].shape) == 1:
						plotvar2[n] = data2[n][var2][:]
					else:
						plotvar2[n] = data2[n][var2][:,model2_lvl-1]
					cloud2[n] = data2[n]['cloud_fraction'][:]
				if data2[n].time.dt.hour[0] == 12:
					if len(data2[n][var2].shape) == 1:
						plotvar4[n] = data2[n][var2][:]
					else:
						plotvar4[n] = data2[n][var2][:,model2_lvl-1]
					cloud4[n] = data2[n]['cloud_fraction'][:]
		else:
			for n in range(dummy2,len(names2)):
				if len(data2[n][var2].shape) == 1:
					plotvar2[n] = data2[n][var2][:]
				else:
					plotvar2[n] = data2[n][var2][:,model2_lvl-1]



	# Choosing one level from observations data

	if obsvar == 'Budget':
		obs1 = obs['rsds'][:] - obs['rsus'][:] + obs['rlds'][:] - obs['rlus'][:] - obs['hfls'][:] - obs['hfss'][:]
	else:
		if len(obs[obsvar].shape) == 1:
			obs1 = obs[obsvar][:]
		else:
			obs1 = obs[obsvar][obs_lvl-1,:]

#	obs_cloud = obs['N'][:]
#	obs_cloud[:] = obs_cloud[:]*12.5

	if len(obs[obsvar2].shape) == 1:
		obs2 = obs[obsvar2][:]
	else:
		obs2 = obs[obsvar2][obs_lvl-1,:]


	if var1 == 'tnt':
		for n in range(dummy1,len(names1)):
			plotvar1[n] = plotvar1[n]*3600
			plotvar1[n] = plotvar1[n][1:]
#			data1[n]['time'] = data1[n]['time'][1:]

#	print plt.rcParams
#	print plt.getp(Figure.patch)

#	exit()

#	print data1[dummy1]['zg'][0,0,0,135].values-data1[dummy1]['orog'][0,0,0].values
#	print data1[dummy1]['zg'][0,0,0,136].values-data1[dummy1]['orog'][0,0,0].values
#	print obs['wheight'][:]

	if cloud:
		fig, (ax0, ax1, ax2) = plt.subplots(3,1, sharex=True, gridspec_kw=dict(height_ratios=[1,1,2]))
		ax3 = ax2.twinx()
		fig.subplots_adjust(bottom=0.15)
#		fig = plt.figure()
#		gs = gridspec.GridSpec(2, 1, height_ratios=[1, 2])
#		ax1 = plt.subplots(gs[0])
#		ax2 = plt.subplot(gs[1], sharex = ax1)
#		plt.setp(ax0.get_xticklabels(), visible=False)

#		ax2 = ax1.twinx(221)
	elif wind:
		fig, (ax1, ax2) = plt.subplots(2,1, sharex=True, gridspec_kw=dict(height_ratios=[1,2]))
		fig.subplots_adjust(bottom=0.15)
	elif hur:
		fig, (ax1, ax2) = plt.subplots(2,1, sharex=True, gridspec_kw=dict(height_ratios=[1,2]))
		fig.subplots_adjust(bottom=0.15)
	else:
		fig, ax2 = plt.subplots()
		fig.subplots_adjust(bottom=0.15)
#		ax2 = ax1.twinx()

#	ax1.plot(x, y1, 'g-')
#	ax2.plot(x, y2, 'b-')

#	ax1.set_xlabel('X data')
#	ax1.set_ylabel('Y1 data', color='g')
#	ax2.set_ylabel('Y2 data', color='b')

	# Plotting lineplots
	if period == 5:	#Plotting the difference between model and obs
		if no == 1 or no == 3:
			for n in range(dummy1,len(names1)):
				if forecast == 1 or forecast == 3:
					if data1[n].time.dt.hour[0] == 00:
						if wind:
							ax1.plot(data1[n]['time'][:],plotvar1[n][:],lw=1,color='black')
						elif hur:
							ax1.plot(data1[n]['time'][:],plotvar1[n][:],lw=1,color='black')
#						elif cloud:
#							ax3.plot(data1[n]['time'][:],plotvar1[n][:],lw=1,color='blue',label='_nolabel_')

						plotvar1[n] = plotvar1[n][7::8]
						ax2.plot(data1[n]['time'][7::8],plotvar1[n][:]-obs1[:],linewidth=1,label=str(data1[n].time.dt.hour[0].values)+'z forecast', color='black')
						if cloud:
#						if var1 == 'ta':
#							plotvar1[n] = plotvar1[n][7::8]
							cloud1[n] = cloud1[n][7::8]
#							plt.plot(data1[n]['time'][7::8],plotvar1[n][:]-obs1[:],linewidth=1,label=model1+' - starting at '+str(data1[n].time.dt.hour[0].values), color='black')
							ax1.plot(data1[n]['time'][7::8],cloud1[n][:]-obs['N'][:],linewidth=1, color='black')
							ax0.plot(data1[n]['time'][:],data1[n]['clt'][:,0,0],lw=1,color='black')
#						else:
#					plt.plot(obs['time'][1+(n-dummy)*12:(n-dummy)*12+24],plotvar2[n][:]-obs1[1+(n-dummy)*12:(n-dummy)*12+24],linewidth=0.4,label='IFS - starting at 00', color='blue')

				if forecast == 2 or forecast == 3:
					if data1[n].time.dt.hour[0] == 12:
						if wind:
							ax1.plot(data1[n]['time'][:],plotvar3[n][:],lw=1,color='red')
						elif hur:
							ax1.plot(data1[n]['time'][:],plotvar3[n][:],lw=1,color='red')
						plotvar3[n] = plotvar3[n][7::8]
						ax2.plot(data1[n]['time'][7::8],plotvar3[n][:]-obs1[:],linewidth=1,label=str(data1[n].time.dt.hour[0].values)+'z forecast', color='red')
#					plt.plot(obs['time'][1+(n-dummy)*12:(n-dummy)*12+24],plotvar3[n][:]-obs1[1+(n-dummy)*12:(n-dummy)*12+24],ls='--',linewidth=0.4,label='IFS - starting at 12', color='green')
						if cloud:
							cloud3[n] = cloud3[n][7::8]
							ax1.plot(data1[n]['time'][7::8],cloud3[n][:]-obs['N'][:],linewidth=1, color='red')
							ax0.plot(data1[n]['time'][:],data1[n]['clt'][:,0,0],lw=1,color='red')


		if no == 2 or no == 3:
			for n in range(dummy2,len(names2)):
				if forecast == 1 or forecast == 3:
					if data2[n].time.dt.hour[0] == 00:
						ax2.plot(data2[n]['time'][:],plotvar2[n][:]-obs1[:],linewidth=1,label=str(data2[n].time.dt.hour[0].values)+'z model run', color='black') #linewidth=1,label=model2+' - starting at '+str(data2[n].time.dt.hour[0].values), color='brown')
						if cloud:
							ax1.plot(data2[n]['time'][:],cloud2[n][:]-obs['N'][:],linewidth=1, color='black')
							ax0.plot(data2[n]['time'][:],data2[n]['cloud_fraction'][:], lw=1, color='black')
				if forecast == 2 or forecast == 3:
					if data2[n].time.dt.hour[0] == 12:
						ax2.plot(data2[n]['time'][:],plotvar4[n][:]-obs1[:],linewidth=1,label=str(data2[n].time.dt.hour[0].values)+'z model run', color='red') #linewidth=1,label=model2+' - starting at '+str(data2[n].time.dt.hour[0].values), color='green')
						if cloud:
							ax1.plot(data2[n]['time'][:],cloud4[n][:]-obs['N'][:],linewidth=1, color='red')
							ax0.plot(data2[n]['time'][:],data2[n]['cloud_fraction'][:], lw=1, color='red')


#		box = ax2.get_position()
#		ax2.set_position([box.x0, box.y0, box.width, box.height*0.3])
		if cloud:
			ax3.plot(obs['time'][:],obs1[:],lw=1,color='blue',label='Observations')
#		elif wind:
#			ax1.plot(obs['time'][:],obs1[:],lw=1,ls='--',color='orange')

		if whole_period:
			ax2.set_xlim([startdate,enddate])
#			plt.xlim([startdate,enddate])
		else:
			ax2.set_xlim([shortsdate,shortedate])
#			plt.xlim([shortsdate,shortedate])
		if cloud:
			ax0.set_ylim([0,100])
			ax1.set_ylim([-100,100])
		if var1 == 'ta' or var1 == 'tas':
			ax2.set_ylim([-14,14])
		elif var1 == 'ua':
			ax2.set_ylim([-5,5])
		elif var1 == 'hur':
			ax2.set_ylim([-45,45])
#		plt.ylim([-14,14])
		ax2.set_xlabel('Time')
		ax2.xaxis.set_tick_params(rotation=14, size=8)
#		ax1.set_xticks(rotation=10,size=8)
#		plt.xticks(rotation=10,size=8)
		ax2.yaxis.set_tick_params(size=8)
		if cloud:
			ax1.yaxis.set_tick_params(size=8)
			ax0.yaxis.set_tick_params(size=8)
		elif wind:
			ax1.yaxis.set_tick_params(size=8)
		elif hur:
			ax1.yaxis.set_tick_params(size=8)
#		ax2.set_yticks(size=8)
#		plt.yticks(size=8)
#		plt.xlabel('Time')
		if var1 == 'Budget':
			plt.ylabel(r'Surface energy budget [Wm$^{-2}$]')
		elif var1 == 'ua' or var1 == 'va':
			ax2.set_ylabel('Wind speed bias ['+data1[dummy1][var1].units+']')
			ax1.set_ylabel('Wind speed ['+data1[dummy1][var1].units+']')
			ax2.yaxis.set_label_coords(-0.08,0.5)
			ax1.yaxis.set_label_coords(-0.08,0.5)
		elif var1 == 'hur':
			ax2.set_ylabel(data1[dummy1][var1].long_name+' bias ['+data1[dummy1][var1].units+']')
			ax1.set_ylabel(data1[dummy1][var1].long_name+' ['+data1[dummy1][var1].units+']')
			ax2.yaxis.set_label_coords(-0.08,0.5)
			ax1.yaxis.set_label_coords(-0.08,0.5)
		else:
			ax2.set_ylabel(data1[dummy1][var1].long_name+' bias ['+data1[dummy1][var1].units+']')
			ax2.yaxis.set_label_coords(-0.08,0.5)
			if var1 == 'ta':
				ax3.set_ylabel(data1[dummy1][var1].long_name+' ['+data1[dummy1][var1].units+']')
			if cloud:
#				ax1.set_ylabel('Cloud fraction')
				ax1.set_ylabel('Cloud fraction [%]')
				ax1.yaxis.set_label_coords(-0.1,1.0)
#			plt.ylabel(data1[dummy1][var1].units)
		ax2.axhline(y=0, lw='0.8', ls='--',color='gray')
		if var1 == 'ta' or var1 == 'tas':
			ax2.axhline(y=5, lw='0.8', ls='--',color='gray')
			ax2.axhline(y=-5, lw='0.8', ls='--',color='gray')
			ax2.axhline(y=10, lw='0.8', ls='--',color='gray')
			ax2.axhline(y=-10, lw='0.8', ls='--',color='gray')
		elif var1 == 'ua':
			ax2.axhline(y=0, lw='0.8', ls='--',color='gray')
			ax2.axhline(y=2, lw='0.8', ls='--',color='gray')
			ax2.axhline(y=-2, lw='0.8', ls='--',color='gray')
		elif var1 == 'hur':
			ax2.axhline(y=0, lw='0.8', ls='--',color='gray')
			ax2.axhline(y=20, lw='0.8', ls='--',color='gray')
			ax2.axhline(y=-20, lw='0.8', ls='--',color='gray')
#			ax2.axhline(y=4, lw='0.8', ls='--',color='gray')
#			ax2.axhline(y=-4, lw='0.8', ls='--',color='gray')

		if cloud:
			ax1.axhline(y=0, lw='0.8', ls='--',color='gray')
			ax1.axhline(y=-50, lw='0.8', ls='--',color='gray')
			ax1.axhline(y=50, lw='0.8', ls='--',color='gray')
			ax0.axhline(y=25, lw='0.8', ls='--',color='gray')
			ax0.axhline(y=50, lw='0.8', ls='--',color='gray')
			ax0.axhline(y=75, lw='0.8', ls='--',color='gray')


#		ax1.fill_between(ax.get_xlim(), y1, y2, color=c, alpha=0.5)
		if cloud:
			ax0.axvspan('2018-02-17', '2018-02-24', facecolor='orange', alpha=0.3)
			ax0.axvspan('2018-02-01', '2018-02-09', facecolor='yellow', alpha=0.3)
			ax0.axvspan('2018-02-27', '2018-03-08', facecolor='yellow', alpha=0.3)
			ax0.axvspan('2018-03-13', '2018-03-17', facecolor='yellow', alpha=0.3)
			ax0.axvspan('2018-03-20', '2018-03-31', facecolor='yellow', alpha=0.3)
		if cloud or wind or hur:
			ax1.axvspan('2018-02-17', '2018-02-24', facecolor='orange', alpha=0.3)
			ax2.axvspan('2018-02-17', '2018-02-24', facecolor='orange', alpha=0.3)

			ax1.axvspan('2018-02-01', '2018-02-09', facecolor='yellow', alpha=0.3)
			ax2.axvspan('2018-02-01', '2018-02-09', facecolor='yellow', alpha=0.3)

			ax1.axvspan('2018-02-27', '2018-03-08', facecolor='yellow', alpha=0.3)
			ax2.axvspan('2018-02-27', '2018-03-08', facecolor='yellow', alpha=0.3)

			ax1.axvspan('2018-03-13', '2018-03-17', facecolor='yellow', alpha=0.3)
			ax2.axvspan('2018-03-13', '2018-03-17', facecolor='yellow', alpha=0.3)

			ax1.axvspan('2018-03-20', '2018-03-31', facecolor='yellow', alpha=0.3)
			ax2.axvspan('2018-03-20', '2018-03-31', facecolor='yellow', alpha=0.3)
#		plt.axhline(y=(np.std(obs['Topen'][:]-obs['Tforest'][:])+(0.176-0.0028*273)), lw='0.8', ls='--',color='gray')
#		plt.axhline(y=(-np.std(obs['Topen'][:]-obs['Tforest'][:])-(0.176-0.0028*273)), lw='0.8', ls='--',color='gray')

#		if model1 == 'IFS-ECMWF':
#			if var1 == 'Budget':
#				plt.title('Difference between model and obs for Surface Energy Budget over time')
#			else:
#				ax1.set_title('Difference between model and obs for '+data1[dummy1][var1].long_name+' over time')
#		else:
#			plt.title('Difference between model and obs for '+data2[dummy2][var1].longname+' over time')
		handles, labels = ax2.get_legend_handles_labels()
		by_label = OrderedDict(zip(labels, handles))
#		handles2, labels2 = ax3.get_legend_handles_labels()
#		by_label = OrderedDict(zip(labels, handles),zip(labels2,handles2))
		if var1 == 'ta':
			ax2.legend(by_label.values(), by_label.keys(),loc='lower right') #, by_label2.values(), by_label2.keys())
			ax3.legend(loc='lower left')
		else:
			ax2.legend(by_label.values(), by_label.keys()) #, by_label2.values(), by_label2.keys())
#		plt.figlegend()
		plt.subplots_adjust(hspace=.0)
		if no == 3:
			plt.savefig(outdir+'line_diff_'+model1.lower()+'_'+model2.lower()+'_'+var1+'.pdf')
		elif no == 1:
			plt.savefig(outdir+'line_diff_'+model1.lower()+'_'+var1+'.pdf',bbox_inches='tight',pad_inches=0)
		elif no == 2:
			plt.savefig(outdir+'line_diff_'+model2.lower()+'_'+var2+'.pdf',bbox_inches='tight',pad_inches=0)

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
			elif period == 3:
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
		elif var1 == 'Budget':
			plt.ylabel(r'Surface energy budget')
		else:
			plt.ylabel(data1[dummy1][var1].units)

#		if var1 == 'Budget':
#			plt.title('Surface energy budget over time')
#		else:
#			plt.title(data1[dummy1][var1].long_name+' over time')
#		plt.axhline(y=0,lw='0.3')
		handles, labels = plt.gca().get_legend_handles_labels()
		by_label = OrderedDict(zip(labels, handles))
		plt.legend(by_label.values(), by_label.keys())
#		plt.legend()
		if no == 3:
			plt.savefig(outdir+'line_'+model1.lower()+'_'+model2.lower()+'_'+var1+'_'+str(period)+'.pdf')
		elif no == 1:
			plt.savefig(outdir+'line_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)
		elif no == 2:
			plt.savefig(outdir+'line_'+model2.lower()+'_'+var2+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)

		plt.clf()



	print 'Lineplot for '+model1+' finished'

	plt.clf()

	'''
######### This section is a plot that was only plotted once and does not have to be plotted again ###############

	plt.plot(obs['time'],obs['Topen'][:]-273, label='open',linewidth=0.5,color='black')
	plt.plot(obs['time'],obs['Tforest'][:]-273, label='forest',linestyle='--',linewidth=0.5,color='green')
	plt.savefig(outdir+'open+forest.pdf')

	plt.clf()

	plt.plot(obs['time'],obs['Topen'][:]-obs['Tforest'][:],label='open-forest', linewidth=0.3,color='blue')
	plt.plot(obs['time'],(obs['Topen'][:]-obs['Tforest'][:])-np.std(obs['Topen'][:]-obs['Tforest'][:]),label='std',ls='--', linewidth=0.3,color='green')
	plt.legend()
	plt.xlabel(r'$K$')
	plt.ylabel('Time')
	plt.title('2m Temperature in Sodankyla as well as the difference')
	plt.savefig(outdir+'open-forest.pdf')

	plt.clf()

	'''

#	Plotting pdf for LWN

#	x = np.arange(150,500,0.24717514124)#

	bw_values = [None, 0.1] #, 0.01]

#	kde = [scipy.stats.gaussian_kde(obs['rlds'][:]-obs['rlus'][:],bw_method=bw) for bw in bw_values]#

	obs_pdf = obs.sel(time=slice('2018-02-03','2018-02-07'))

	kde = [gaussian_kde(obs_pdf['rlds'][:]-obs_pdf['rlus'][:],bw_method=bw) for bw in bw_values]
	plt.hist(obs_pdf['rlds'][:]-obs_pdf['rlus'][:], 10, density=1, facecolor='green', alpha=0.5)
	t_range = np.linspace(-100,30,800)
	for i, bw in enumerate(bw_values):
	    plt.plot(t_range,kde[i](t_range),lw=2, label='bw = '+str(bw))
	plt.legend()

#	plt.plot(norm.pdf(obs['rlds'][:]-obs['rlus'][:]))#
#	plt.show()#

	plt.savefig(outdir+'pdf-period1.pdf')
	plt.clf()

#	'''
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

#	fig = plt.figure()
#	ax = plt.subplot(111)



#	label_param = label_param.replace(r"\", r"\\")

#	plt.rc('text', usetex=True)
#	plt.rc('font', family='serif')

#	ax = fig.add_axes([0.1,0.1,0.7,0.8])
#	fig, ax=plt.subplot()

#	ax.set_prop_cycle('color',['red','red','blue', 'blue', 'green','green','black', 'black', 'yellow','yellow','brown','brown','orange','orange','purple','purple','pink','pink','cyan','cyan','olive','olive']) #plt.cm.gist_rainbow([0,0,0.1,0.1,0.2,0.2,0.3,0.3,0.4,0.4,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1,1]))


#	ax.set_prop_cycle('color',plt.cm.gist_rainbow(np.linspace(0,1,10)))
#	ax.set_prop_cycle(obs_color,plt.cm.gist_rainbow(np.linspace(0,1,10)))


#	ax.set_color_cycle(['red','red','blue', 'blue', 'green','green','black', 'black', 'yellow','yellow','brown','brown','orange','orange','purple','purple','pink','pink'])

	if var1 != 'Budget':
		if len(data1[n][var1].shape) == 4:
			# Vertical profiles for initial conditions of forecast
			if period == 1 or period == 2 or period == 3 or period == 4:
				fig, (ax1, ax2) = plt.subplots(1,2, sharey=True, gridspec_kw=dict(width_ratios=[1,1]))
				ax1.set_prop_cycle('color',['red','red','blue', 'blue', 'green','green','black', 'black', 'yellow','yellow','brown','brown','orange','orange','purple','purple','pink','pink']) #plt.cm.gist_rainbow([0,0,0.1,0.1,0.2,0.2,0.3,0.3,0.4,0.4,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1,1]))
				ax2.set_prop_cycle('color',[ 'cyan','cyan','olive','olive','darkred','darkred','royalblue','royalblue','darkorange','darkorange','deeppink','deeppink','lime','lime','darkgray','darkgray']) #plt.cm.gist_rainbow([0,0,0.1,0.1,0.2,0.2,0.3,0.3,0.4,0.4,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1,1]))
				for n in range(dummy1,len(names1)):
					if no_filters == 1:
						if period == 1:
#							if data1[n][filtervar][0,0,0] < filter:
							if obs[filtervar1][(n-dummy1)*12] < filter1:
								plt.plot(data1[n][var1][1,0,0,:],data1[n]['zg'][1,0,0,:]-data1[n]['orog'][1,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#								plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],label='obs',c='black')
						elif period == 2:
							if n % 2 == 0:
#								if data1[n][filtervar][0,0,0] < filter:
								if obs[filtervar1][(n-dummy1)*12] < filter1:
									plt.plot(data1[n][var1][1,0,0,:],data1[n]['zg'][1,0,0,:]-data1[n]['orog'][1,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#									plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],label='obs',c='black')
						elif period == 3:
							if n % 2 == 1:
#								if data1[n][filtervar][0,0,0] < filter:
								if obs[filtervar1][(n-dummy1)*12] < filter1:
									plt.plot(data1[n][var1][1,0,0,:],data1[n]['zg'][1,0,0,:]-data1[n]['orog'][1,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#									plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],c='black',label='obs')
#								plt.plot(data1[n][var1][0,0,0,:],data1[n]['zg'][0,0,0,:],linewidth=0.3,label='IFS')
						elif period == 4:
#								if data1[n][filtervar][0,0,0] < filter:
								if obs[filtervar1][(n-dummy1)*12] < filter1:
									plt.plot(data1[n][var1][0,0,0,:],data1[n]['zg'][0,0,0,:]-data1[n]['orog'][0,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
					else:
						if period == 1:
							if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
								plt.plot(data1[n][var1][1,0,0,:]*3600,data1[n]['zg'][1,0,0,:]-data1[n]['orog'][0,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#								if data1[n].time.dt.hour[0] == 12:
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

#								plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],label='obs',c='black')

#						plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='o',color='red')
#					elif obs[filtervar1][(n-dummy)*12] < filter1 and obs[filtervar2][(n-dummy)*12] > filter2:
#						plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=8,marker='o',color='red')
#					elif obs[filtervar1][(n-dummy)*12] > filter1 and obs[filtervar2][(n-dummy)*12] < filter2:
#						plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='o',color='green')
#					else:
#						plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=8,marker='o',color='green')
						elif period == 2:
							if data1[n].time.dt.hour[0] == 00:
#								if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
#								if data1[n]['tas'][0,0,0].values-obs['Topen'][(n-dummy1)*12].values > 5:
								if obs['ta'][1,(n-dummy1)*12].values < 255:
									if data1[n].time.dt.month[0] == 2:
										if data1[n].time.dt.day[0] < 15:
											ax1.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=1.2,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
										else:
											ax2.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=1.2,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
										day = str(data1[n].time.dt.day[0].values)
										month = str(data1[n].time.dt.month[0].values)
										year = str(data1[n].time.dt.year[0].values)
										if len(day) == 1:
											day = '0'+day
										if len(month) == 1:
											month = '0'+month
										days = year+month+day
										if var1 == 'ta':
											obs_plot = temp_vert[temp_vert.DATE == days]
											obs_plot.DATA_VALUE = obs_plot.DATA_VALUE+273
										elif var1 == 'ua' or var1 == 'va':
											obs_plot = wind_vert[wind_vert.DATE == days]
										elif var1 == 'hur':
											obs_plot = temp_vert[temp_vert.DATE == days]
											obs_plot_temporary = dew_vert[dew_vert.DATE == days]
											obs_plot.DATA_VALUE = 100 * (np.exp(5423*((1/273)-(1/(obs_plot_temporary.DATA_VALUE.values+273))))/np.exp(5423*((1/273)-(1/(temp_vert[temp_vert.DATE == days].DATA_VALUE.values+273)))))    #100 - 5*((temp_vert[temp_vert.DATE == days].DATA_VALUE.values+273) - (obs_plot_temporary.DATA_VALUE.values+273))
										obs_plot = obs_plot[obs_plot.TIME == '00']
										obs_plot = obs_plot[obs_plot.ALTITUDE < 2300]
										if int(float(day)) < 15:
											ax1.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=1.2,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
										else:
											ax2.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=1.2,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='o',color='red')
#						elif obs[filtervar1][(n-dummy)*12] < filter1 and obs[filtervar2][(n-dummy)*12] > filter2:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='*',color='red')
#						elif obs[filtervar1][(n-dummy)*12] > filter1 and obs[filtervar2][(n-dummy)*12] < filter2:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='o',color='green')
#						else:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy)*12],s=4,marker='*',color='green')
						elif period == 3:
							if data1[n].time.dt.hour[0] == 12:
#							if n % 2 == 1:
#								if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
#								if data1[n]['tas'][0,0,0].values-obs['Topen'][(n-dummy1)*12].values > 5:
								if obs['ta'][1,(n-dummy1)*12].values > 254:
									 if data1[n].time.dt.month[0] == 2:
										if data1[n].time.dt.day[0] < 10:
											ax1.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
										else:
											ax2.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#										plt.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#										plt.plot(plotvar1_vert[n][0,:],data1[n]['zg'][0,0,0,:]-data1[n]['orog'][0,0,0],linewidth=0.8,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#									plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],c='black')

										day = str(data1[n].time.dt.day[0].values)
										month = str(data1[n].time.dt.month[0].values)
										year = str(data1[n].time.dt.year[0].values)
										if len(day) == 1:
											day = '0'+day
										if len(month) == 1:
											month = '0'+month
										days = year+month+day

										if var1 == 'ta':
											obs_plot = temp_vert[temp_vert.DATE == days]
#											obs_plot1 = dew_vert[dew_vert.DATE == days]
											obs_plot.DATA_VALUE = obs_plot.DATA_VALUE+273
#											obs_plot1.DATA_VALUE = obs_plot1.DATA_VALUE+273
										elif var1 == 'ua' or var1 == 'va':
											obs_plot = wind_vert[wind_vert.DATE == days]
										elif var1 == 'hur':
											obs_plot = temp_vert[temp_vert.DATE == days]
											obs_plot_temporary = dew_vert[dew_vert.DATE == days]
											obs_plot.DATA_VALUE = 100 - 5*(obs_plot.DATA_VALUE.values - obs_plot_temporary.DATA_VALUE.values)
#											obs_plot = temp_vert[temp_vert.DATE == days]
#											obs_plot.DATA_VALUE = 100-5*(temp_vert[temp_vert.DATE == days].DATA_VALUE.values-dew_vert[dew_vert.DATE == days].DATA_VALUE.values)

										obs_plot = obs_plot[obs_plot.TIME == '12']
#										obs_plot1 = obs_plot1[obs_plot1.TIME == '12']
										obs_plot = obs_plot[obs_plot.ALTITUDE < 2300]
#										obs_plot1 = obs_plot1[obs_plot1.ALTITUDE < 2300]

										if int(float(day)) < 10:
											ax1.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
										else:
											ax2.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

#										plt.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-180,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#										plt.plot(obs_plot1.DATA_VALUE,obs_plot1.ALTITUDE-180,lw=0.8,label='obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

#									plt.plot(obs_plot.DATA_VALUE+273,obs_plot.ALTITUDE-180,lw='0.3',color='black',label='obs')

#									plt.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-180, color='black', label='obs')

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


#####			This block is to calculate values for xlim ######
				max_value = np.amax(plotvar1_vert[dummy1].values)  # maximum value
				min_value = np.amin(plotvar1_vert[dummy1].values)  # maximum value
				for n in range(dummy1+1,len(names1)):
					if np.any(max_value < plotvar1_vert[n].values):  # maximum value
						max_value = np.amax(plotvar1_vert[n][:,100:].values)  # maximum value
					if np.any(min_value > plotvar1_vert[n].values):
						min_value = np.amin(plotvar1_vert[n][:,100:].values)  # minimum value
				if np.any(max_value < obs_plot.DATA_VALUE.values):  # maximum value
					max_value = np.amax(obs_plot.DATA_VALUE.values)  # maximum value
				if np.any(min_value > obs_plot.DATA_VALUE.values):
					min_value = np.amin(obs_plot.DATA_VALUE.values)  # minimum value
				max_value = np.ceil(max_value)
				min_value = np.floor(min_value)
######-------------------------------------------------------------########
				box1 = ax1.get_position()
#				print box1
				ax1.set_position([box1.x0, box1.y0, box1.width * 0.8, box1.height])
				box1 = ax1.get_position()
#				print box1
				box2 = ax2.get_position()
				ax2.set_position([box2.x0, box2.y0, box2.width * 0.8, box2.height])

#				ax1.set_position(

				ax1.set_yscale('log')
				ax2.set_yscale('log')
				ax1.set_xlim([min_value,max_value])
				ax2.set_xlim([min_value,max_value])
#				if vertical_low:
#					plt.ylim([0,350])
#				else:
				plt.ylim([0,2000])
				ax2.tick_params(axis='y',which='both',left=False,right=False)
#				ax1.set_xlabel(data1[dummy1][var1].units)
#				ax2.set_xlabel(data1[dummy1][var1].units)
#				ax1.set_ylabel(data1[dummy1]['orog'].units)

				if var1 == 'ua' or var1 == 'va':
					ax1.set_xlabel('Wind speed ['+data1[dummy1][var1].units+']')
				else:
					ax1.set_xlabel(data1[dummy1][var1].long_name+' ['+data1[dummy1][var1].units+']')
				ax1.xaxis.set_label_coords(1.0,-0.08)
				ax1.set_ylabel('Height above surface ['+data1[dummy1]['orog'].units+']')


#				plt.title('Vertical profile of '+data1[dummy1][var1].long_name)
#				handles, labels = plt.gca().get_legend_handles_labels()
#				by_label = OrderedDict(zip(labels, handles))

#				plt.legend(by_label.values(), by_label.keys())

#				ax2.legend(by_label.values(), by_label.keys(),loc='center left', bbox_to_anchor=(1, 0.5),fontsize='small')
				ax1.legend(loc='lower right',fontsize=8)
				ax2.legend(loc='lower right',fontsize=8)
				plt.subplots_adjust(wspace=.0)
				if vertical_low:
					plt.savefig(outdir+'line_vertical_2_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)
				else:
					plt.savefig(outdir+'line_vertical_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)
#				plt.show()

				plt.clf()



		# Vertical profiles for 12 hours into forecast
			if period == 1 or period == 2 or period == 3 or period == 4:
				fig, (ax1, ax2) = plt.subplots(1,2, sharey=True, gridspec_kw=dict(width_ratios=[1,1]))
				ax1.set_prop_cycle('color',['red','red','blue', 'blue', 'green','green','black', 'black', 'yellow','yellow','brown','brown']) #plt.cm.gist_rainbow([0,0,0.1,0.1,0.2,0.2,0.3,0.3,0.4,0.4,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1,1]))
				ax2.set_prop_cycle('color',['orange','orange','purple','purple','pink','pink','cyan','cyan','olive','olive']) #plt.cm.gist_rainbow([0,0,0.1,0.1,0.2,0.2,0.3,0.3,0.4,0.4,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1,1]))
				for n in range(dummy1,len(names1)):

					if period == 2:
						if data1[n].time.dt.hour[0] == 00:
							if obs['ta'][1,(n-dummy1)*12].values < 255:
								if data1[n].time.dt.month[0] == 2:
									if data1[n].time.dt.day[0] < 10:
										ax1.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
									else:
										ax2.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

									day = str(data1[n].time.dt.day[0].values)
									month = str(data1[n].time.dt.month[0].values)
									year = str(data1[n].time.dt.year[0].values)
									if len(day) == 1:
										day = '0'+day
									if len(month) == 1:
										month = '0'+month
									days = year+month+day

									if var1 == 'ta':
										obs_plot = temp_vert[temp_vert.DATE == days]
										obs_plot.DATA_VALUE = obs_plot.DATA_VALUE+273
									elif var1 == 'ua' or var1 == 'va':
										obs_plot = wind_vert[wind_vert.DATE == days]
#										obs_plot.iloc([0,3]).values() = 0
#										print obs_plot.wind_vert
#										print obs_plot[-1,2]
									elif var1 == 'hur':
										obs_plot = temp_vert[temp_vert.DATE == days]
										obs_plot_temporary = dew_vert[dew_vert.DATE == days]
										obs_plot.DATA_VALUE = 100 * (np.exp(5423*((1/273)-(1/obs_plot_temporary.DATA_VALUE.values)))/np.exp(5423*((1/273)-(1/temp_vert[temp_vert.DATE == days].DATA_VALUE.values))))    #100 - 5*((temp_vert[temp_vert.DATE == days].DATA_VALUE.values+273) - (obs_plot_temporary.DATA_VALUE.values+273))

									obs_plot = obs_plot[obs_plot.TIME == '12']
									obs_plot = obs_plot[obs_plot.ALTITUDE < 2300]
									if int(float(day)) < 10:
										ax1.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
									else:
										ax2.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

					elif period == 3:
						if data1[n].time.dt.hour[0] == 12:
							if obs['ta'][1,(n-dummy1)*12].values < 255:
								 if data1[n].time.dt.month[0] == 2:
									if data1[n].time.dt.day[0] < 10:
										ax1.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
									else:
										ax2.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

									day = str(data1[n].time.dt.day[0].values+1)
									month = str(data1[n].time.dt.month[0].values)
									year = str(data1[n].time.dt.year[0].values)
									if len(day) == 1:
										day = '0'+day
									if len(month) == 1:
										month = '0'+month
									days = year+month+day

									if var1 == 'ta':
										obs_plot = temp_vert[temp_vert.DATE == days]
#										obs_plot1 = dew_vert[dew_vert.DATE == days]
										obs_plot.DATA_VALUE = obs_plot.DATA_VALUE+273
#										obs_plot1.DATA_VALUE = obs_plot1.DATA_VALUE+273
									elif var1 == 'ua' or var1 == 'va':
										obs_plot = wind_vert[wind_vert.DATE == days]
									elif var1 == 'hur':
										obs_plot = temp_vert[temp_vert.DATE == days]
										obs_plot_temporary = dew_vert[dew_vert.DATE == days]
										obs_plot.DATA_VALUE = 100 - 5*(obs_plot.DATA_VALUE.values - obs_plot_temporary.DATA_VALUE.values)
#										obs_plot = temp_vert[temp_vert.DATE == days]
#										obs_plot.DATA_VALUE = 100-5*(temp_vert[temp_vert.DATE == days].DATA_VALUE.values-dew_vert[dew_vert.DATE == days].DATA_VALUE.values)

									obs_plot = obs_plot[obs_plot.TIME == '00']
#									obs_plot1 = obs_plot1[obs_plot1.TIME == '12']
									obs_plot = obs_plot[obs_plot.ALTITUDE < 2300]
#									obs_plot1 = obs_plot1[obs_plot1.ALTITUDE < 2300]

									if int(float(day)) < 10:
										ax1.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
									else:
										ax2.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))




#####			This block is to calculate values for xlim ######
				max_value = np.amax(plotvar1_vert[dummy1].values)  # maximum value
				min_value = np.amin(plotvar1_vert[dummy1].values)  # maximum value
				for n in range(dummy1+1,len(names1)):
					if np.any(max_value < plotvar1_vert[n].values):  # maximum value
						max_value = np.amax(plotvar1_vert[n][:,100:].values)  # maximum value
					if np.any(min_value > plotvar1_vert[n].values):
						min_value = np.amin(plotvar1_vert[n][:,100:].values)  # minimum value
				if np.any(max_value < obs_plot.DATA_VALUE.values):  # maximum value
					max_value = np.amax(obs_plot.DATA_VALUE.values)  # maximum value
				if np.any(min_value > obs_plot.DATA_VALUE.values):
					min_value = np.amin(obs_plot.DATA_VALUE.values)  # minimum value
				max_value = np.ceil(max_value)
				min_value = np.floor(min_value)
######-------------------------------------------------------------########
				box1 = ax1.get_position()
#				print box1
				ax1.set_position([box1.x0, box1.y0, box1.width * 0.8, box1.height])
				box1 = ax1.get_position()
#				print box1
				box2 = ax2.get_position()
				ax2.set_position([box2.x0, box2.y0, box2.width * 0.8, box2.height])

#				ax1.set_position(

				ax1.set_yscale('log')
				ax2.set_yscale('log')
				ax1.set_xlim([min_value,max_value])
				ax2.set_xlim([min_value,max_value])
				if vertical_low:
					plt.ylim([0,350])
				else:
					plt.ylim([0,2000])
				ax2.tick_params(axis='y',which='both',left=False,right=False)
#				ax1.set_xlabel(data1[dummy1][var1].units)
#				ax2.set_xlabel(data1[dummy1][var1].units)
#				ax1.set_ylabel(data1[dummy1]['orog'].units)

				if var1 == 'ua' or var1 == 'va':
					ax1.set_xlabel('Wind speed ['+data1[dummy1][var1].units+']')
				else:
					ax1.set_xlabel(data1[dummy1][var1].long_name+'['+data1[dummy1][var1].units+']')
				ax1.xaxis.set_label_coords(1.0,-0.08)
				ax1.set_ylabel('Height above surface ['+data1[dummy1]['orog'].units+']')

#				plt.title('Vertical profile of '+data1[dummy1][var1].long_name)
#				handles, labels = plt.gca().get_legend_handles_labels()
#				by_label = OrderedDict(zip(labels, handles))
#				plt.legend(by_label.values(), by_label.keys())
#				ax2.legend(by_label.values(), by_label.keys(),loc='center left', bbox_to_anchor=(1, 0.5),fontsize='small')
				ax1.legend(loc='lower left',fontsize=8)
				ax2.legend(loc='lower left',fontsize=8)

				plt.subplots_adjust(wspace=.0)
				if vertical_low:
					plt.savefig(outdir+'line_vertical_low_mid_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)
				else:
					plt.savefig(outdir+'line_vertical_mid_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)
#				plt.show()

				plt.clf()







		# Vertical profiles for 24 hours into forecast
			if period == 1 or period == 2 or period == 3 or period == 4:
				fig, (ax1, ax2) = plt.subplots(1,2, sharey=True, gridspec_kw=dict(width_ratios=[1,1]))
				ax1.set_prop_cycle('color',['red','red','blue', 'blue', 'green','green','black', 'black', 'yellow','yellow','brown','brown']) #plt.cm.gist_rainbow([0,0,0.1,0.1,0.2,0.2,0.3,0.3,0.4,0.4,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1,1]))
				ax2.set_prop_cycle('color',['orange','orange','purple','purple','pink','pink','cyan','cyan','olive','olive']) #plt.cm.gist_rainbow([0,0,0.1,0.1,0.2,0.2,0.3,0.3,0.4,0.4,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1,1]))
				for n in range(dummy1,len(names1)):

					if period == 2:
						if data1[n].time.dt.hour[0] == 00:
							if obs['ta'][1,(n-dummy1)*12].values < 255:
								if data1[n].time.dt.month[0] == 2:
									if data1[n].time.dt.day[0] < 10:
										ax1.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
									else:
										ax2.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

									day = str(data1[n].time.dt.day[0].values+1)
									month = str(data1[n].time.dt.month[0].values)
									year = str(data1[n].time.dt.year[0].values)
									if len(day) == 1:
										day = '0'+day
									if len(month) == 1:
										month = '0'+month
									days = year+month+day

									if var1 == 'ta':
										obs_plot = temp_vert[temp_vert.DATE == days]
										obs_plot.DATA_VALUE = obs_plot.DATA_VALUE+273
									elif var1 == 'ua' or var1 == 'va':
										obs_plot = wind_vert[wind_vert.DATE == days]
#										obs_plot.iloc([0,3]).values() = 0
#										print obs_plot.wind_vert
#										print obs_plot[-1,2]
									elif var1 == 'hur':
										obs_plot = temp_vert[temp_vert.DATE == days]
										obs_plot_temporary = dew_vert[dew_vert.DATE == days]
										obs_plot.DATA_VALUE = 100 * (np.exp(5423*((1/273)-(1/obs_plot_temporary.DATA_VALUE.values)))/np.exp(5423*((1/273)-(1/temp_vert[temp_vert.DATE == days].DATA_VALUE.values))))    #100 - 5*((temp_vert[temp_vert.DATE == days].DATA_VALUE.values+273) - (obs_plot_temporary.DATA_VALUE.values+273))

									obs_plot = obs_plot[obs_plot.TIME == '00']
									obs_plot = obs_plot[obs_plot.ALTITUDE < 2300]
									if int(float(day)) < 10:
										ax1.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
									else:
										ax2.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

					elif period == 3:
						if data1[n].time.dt.hour[0] == 12:
							if obs['ta'][1,(n-dummy1)*12].values < 255:
								 if data1[n].time.dt.month[0] == 2:
									if data1[n].time.dt.day[0] < 10:
										ax1.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
									else:
										ax2.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

									day = str(data1[n].time.dt.day[0].values+1)
									month = str(data1[n].time.dt.month[0].values)
									year = str(data1[n].time.dt.year[0].values)
									if len(day) == 1:
										day = '0'+day
									if len(month) == 1:
										month = '0'+month
									days = year+month+day

									if var1 == 'ta':
										obs_plot = temp_vert[temp_vert.DATE == days]
#										obs_plot1 = dew_vert[dew_vert.DATE == days]
										obs_plot.DATA_VALUE = obs_plot.DATA_VALUE+273
#										obs_plot1.DATA_VALUE = obs_plot1.DATA_VALUE+273
									elif var1 == 'ua' or var1 == 'va':
										obs_plot = wind_vert[wind_vert.DATE == days]
									elif var1 == 'hur':
										obs_plot = temp_vert[temp_vert.DATE == days]
										obs_plot_temporary = dew_vert[dew_vert.DATE == days]
										obs_plot.DATA_VALUE = 100 - 5*(obs_plot.DATA_VALUE.values - obs_plot_temporary.DATA_VALUE.values)
#										obs_plot = temp_vert[temp_vert.DATE == days]
#										obs_plot.DATA_VALUE = 100-5*(temp_vert[temp_vert.DATE == days].DATA_VALUE.values-dew_vert[dew_vert.DATE == days].DATA_VALUE.values)

									obs_plot = obs_plot[obs_plot.TIME == '12']
#									obs_plot1 = obs_plot1[obs_plot1.TIME == '12']
									obs_plot = obs_plot[obs_plot.ALTITUDE < 2300]
#									obs_plot1 = obs_plot1[obs_plot1.ALTITUDE < 2300]

									if int(float(day)) < 10:
										ax1.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
									else:
										ax2.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))




#####			This block is to calculate values for xlim ######
				max_value = np.amax(plotvar1_vert[dummy1].values)  # maximum value
				min_value = np.amin(plotvar1_vert[dummy1].values)  # maximum value
				for n in range(dummy1+1,len(names1)):
					if np.any(max_value < plotvar1_vert[n].values):  # maximum value
						max_value = np.amax(plotvar1_vert[n][:,100:].values)  # maximum value
					if np.any(min_value > plotvar1_vert[n].values):
						min_value = np.amin(plotvar1_vert[n][:,100:].values)  # minimum value
				if np.any(max_value < obs_plot.DATA_VALUE.values):  # maximum value
					max_value = np.amax(obs_plot.DATA_VALUE.values)  # maximum value
				if np.any(min_value > obs_plot.DATA_VALUE.values):
					min_value = np.amin(obs_plot.DATA_VALUE.values)  # minimum value
				max_value = np.ceil(max_value)
				min_value = np.floor(min_value)
######-------------------------------------------------------------########
				box1 = ax1.get_position()
#				print box1
				ax1.set_position([box1.x0, box1.y0, box1.width * 0.8, box1.height])
				box1 = ax1.get_position()
#				print box1
				box2 = ax2.get_position()
				ax2.set_position([box2.x0, box2.y0, box2.width * 0.8, box2.height])

#				ax1.set_position(

				ax1.set_yscale('log')
				ax2.set_yscale('log')
				ax1.set_xlim([min_value,max_value])
				ax2.set_xlim([min_value,max_value])
				if vertical_low:
					plt.ylim([0,350])
				else:
					plt.ylim([0,2000])
				ax2.tick_params(axis='y',which='both',left=False,right=False)
				if var1 == 'ua' or var1 == 'va':
					ax1.set_xlabel('Wind speed ['+data1[dummy1][var1].units+']')
				else:
					ax1.set_xlabel(data1[dummy1][var1].long_name+'['+data1[dummy1][var1].units+']')
				ax1.xaxis.set_label_coords(1.0,-0.08)
				ax1.set_ylabel('Height above surface ['+data1[dummy1]['orog'].units+']')

#				ax2.set_xlabel(data1[dummy1][var1].units)

#				plt.title('Vertical profile of '+data1[dummy1][var1].long_name)

#				handles, labels = plt.gca().get_legend_handles_labels()
#				by_label = OrderedDict(zip(labels, handles))
#				plt.legend(by_label.values(), by_label.keys())
#				ax2.legend(by_label.values(), by_label.keys(),loc='center left', bbox_to_anchor=(1, 0.5),fontsize='small')

				ax1.legend(loc='lower left',fontsize=8)
				ax2.legend(loc='lower left',fontsize=8)
				plt.subplots_adjust(wspace=.0)
				if vertical_low:
					plt.savefig(outdir+'line_vertical_low_end_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)
				else:
					plt.savefig(outdir+'line_vertical_end_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)
#				plt.show()

				plt.clf()






#	plt.plot(obs['Topen'][:]-obs['Tforest'][:], norm.pdf(obs['Topen'][:]-obs['Tforest'][:]))
#	plt.show()



#	Plotting diurnal cycles

	if diurnal:
		if period == 1 or period == 2 or period == 3 or period == 4:

			fig = plt.figure()
			ax = plt.subplot(111)

			diurnal = np.linspace(0.125,24,192)
			diurnal1 = np.linspace(0,24,24)
			diurnal2 = np.linspace(-12,12,24)

			data1_diurnal = {}

			for n in range(dummy1,len(names1)):
				data1_diurnal[n] = data1[n]

				data1_diurnal[n] = data1_diurnal[n].sel(time=slice('2018-02-18','2018-02-26'))

			for n in range(dummy1,len(names1)):
				if var1 == 'Budget':
					plotvar1[n] = data1_diurnal[n]['rsds'][:,0,0] - data1_diurnal[n]['rsus'][:,0,0] + data1_diurnal[n]['rlds'][:,0,0] - data1_diurnal[n]['rlus'][:,0,0] - data1_diurnal[n]['hfls'][:,0,0] - data1_diurnal[n]['hfss'][:,0,0]
				elif len(data1_diurnal[n][var1].shape) == 3:
					if var1 == 'uas' or var1 == 'vas':
						plotvar1[n] = np.sqrt(data1_diurnal[n]['uas'][:,0,0]**2+data1_diurnal[n]['vas'][:,0,0]**2)
					else:
						plotvar1[n] = data1_diurnal[n][var1][:,0,0]
				else:
					if var1 == 'ua' or var1 == 'va':
						plotvar1[n] = np.sqrt(data1_diurnal[n]['ua'][:,0,0,model1_lvl-1]**2+data1_diurnal[n]['va'][:,0,0,model1_lvl-1]**2)
					else:
						plotvar1[n] = data1_diurnal[n][var1][:,0,0,model1_lvl-1]


			obs1_diurnal = obs1
			obs1_diurnal = obs1_diurnal.sel(time=slice('2018-02-18','2018-02-26'))

			obs1_diurnal = obs1_diurnal[np.logical_not(np.isnan(obs1_diurnal))]
			'''
			max_value = np.amax(plotvar1[dummy1].values)  # maximum value
			min_value = np.amin(plotvar1[dummy1].values)  # maximum value
			for n in range(dummy1+1,len(names1)):
				if np.any(max_value < plotvar1[n]):  # maximum value
					max_value = np.amax(plotvar1[n].values)  # maximum value
				if np.any(min_value > plotvar1[n]):
					min_value = np.amin(plotvar1[n].values)  # minimum value

			print max_value
			print min_value

			if np.any(max_value < obs1.values):
				max_value = np.amax(obs1_diurnal.values)
			if np.any(min_value > obs1.values):
				min_value = np.amin(obs1_diurnal.values)
			max_value = np.ceil(max_value)
			min_value = np.floor(min_value)

			print max_value
			print min_value
			'''

			fig, ax = plt.subplots()
			ax.set_prop_cycle('color',['red','red','blue', 'blue', 'green','green','black', 'black', 'yellow','yellow','brown','brown','orange','orange','purple','purple','pink','pink']) #plt.cm.gist_rainbow([0,0,0.1,0.1,0.2,0.2,0.3,0.3,0.4,0.4,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1,1]))

			for n in range(dummy1,len(names1)):
				if period == 1:
#				if data1[n]['ta'][0,0,0,136]-obs['ta'][1,(n-dummy)*12] > 2:
					plt.plot(diurnal[:],plotvar1[:],linewidth=0.3,label=model1, color='black')
#				else:
#					plt.plot(data1[n]['time'][0],np.mean(plotvar1[n][1:]),'r*') #,linewidth=0.3,label='IFS', color='black')
				elif period == 2:
					try:
						if data1_diurnal[n].time.dt.hour[0] == 00:
							try:
								ax.plot(diurnal[:],plotvar1[n][:],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #model1+' - '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
								ax.plot(diurnal1[:],obs1_diurnal[(n-50)*12:24+(n-50)*12],lw=0.8,ls='--',label='_nolegend_') #'Sodankyla - '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values),linewidth=0.8,linestyle='--')
							except ValueError:
								pass
					except IndexError:
						pass
				elif period == 3:
					try:
						if data1[n].time.dt.hour[0] == 12:
							try:
								plt.plot(diurnal[:],plotvar1[n][:],linewidth=0.8,label=model1+' - '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
								plt.plot(diurnal1[:],obs1_diurnal[12+(n-51)*12:36+(n-51)*12],label='Sodankyla - '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values),linewidth=0.8,linestyle='--')
							except ValueError:
								pass
					except IndexError:
						pass
				elif period == 4:
					plt.plot(data1[n]['time'][:],plotvar1[n][:],linewidth=0.3,label=model1, color='black')


			box = ax.get_position()
			ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

#			plt.ylim([min_value,max_value])
			if period == 2:
				plt.xticks([0,3,6,9,12,15,18,21,24],['2:00','5:00','8:00','11:00','14:00','17:00','20:00','23:00','2:00'],size=8)
			else:
				plt.xticks([0,3,6,9,12,15,18,21,24],['14:00','17:00','20:00','23:00','2:00','5:00','8:00','11:00','14:00'],size=8)
#			plt.xticks(rotation=10,size=8)
			plt.yticks(size=8)
			if var1 == 'rsds' or var1 == 'rsus':
				plt.xlim([4,17])
			else:
				plt.xlim([0,24])

			plt.xlabel('Local time')
			if var1 == 'Budget':
				plt.ylabel(r'Surface energy budget [$Wm^{-2}$]')
			elif var1 == 'rsds' or var1 == 'rsus' or var1 == 'rlds' or var1 == 'rlus':
				plt.ylabel(data1[dummy1][var1].long_name+r' [$Wm^{-2}$]')
			else:
				plt.ylabel(data1[dummy1][var1].long_name+' ['+data1[dummy1][var1].units+']')

#			plt.title('Diurnal cycle of '+data1[dummy1][var1].long_name)
#			plt.axhline(y=0,lw='0.3')
			handles, labels = plt.gca().get_legend_handles_labels()
			by_label = OrderedDict(zip(labels, handles))
			plt.legend(by_label.values(), by_label.keys(),loc='center left', bbox_to_anchor=(1, 0.5),fontsize='small')
#			plt.legend()
			if no == 3:
				plt.savefig(outdir+'diurnal_'+model1.lower()+'_'+model2.lower()+'_'+var1+'_'+str(period)+'.pdf')
			elif no == 1:
				plt.savefig(outdir+'diurnal_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)
			elif no == 2:
				plt.savefig(outdir+'diurnal_'+model2.lower()+'_'+var2+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)

			plt.clf()

		'''
		if cumulate:
			short_up = {}
			short_d = {}
			long_up = {}
			long_d = {}
			hfls = {}
			hfss = {}

			tot_su = {}
			tot_sd = {}
			tot_lu = {}
			tot_ld = {}
			tot_l = {}
			tot_s = {}

			sw_net = {}
			lw_net = {}

			for n in range(dummy1,len(names1)):
#			if period == 2:
#				if data1[n].time.dt.hour[0] == 0:
				short_d[n] = np.cumsum(data1_diurnal[n]['rsds'][7::8,0,0])
				short_up[n] = np.cumsum(data1_diurnal[n]['rsus'][7::8,0,0])
				long_d[n] = np.cumsum(data1_diurnal[n]['rlds'][7::8,0,0])
				long_up[n] = np.cumsum(data1_diurnal[n]['rlus'][7::8,0,0])
				hfls[n] = np.cumsum(data1_diurnal[n]['hfls'][7::8,0,0])
				hfss[n] = np.cumsum(data1_diurnal[n]['hfss'][7::8,0,0])


			for n in range(dummy1,len(names1)):
#		if data1[n].time.dt.hour[0] == 0:
				if n == 49 or n == 50:
					tot_sd[n] = short_d[n].values
					tot_su[n] = short_up[n].values
					tot_ld[n] = long_d[n].values
					tot_lu[n] = long_up[n].values
					tot_l[n] = hfls[n].values
					tot_s[n] = hfss[n].values
				elif n > 50 and n < 66:
					print n
					tot_sd[n] = short_d[n].values + tot_sd[n-2][-1]
					tot_su[n] = short_up[n].values + tot_su[n-2][-1]
					tot_ld[n] = long_d[n].values + tot_ld[n-2][-1]
					tot_lu[n] = long_up[n].values + tot_lu[n-2][-1]
					tot_l[n] = hfls[n].values + tot_l[n-2][-1]
					tot_s[n] = hfss[n].values + tot_s[n-2][-1]

				if n > 49 and n < 66:
					sw_net[n] = tot_sd[n]-tot_su[n]
					lw_net[n] = tot_ld[n]-tot_lu[n]

			obs_diurnal = obs
			obs_diurnal = obs_diurnal.sel(time=slice('2018-02-18','2018-02-26'))

			obs_diurnal = obs_diurnal[np.logical_not(np.isnan(obs_diurnal))]


			sw_u = np.cumsum(obs_diurnal['rsus'][:])
			sw_d = np.cumsum(obs_diurnal['rsds'][:])
			lw_u = np.cumsum(obs_diurnal['rlus'][:])
			lw_d = np.cumsum(obs_diurnal['rlds'][:])
			lat = np.cumsum(obs_diurnal['hfls'][:])
			sen = np.cumsum(obs_diurnal['hfss'][:])

			net_sw = sw_d[:]-sw_u[:]
			net_lw = lw_d[:]-lw_u[:]

			for n in range(dummy1,len(names1)):
#			if period == 2:
				if data1[n].time.dt.hour[0] == 0:
					plt.plot(diurnal1,sw_net[n][:]) #,color='red')
					plt.plot(diurnal1,sw_net[n][:]+lw_net[n][:]) #, color='black')
#					plt.plot(data1[n]['time'][7::8],lw_net[n][:], color='black')
					plt.plot(diurnal1,sw_net[n][:]+lw_net[n][:]+tot_l[n]) #, color='green')
#					plt.plot(data1[n]['time'][7::8],-tot_l[n], color='green')
					plt.plot(diurnal1,sw_net[n][:]+lw_net[n][:]+tot_l[n]+tot_s[n]) #, color='blue')
#					plt.plot(data1[n]['time'][7::8],-tot_s[n], color='blue')
			plt.plot(diurnal1,net_sw[:],ls='--') #,color='red')
			plt.plot(diurnal1,net_sw[:]+net_lw[:],ls='--') #,color='black')
#			plt.plot(obs['time'][:],net_lw[:],ls='--',color='black')
			plt.plot(diurnal1,net_sw[:]+net_lw[:]+lat[:],ls='--') #,color='green')
#			plt.plot(obs['time'][:],lat[:],ls='--',color='green')
			plt.plot(diurnal1,net_sw[:]+net_lw[:]+lat[:]+sen[:],ls='--') #,color='blue')
#			plt.plot(obs['time'][:],sen[:],ls='--',color='blue')

#			plt.show()
			plt.savefig('plots/diurnal_cumulated_energy_budget_'+model1.lower()+'.pdf',bbox_inches='tight',pad_inches=0)

			plt.clf()
		'''


	if cumulate:
		short_up = {}
		short_d = {}
		long_up = {}
		long_d = {}
		hfls = {}
		hfss = {}

		tot_su = {}
		tot_sd = {}
		tot_lu = {}
		tot_ld = {}
		tot_l = {}
		tot_s = {}

		sw_net = {}
		lw_net = {}

		for n in range(dummy1,len(names1)-6):
#			if period == 2:
#				if data1[n].time.dt.hour[0] == 0:
			short_d[n] = np.cumsum(data1[n]['rsds'][7::8,0,0])
			short_up[n] = np.cumsum(data1[n]['rsus'][7::8,0,0])
			long_d[n] = np.cumsum(data1[n]['rlds'][7::8,0,0])
			long_up[n] = np.cumsum(data1[n]['rlus'][7::8,0,0])
			hfls[n] = np.cumsum(data1[n]['hfls'][7::8,0,0])
			hfss[n] = np.cumsum(data1[n]['hfss'][7::8,0,0])
			print len(short_d[n])
		for n in range(dummy1,len(names1)-6):
#		if data1[n].time.dt.hour[0] == 0:
			if n == dummy1 or n == dummy1+1:
				tot_sd[n] = short_d[n].values
				tot_su[n] = short_up[n].values
				tot_ld[n] = long_d[n].values
				tot_lu[n] = long_up[n].values
				tot_l[n] = hfls[n].values
				tot_s[n] = hfss[n].values
			else:
				tot_sd[n] = short_d[n].values + tot_sd[n-2][-1]
				tot_su[n] = short_up[n].values + tot_su[n-2][-1]
				tot_ld[n] = long_d[n].values + tot_ld[n-2][-1]
				tot_lu[n] = long_up[n].values + tot_lu[n-2][-1]
				tot_l[n] = hfls[n].values + tot_l[n-2][-1]
				tot_s[n] = hfss[n].values + tot_s[n-2][-1]
				print len(tot_sd[n])
			sw_net[n] = tot_sd[n]-tot_su[n]
			lw_net[n] = tot_ld[n]-tot_lu[n]


		sw_u = np.cumsum(obs['rsus'][:])
		sw_d = np.cumsum(obs['rsds'][:])
		lw_u = np.cumsum(obs['rlus'][:])
		lw_d = np.cumsum(obs['rlds'][:])
		lat = np.cumsum(obs['hfls'][:])
		sen = np.cumsum(obs['hfss'][:])

		net_sw = sw_d[:]-sw_u[:]
		net_lw = lw_d[:]-lw_u[:]

		for n in range(dummy1,len(names1)-6):
#			if period == 2:
			if data1[n].time.dt.hour[0] == 0:
				plt.plot(data1[n]['time'][7::8],sw_net[n][:],color='red',label='Net SW')
				plt.plot(data1[n]['time'][7::8],sw_net[n][:]+lw_net[n][:], color='blue',label='Net SW + net LW')
#				plt.plot(data1[n]['time'][7::8],lw_net[n][:], color='black')
				plt.plot(data1[n]['time'][7::8],sw_net[n][:]+lw_net[n][:]+tot_l[n], color='orange',label='Net SW + net LW + latent heat flux')
#				plt.plot(data1[n]['time'][7::8],-tot_l[n], color='green')
				plt.plot(data1[n]['time'][7::8],sw_net[n][:]+lw_net[n][:]+tot_l[n]+tot_s[n], color='purple',label='Net SW + Net LW + latent heat flux + sensible heat flux')
#				plt.plot(data1[n]['time'][7::8],-tot_s[n], color='blue')
		plt.plot(obs['time'][:],net_sw[:],ls='--',color='red')
		plt.plot(obs['time'][:],net_sw[:]+net_lw[:],ls='--',color='blue')
#		plt.plot(obs['time'][:],net_lw[:],ls='--',color='black')
		plt.plot(obs['time'][:],net_sw[:]+net_lw[:]+lat[:],ls='--',color='orange')
#		plt.plot(obs['time'][:],lat[:],ls='--',color='green')
		plt.plot(obs['time'][:],net_sw[:]+net_lw[:]+lat[:]+sen[:],ls='--',color='purple')
#		plt.plot(obs['time'][:],sen[:],ls='--',color='blue')

#		plt.show()
		plt.xticks(rotation=12, size=8)
		plt.ylabel(r'Energy [$Wm^{-2}$]')
		plt.xlabel('Time')
		plt.xlim(['2018-02-01','2018-03-29'])
		handles, labels = plt.gca().get_legend_handles_labels()
		by_label = OrderedDict(zip(labels, handles))
		plt.legend(by_label.values(), by_label.keys(),fontsize=8) #,loc='center left', bbox_to_anchor=(1, 0.5),fontsize='small')
		plt.savefig('plots/cumulated_energy_budget_'+model1.lower()+'.pdf',bbox_inches='tight',pad_inches=0)

		plt.clf()



	if cumulate:
		fig, (ax1, ax2) = plt.subplots(2,1, sharex=True, gridspec_kw=dict(height_ratios=[2,1]))
		fig.subplots_adjust(bottom=0.15)

		daily_meansw = np.empty((len(names1)))
		daily_meansw[:] = np.nan
		daily_meanlw = np.empty((len(names1)))
		daily_meanlw[:] = np.nan
		daily_meanlat = np.empty((len(names1)))
		daily_meanlat[:] = np.nan
		daily_meansen = np.empty((len(names1)))
		daily_meansen[:] = np.nan
		time = np.empty((len(names1)))
		time[:] = np.nan

		for n in range(dummy1,len(names1)):
			if data1[n].time.dt.hour[0] == 0:
#				print (n-dummy1)/2
#				print data1[n]['rsds'][:-1,0,0].resample(time='24H').mean().time
				x = data1[n]['rsds'][:,0,0].resample(time='24H').mean().values
				xu = data1[n]['rsus'][:,0,0].resample(time='24H').mean().values
				xx = data1[n]['rlds'][:,0,0].resample(time='24H').mean().values
				xxu = data1[n]['rlus'][:,0,0].resample(time='24H').mean().values
				xl = data1[n]['hfls'][:,0,0].resample(time='24H').mean().values
				xs = data1[n]['hfss'][:,0,0].resample(time='24H').mean().values
				if data1[n].time.dt.month[0] == 2:
					y = data1[n].time.dt.day[0].values
				else:
					y = data1[n].time.dt.day[0].values + 28

				daily_meansw[n] = x[0]-xu[0] # data1[n]['rsds'][:-1,0,0].resample(time='1D').mean().values
				daily_meanlw[n] = xx[0]-xxu[0] # data1[n]['rsds'][:-1,0,0].resample(time='1D').mean().values
				daily_meanlat[n] = xl[0] # data1[n]['rsds'][:-1,0,0].resample(time='1D').mean().values
				daily_meansen[n] = xs[0] # data1[n]['rsds'][:-1,0,0].resample(time='1D').mean().values
				time[n] = y
#				print time[n]

		mask = np.isnan(daily_meansw)
		mask = [not i for i in mask]
		daily_meansw = daily_meansw[mask]
		mask = np.isnan(daily_meanlw)
		mask = [not i for i in mask]
		daily_meanlw = daily_meanlw[mask]
		mask = np.isnan(daily_meanlat)
		mask = [not i for i in mask]
		daily_meanlat = daily_meanlat[mask]
		mask = np.isnan(daily_meansen)
		mask = [not i for i in mask]
		daily_meansen = daily_meansen[mask]
		mask = np.isnan(time)
		mask = [not i for i in mask]
		time = time[mask]


		ax1.plot(time,daily_meansw,color='red',label='Net SW')
		ax1.plot(time,daily_meanlw,color='blue',label='Net LW')
#		ax1.plot(time,daily_meansw,color='red',label='SW')
#		ax1.plot(time,daily_meanlw,color='blue',label='LW')
		ax1.plot(time,daily_meanlat,color='orange',label='Latent heat flux')
		ax1.plot(time,daily_meansen,color='purple',label='Sensible heat flux')
		ax2.plot(time,+daily_meanlat+daily_meansw+daily_meanlw+daily_meansen,color='black',label='Total energy')

#		plt.plot(time,daily_meanlat,color='black',label='latent')
#		plt.plot(time,daily_meansen,color='orange',label='sensible')

		time2 = np.linspace(1,59,59)

		ax1.plot(time2,obs['rsds'][:].resample(time='1D').mean()-obs['rsus'][:].resample(time='1D').mean(),ls='--',color='red')
		ax1.plot(time2,obs['rlds'][:].resample(time='1D').mean()-obs['rlus'][:].resample(time='1D').mean(),ls='--',color='blue')
		ax1.plot(time2,obs['hfls'][:].resample(time='1D').mean(),ls='--',color='orange',label='_nolabel')
		ax1.plot(time2,obs['hfss'][:].resample(time='1D').mean(),ls='--',color='purple',label='_nolabel')
#		plt.plot(time2,obs['hfls'][:].resample(time='1D').mean()+obs['rsds'][:].resample(time='1D').mean()-obs['rsus'][:].resample(time='1D').mean()+obs['rlds'][:].resample(time='1D').mean()-obs['rlus'][:].resample(time='1D').mean(),ls='--',color='black')
		ax2.plot(time2,obs['hfls'][:].resample(time='1D').mean()+obs['hfss'][:].resample(time='1D').mean()+obs['rsds'][:].resample(time='1D').mean()-obs['rsus'][:].resample(time='1D').mean()+obs['rlds'][:].resample(time='1D').mean()-obs['rlus'][:].resample(time='1D').mean(),ls='--',color='black')

#		plt.plot(time2,obs['hfls'][:].resample(time='1D').mean(),ls='--',color='black')
#		plt.plot(time2,obs['hfss'][:].resample(time='1D').mean(),ls='--',color='orange')

		ax2.set_xlim([np.amin(time2),np.amax(time2)])
		ax2.set_xlabel('Time')
		ax1.set_ylabel(r'Energy [$Wm^{-2}$]')
		ax1.yaxis.set_label_coords(-0.08,0.0)

		plt.xticks([5,15,25,35,45,55],['2018-02-05','2018-02-15','2018-02-25','2018-03-07','2018-03-17','2018-03-27'],rotation=12,size=8)
		ax1.legend()
		ax2.legend()
		plt.subplots_adjust(hspace=.0)

		print np.sum(daily_meansw[:]-(obs['rsds'][:].resample(time='1D').mean()-obs['rsus'][:].resample(time='1D').mean()))
		print ' '
		print np.sum(daily_meanlw[:]-(obs['rlds'][:].resample(time='1D').mean()-obs['rlus'][:].resample(time='1D').mean()))
		print ' '
		print np.sum(daily_meanlat[:]-(obs['hfls'][:].resample(time='1D').mean()))
		print ' '
		print np.sum(daily_meansen[:]-(obs['hfss'][:].resample(time='1D').mean()))
		print ' '
		print np.sum((daily_meansw[:]+daily_meanlw[:]+daily_meanlat[:]+daily_meansen[:])-(obs['rsds'][:].resample(time='1D').mean()-obs['rsus'][:].resample(time='1D').mean()+obs['rlds'][:].resample(time='1D').mean()-obs['rlus'][:].resample(time='1D').mean()+obs['hfls'][:].resample(time='1D').mean()+obs['hfss'][:].resample(time='1D').mean()))

#		handles, labels = plt.gca().get_legend_handles_labels()
#		by_label = OrderedDict(zip(labels, handles))
#		plt.legend(by_label.values(), by_label.keys(),loc='center left', bbox_to_anchor=(1, 0.5),fontsize='small')

#		plt.show()
		plt.savefig('plots/daily_mean_energy_'+model1.lower()+'.pdf',bbox_inches='tight',pad_inches=0)

		plt.clf()

	'''
####### Vertical profiles fro case study ########

	fig = plt.figure()
	ax = plt.subplot(111)

	ax.set_prop_cycle('color',['red','red','blue', 'blue', 'green','green','black', 'black', 'yellow','yellow','brown','brown','orange','orange','purple','purple','pink','pink']) #plt.cm.gist_rainbow([0,0,0.1,0.1,0.2,0.2,0.3,0.3,0.4,0.4,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1,1]))
#	ax.set_prop_cycle('color',plt.cm.gist_rainbow(np.linspace(0,1,10)))
#	ax.set_prop_cycle(obs_color,plt.cm.gist_rainbow(np.linspace(0,1,10)))


#	ax.set_color_cycle(['red','red','blue', 'blue', 'green','green','black', 'black', 'yellow','yellow','brown','brown','orange','orange','purple','purple','pink','pink'])



	if var1 != 'Budget':
		if len(data1[n][var1].shape) == 4:
			data1_diurnal = {}

			for n in range(dummy1,len(names1)):
				data1_diurnal[n] = data1[n]

				data1_diurnal[n] = data1_diurnal[n].sel(time=slice('2018-02-23','2018-02-23'))

			for n in range(dummy1,len(names1)):
				if var1 == 'ua' or var1 == 'va':
					plotvar1[n] = np.sqrt(data1_diurnal[n]['ua'][:,0,0,:]**2+data1_diurnal[n]['va'][:,0,0,:]**2)
				else:
					plotvar1[n] = data1_diurnal[n][var1][:,0,0,:]


			obs1_diurnal = obs
			obs1_diurnal = obs1_diurnal.sel(time=slice('2018-02-23','2018-02-23'))

			obs1_diurnal = obs1_diurnal[np.logical_not(np.isnan(obs1_diurnal))]


			if period == 1 or period == 2 or period == 3 or period == 4:
				for n in range(dummy1,len(names1)):
					if period == 1:
#						if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
						plt.plot(data1[n][var1][1,0,0,:]*3600,data1[n]['zg'][1,0,0,:]-data1[n]['orog'][0,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#						if data1[n].time.dt.hour[0] == 12:
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

					elif period == 2:
						if data1[n].time.dt.hour[0] == 00:
#							if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
							if data1[n].time.dt.month[0] == 2:
								plt.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label=str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values)+' '+str(data1[n].time.dt.year[0].values)) #'IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#								plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],c='black')

								day = str(data1[n].time.dt.day[0].values)
								month = str(data1[n].time.dt.month[0].values)
								year = str(data1[n].time.dt.year[0].values)
								if len(day) == 1:
									day = '0'+day
								if len(month) == 1:
									month = '0'+month
								days = year+month+day

								if var1 == 'ta':
									obs_plot = temp_vert[temp_vert.DATE == days]
									obs_plot.DATA_VALUE = obs_plot.DATA_VALUE+273
								elif var1 == 'ua' or var1 == 'va':
									obs_plot = wind_vert[wind_vert.DATE == days]
#									obs_plot.iloc([0,3]) = 0
#									print obs_plot.wind_vert
#									print obs_plot[-1,2]
								elif var1 == 'hur':
									obs_plot = temp_vert[temp_vert.DATE == days]
									obs_plot_temporary = dew_vert[dew_vert.DATE == days]
									obs_plot.DATA_VALUE = 100 - 5*(temp_vert[temp_vert.DATE == days].DATA_VALUE.values - obs_plot_temporary.DATA_VALUE.values)

								obs_plot = obs_plot[obs_plot.TIME == '00']
								obs_plot = obs_plot[obs_plot.ALTITUDE < 2300]
								plt.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-179,lw=0.8,ls='--',label='_nolegend_') #'obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))


					elif period == 3:
						if data1[n].time.dt.hour[0] == 12:
#							if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
							 if data1[n].time.dt.month[0] == 2:
								plt.plot(plotvar1_vert[n][0,:],xr.concat([data1[n]['zg'][0,0,0,:],data1[n]['orog'][0,0,0]],dim='level')-data1[n]['orog'][0,0,0],linewidth=0.8,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#								plt.plot(plotvar1_vert[n][0,:],data1[n]['zg'][0,0,0,:]-data1[n]['orog'][0,0,0],linewidth=0.8,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#							plt.plot(obs[obsvar][:,(n-dummy)*12],obs['height'][:],c='black')

								day = str(data1[n].time.dt.day[0].values)
								month = str(data1[n].time.dt.month[0].values)
								year = str(data1[n].time.dt.year[0].values)
								if len(day) == 1:
									day = '0'+day
								if len(month) == 1:
									month = '0'+month
								days = year+month+day

								if var1 == 'ta':
									obs_plot = temp_vert[temp_vert.DATE == days]
#									obs_plot1 = dew_vert[dew_vert.DATE == days]
									obs_plot.DATA_VALUE = obs_plot.DATA_VALUE+273
#									obs_plot1.DATA_VALUE = obs_plot1.DATA_VALUE+273
								elif var1 == 'ua' or var1 == 'va':
									obs_plot = wind_vert[wind_vert.DATE == days]
								elif var1 == 'hur':
									obs_plot = temp_vert[temp_vert.DATE == days]
									obs_plot_temporary = dew_vert[dew_vert.DATE == days]
									obs_plot.DATA_VALUE = 100 - 5*(obs_plot.DATA_VALUE.values - obs_plot_temporary.DATA_VALUE.values)
#									obs_plot = temp_vert[temp_vert.DATE == days]
#									obs_plot.DATA_VALUE = 100-5*(temp_vert[temp_vert.DATE == days].DATA_VALUE.values-dew_vert[dew_vert.DATE == days].DATA_VALUE.values)

								obs_plot = obs_plot[obs_plot.TIME == '12']
#								obs_plot1 = obs_plot1[obs_plot1.TIME == '12']
								obs_plot = obs_plot[obs_plot.ALTITUDE < 2300]
#								obs_plot1 = obs_plot1[obs_plot1.ALTITUDE < 2300]

								plt.plot(obs_plot.DATA_VALUE,obs_plot.ALTITUDE-180,lw=0.8,ls='--',label='obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))
#								plt.plot(obs_plot1.DATA_VALUE,obs_plot1.ALTITUDE-180,lw=0.8,label='obs '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))

					elif period == 4:
						if n < len(names1)-1:
							if obs[filtervar1][(n-dummy1)*12+12] < filter1 and obs[filtervar2][(n-dummy1)*12+12] < filter2:
								plt.plot(data1[n][var1][1,0,0,:]*3600,data1[n]['zg'][0,0,0,:]-data1[n]['orog'][0,0,0],linewidth=0.3,label='IFS '+str(data1[n].time.dt.day[0].values)+'/'+str(data1[n].time.dt.month[0].values))


#####			This block is to calculate values for xlim ######
				max_value = np.amax(plotvar1_vert[dummy1].values)  # maximum value
				min_value = np.amin(plotvar1_vert[dummy1].values)  # maximum value
				for n in range(dummy1+1,len(names1)):
					if np.any(max_value < plotvar1_vert[n].values):  # maximum value
						max_value = np.amax(plotvar1_vert[n][:,100:].values)  # maximum value
					if np.any(min_value > plotvar1_vert[n].values):
						min_value = np.amin(plotvar1_vert[n][:,100:].values)  # minimum value
				if np.any(max_value < obs_plot.DATA_VALUE.values):  # maximum value
					max_value = np.amax(obs_plot.DATA_VALUE.values)  # maximum value
				if np.any(min_value > obs_plot.DATA_VALUE.values):
					min_value = np.amin(obs_plot.DATA_VALUE.values)  # minimum value
				max_value = np.ceil(max_value)
				min_value = np.floor(min_value)
######-------------------------------------------------------------########
				box = ax.get_position()
				ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

				plt.xlim([min_value,max_value])
				if vertical_low:
					plt.ylim([0,350])
				else:
					plt.ylim([0,2000])
				plt.xlabel(data1[dummy1][var1].units)
				plt.ylabel(data1[dummy1]['orog'].units)
#				plt.title('Vertical profile of '+data1[dummy1][var1].long_name)
				handles, labels = plt.gca().get_legend_handles_labels()
				by_label = OrderedDict(zip(labels, handles))
				plt.legend(by_label.values(), by_label.keys(),loc='center left', bbox_to_anchor=(1, 0.5),fontsize='small')
				if vertical_low:
					plt.savefig(outdir+'line_vertical_low_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)
				else:
					plt.savefig(outdir+'line_vertical_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf',bbox_inches='tight',pad_inches=0)

				plt.clf()
	'''



	return







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
#		plt.ylim([-14,14])
		plt.xticks(rotation=10,size=8)
		plt.yticks(size=8)
		plt.xlabel('Time')
		plt.ylabel(data1[dummy1][var1].units)
		plt.axhline(y=0, lw='0.8', ls='--',color='gray')
#		plt.axhline(y=5, lw='0.8', ls='--',color='gray')
#		plt.axhline(y=-5, lw='0.8', ls='--',color='gray')
#		plt.axhline(y=10, lw='0.8', ls='--',color='gray')
#		plt.axhline(y=-10, lw='0.8', ls='--',color='gray')

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
				plt.plot(data1[n]['time'][:],data1[n]['rsds'][:]-data1[n]['rsus'][:]+data1[n]['rlds'][:]-data1[n]['rlus'][:],linewidth=0.3,label=model1, color='black')
#				else:
#					plt.plot(data1[n]['time'][0],np.mean(plotvar1[n][1:]),'r*') #,linewidth=0.3,label='IFS', color='black')
			elif period == 2:
#				if n % 2 == 0:
				if data1[n].time.dt.hour[0] == 00:
					plt.plot(data1[n]['time'][:],plotvar1[n][:],linewidth=0.3,label=model1+' - '+str(data1[n].time.dt.hour[0].values), color='black')
#					ax2.plot(data1[n]['time'][start*96:end*97],data1[n]['clt'][start*96:end*97,0,0],label='IFS',linestyle=':', color='green')
			elif period == 3:
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
			plt.savefig(outdir+'line_'+model1.lower()+'_'+model2.lower()+'_'+var1+'_'+str(period)+'.pdf')
		elif no == 1:
			plt.savefig(outdir+'line_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf')
		elif no == 2:
			plt.savefig(outdir+'line_'+model2.lower()+'_'+var2+'_'+str(period)+'.pdf')

		plt.clf()





	print 'Lineplot for '+model1+' finished'

	plt.clf()


	x = rsds + rsus + rlds + rlus + hfls + hfss
