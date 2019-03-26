import numpy as np
import pandas as pd
import xarray as xr
import os
import matplotlib.pyplot as plt
from collections import OrderedDict

def plot(model1,model2,site,var1,var2,obsvar,data1,data2,obs,names1,names2,model1_lvl,model2_lvl,obs_lvl,outdir,period,no,dummy1,dummy2,filtervar1,filtervar2,filter1,filter2,filterby,no_filters):

	if outdir[-1] != '/':
		outdir = outdir + '/'

	if not os.path.isdir(outdir):
		os.makedirs(outdir)

	plotvar1 = {}
	plotvar2 = {}

	for n in range(dummy1,len(names1)):
		try:
			if len(data1[n][var1].shape) == 3:
				plotvar1[n] = data1[n][var1][:,0,0]
			else:
				plotvar1[n] = data1[n][var1][:,0,0,model1_lvl-1]
		except KeyError:
			print 'Error: There is no entry number '+str(n)+' in the data'

	if no == 2:
		for n in range(dummy2,len(names2)):
			try:
				if len(data2[n][var2].shape) == 2:
					plotvar2[n] = data2[n][var2][:,model2_lvl-1]
				else:
					plotvar2[n] = data2[n][var2][:]
			except KeyError:
				print 'Error: There is no entry number '+str(n)+' in the data'


	if len(obs[obsvar].shape) == 1:
		obs[obsvar] = obs[obsvar][:]
	else:
		obs[obsvar] = obs[obsvar][obs_lvl-1,:]

	obs1 = obs[obsvar]

#	models1 = []
	for n in range(dummy1, len(names1)):
		if no_filters == 1:
			if filterby == 'obs':
				if period == 1:
					if obs[filtervar1][(n-dummy1)*12] < filter1:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
					else:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
				elif period == 2:
					if n % 2 == 0:
						if obs[filtervar1][(n-dummy1)*12] < filter1:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
				elif period == 3:
					if n % 2 == 1:
						if obs[filtervar1][(n-dummy1)*12] < filter1:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
				elif period == 4:
					if n < len(names1)-1:
						if obs[filtervar1][(n-dummy1)*12+12] < filter1:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='red')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='green')
			else:
				if period == 1:
					if data1[n][filtervar1][0,0,0] < filter1:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
					else:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
				elif period == 2:
					if n % 2 == 0:
						if data1[n][filtervar1][0,0,0] < filter1:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
				elif period == 3:
					if n % 2 == 1:
						if data1[n][filtervar1][0,0,0] < filter1:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
				elif period == 4:
					if n < len(names1)-1:
						if data1[n][filtervar1][0,0,0] < filter1:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='red')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='green')
		else:
			if filterby == 'obs':
				if period == 1:
					if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=6,marker='*',color='red')
					elif obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] > filter2:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=12,marker='*',color='red')
					elif obs[filtervar1][(n-dummy1)*12] > filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=6,marker='o',color='red')
					else:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=12,marker='o',color='red')
				elif period == 2:
					if data1[n].time.dt.hour[0] == 0:
						if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='o',color='red',label=model1+' - 00 run - Clear and calm')
						elif obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] > filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='v',color='red',label=model1+' - 00 run - Clear and windy')
						elif obs[filtervar1][(n-dummy1)*12] > filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='^',color='black',label=model1+' - 00 run - Cloudy and calm')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='s',color='black',label=model1+' - 00 run - Cloudy and windy')
				elif period == 3:
					if data1[n].time.dt.hour[0] == 12:
						if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='o',color='black',label=model1+' 12 - Clear and calm')
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='o',color='red',label=model1+' - 12 run - Clear and calm')
						elif obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] > filter2:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='v',color='black',label=model1+' 12 - Clear and windy')
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='v',color='red',label=model1+' - 12 run - Clear and windy')
						elif obs[filtervar1][(n-dummy1)*12] > filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='^',color='black',label=model1+' 12 - Cloudy and calm')
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='^',color='black',label=model1+' - 12 run - Cloudy and calm')
						else:
#							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='s',color='black',label=model1+' 12 - Cloudy and windy')
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=16,marker='s',color='black',label=model1+' - 12 run - Cloudy and windy')
				elif period == 4:
					if n < len(names1)-1:
						if obs[filtervar1][(n-dummy1)*12+12] < filter1 and obs[filtervar2][(n-dummy1)*12+12] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='red')
						elif obs[filtervar1][(n-dummy1)*12+12] < filter1 and obs[filtervar2][(n-dummy1)*12+12] > filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=8,marker='o',color='red')
						elif obs[filtervar1][(n-dummy1)*12+12] > filter1 and obs[filtervar2][(n-dummy1)*12+12] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='green')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=8,marker='o',color='green')
			else:
				if period == 1:
					if data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] < filter2:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
					elif data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] > filter2:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=8,marker='o',color='red')
					elif data1[n][filtervar1][0,0,0] > filter1 and data1[n][filtervar2][0,0,0] < filter2:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
					else:
						plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=8,marker='o',color='green')
				elif period == 2:
					if n % 2 == 0:
						if data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
						elif data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] > filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='*',color='red')
						elif data1[n][filtervar1][0,0,0] > filter1 and data1[n][filtervar2][0,0,0] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='*',color='green')
				elif period == 3:
					if n % 2 == 1:
						if data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
						elif data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] > filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='*',color='red')
						elif data1[n][filtervar1][0,0,0] > filter1 and data1[n][filtervar2][0,0,0] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='*',color='green')
				elif period == 4:
					if n < len(names1)-1:
						if data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='red')
						elif data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] > filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=8,marker='o',color='red')
						elif data1[n][filtervar1][0,0,0] > filter1 and data1[n][filtervar2][0,0,0] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='green')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=8,marker='o',color='green')

#	if period == 1 or period == 2 or period == 3 or period == 4:
#		handles, labels = plt.gca().get_legend_handles_labels()
#		by_label = OrderedDict(zip(labels, handles))
#		legend1 = plt.legend(by_label.values(), by_label.keys(),loc=2)
	if no == 2:
#		models2 = []
		for n in range(dummy2, len(names2)):
			if no_filters == 1:
				if filterby == 'obs':
					if period == 1:
						if obs[filtervar1][(n-dummy1)*12] < filter1:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
					elif period == 2:
						if n % 2 == 0:
							if obs[filtervar1][(n-dummy1)*12] < filter1:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
							else:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
					elif period == 3:
						if n % 2 == 1:
							if obs[filtervar1][(n-dummy1)*12] < filter1:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
							else:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
					elif period == 4:
						if n < len(names1)-1:
							if obs[filtervar1][(n-dummy1)*12+12] < filter1:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='red')
							else:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='green')
				else:
					if period == 1:
						if data1[n][filtervar1][0,0,0] < filter1:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
					elif period == 2:
						if n % 2 == 0:
							if data1[n][filtervar1][0,0,0] < filter1:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
							else:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
					elif period == 3:
						if n % 2 == 1:
							if data1[n][filtervar1][0,0,0] < filter1:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
							else:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
					elif period == 4:
						if n < len(names1)-1:
							if data1[n][filtervar1][0,0,0] < filter1:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='red')
							else:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='green')
			else:
				if filterby == 'obs':
					if period == 1:
						if obs[filtervar1][(n-dummy2)*12] < filter1 and obs[filtervar2][(n-dummy2)*12] < filter2:
							plt.scatter(plotvar2[n][0],obs1[(n-dummy2)*12],s=4,marker='*',color='red')
						elif obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] > filter2:
							plt.scatter(plotvar2[n][0],obs1[(n-dummy2)*12],s=8,marker='*',color='red')
						elif obs[filtervar1][(n-dummy1)*12] > filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
							plt.scatter(plotvar2[n][0],obs1[(n-dummy2)*12],s=4,marker='*',color='green')
						else:
							plt.scatter(plotvar2[n][0],obs1[(n-dummy2)*12],s=8,marker='*',color='green')
					elif period == 2:
						if n % 2 == 0:
							if obs[filtervar1][(n-dummy2)*12] < filter1 and obs[filtervar2][(n-dummy2)*12] < filter2:
								plt.scatter(plotvar2[n][0],obs1[(n-dummy2)*12],s=6,marker='^',color='green',label=model2+' 2')
							elif obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] > filter2:
								plt.scatter(plotvar2[n][0],obs1[(n-dummy2)*12],s=20,marker='v',color='green',label=model2+' 1a')
							elif obs[filtervar1][(n-dummy1)*12] > filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
								plt.scatter(plotvar2[n][0],obs1[(n-dummy2)*12],s=6,marker='>',color='green',label=model2+' 1b')
							else:
								plt.scatter(plotvar2[n][0],obs1[(n-dummy2)*12],s=20,marker='<',color='green',label=model2+' 0')
					elif period == 3:
						if n % 2 == 1:
							if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
							elif obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] > filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='*',color='red')
							elif obs[filtervar1][(n-dummy1)*12] > filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
							else:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='*',color='green')
					elif period == 4:
						if n < len(names1)-1:
							if obs[filtervar1][(n-dummy1)*12+12] < filter1 and obs[filtervar2][(n-dummy1)*12+12] < filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='red')
							elif obs[filtervar1][(n-dummy1)*12+12] < filter1 and obs[filtervar2][(n-dummy1)*12+12] > filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=8,marker='o',color='red')
							elif obs[filtervar1][(n-dummy1)*12+12] > filter1 and obs[filtervar2][(n-dummy1)*12+12] < filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='green')
							else:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=8,marker='o',color='green')
				else:
					if period == 1:
						if data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
						elif data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] > filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=8,marker='o',color='red')
						elif data1[n][filtervar1][0,0,0] > filter1 and data1[n][filtervar2][0,0,0] < filter2:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
						else:
							plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=8,marker='o',color='green')
					elif period == 2:
						if n % 2 == 0:
							if data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] < filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
							elif data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] > filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='*',color='red')
							elif data1[n][filtervar1][0,0,0] > filter1 and data1[n][filtervar2][0,0,0] < filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
							else:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='*',color='green')
					elif period == 3:
						if n % 2 == 1:
							if data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] < filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
							elif data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] > filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='*',color='red')
							elif data1[n][filtervar1][0,0,0] > filter1 and data1[n][filtervar2][0,0,0] < filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
							else:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12],s=4,marker='*',color='green')
					elif period == 4:
						if n < len(names1)-1:
							if data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] < filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='red')
							elif data1[n][filtervar1][0,0,0] < filter1 and data1[n][filtervar2][0,0,0] > filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=8,marker='o',color='red')
							elif data1[n][filtervar1][0,0,0] > filter1 and data1[n][filtervar2][0,0,0] < filter2:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=4,marker='o',color='green')
							else:
								plt.scatter(plotvar1[n][0],obs1[(n-dummy1)*12+12],s=8,marker='o',color='green')

	if period == 1 or period == 2 or period == 3 or period == 4:
		plt.axis('scaled')
		plt.xlim([240,275])
		plt.ylim([240,275])
#		plt.plot([240,275], [240,275], ls="--", c=".3")
		plt.plot([240+np.std(obs['Topen'][:]-obs['Tforest'][:])+(0.176-0.0028*(240-273)),275], [240,275-np.std(obs['Topen'][:]-obs['Tforest'][:])-(0.176-0.0028*(275-273))], ls="--",lw=0.8, c='orange',label='Measurement variation')
		plt.plot([240,275-np.std(obs['Topen'][:]-obs['Tforest'][:])-(0.176-0.0028*(275-273))], [240+np.std(obs['Topen'][:]-obs['Tforest'][:])+(0.176-0.0028*(240-273)),275], ls="--",lw=0.8, c='orange')
		plt.plot([245,275], [240,270], ls="--",lw=0.3, c='red')
		plt.plot([240,270], [245,275], ls="--",lw=0.3, c='red')
		plt.plot([250,275], [240,265], ls="--",lw=0.3, c='red')
		plt.plot([240,265], [250,275], ls="--",lw=0.3, c='red')
		plt.plot([255,275], [240,260], ls="--",lw=0.3, c='red')
		plt.plot([240,260], [255,275], ls="--",lw=0.3, c='red')

#		plt.legend('red o - both')
#		+-(0.176 - 0.0028 * temperature) C

		handles, labels = plt.gca().get_legend_handles_labels()
		by_label = OrderedDict(zip(labels, handles))
		plt.legend(by_label.values(), by_label.keys(),fontsize=6)
#		if no == 2:
#			handles, labels = plt.gca().get_legend_handles_labels(models2)
#			by_label = OrderedDict(zip(labels, handles))
#			legend2 = plt.legend(by_label.values(), by_label.keys())

#		plt.gca().add_artist(legend1)
		plt.xlabel(r'Model data ['+data1[dummy1][var1].units+']')
		plt.ylabel('Observations ['+data1[dummy1][var1].units+']')
		plt.title('Initial '+data1[dummy1][var1].long_name.lower()+' filtered by clouds and wind')
		if no == 2:
			plt.savefig(outdir+'scatter_first_'+model1.lower()+'_'+model2.lower()+'_'+var1+'_'+str(period)+'.pdf')
		else:
			plt.savefig(outdir+'scatter_first_'+model1.lower()+'_'+var1+'_'+str(period)+'.pdf')

		plt.clf()

	for n in range(dummy1, len(names1)):
		if period == 1:
			if obs[filtervar1][(n-dummy1)*12+12] < filter1 and obs[filtervar2][(n-dummy1)*12+12] < filter2:
				plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12+12],s=4,marker='o',color='red')
			elif obs[filtervar1][(n-dummy1)*12+12] < filter1 and obs[filtervar2][(n-dummy1)*12+12] > filter2:
				plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12+12],s=8,marker='o',color='red')
			elif obs[filtervar1][(n-dummy1)*12+12] > filter1 and obs[filtervar2][(n-dummy1)*12+12] < filter2:
				plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12+12],s=4,marker='o',color='green')
			else:
				plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12+12],s=8,marker='o',color='green')

		elif period == 2:
			if n % 2 == 0:
				if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
				elif obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] > filter2:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12],s=8,marker='o',color='red')
				elif obs[filtervar1][(n-dummy1)*12] > filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
				else:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12],s=8,marker='o',color='green')
		elif period == 3:
			if n % 2 == 1:
				if obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12],s=4,marker='o',color='red')
				elif obs[filtervar1][(n-dummy1)*12] < filter1 and obs[filtervar2][(n-dummy1)*12] > filter2:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12],s=8,marker='o',color='red')
				elif obs[filtervar1][(n-dummy1)*12] > filter1 and obs[filtervar2][(n-dummy1)*12] < filter2:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12],s=4,marker='o',color='green')
				else:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12],s=8,marker='o',color='green')
		elif period == 4:
			if n < len(names1)-1:
				if obs[filtervar1][(n-dummy1)*12+24] < filter1 and obs[filtervar2][(n-dummy1)*12+24] < filter2:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12+24],s=4,marker='o',color='red')
				elif obs[filtervar1][(n-dummy1)*12+24] < filter1 and obs[filtervar2][(n-dummy1)*12+24] > filter2:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12+24],s=8,marker='o',color='red')
				elif obs[filtervar1][(n-dummy1)*12+24] > filter1 and obs[filtervar2][(n-dummy1)*12+24] < filter2:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12+24],s=4,marker='o',color='green')
				else:
					plt.scatter(plotvar1[n][-1],obs1[(n-dummy1)*12+24],s=8,marker='o',color='green')


	if period == 1 or period == 2 or period == 3 or period == 4:
		plt.axis('scaled')
		plt.xlim([240,275])
		plt.ylim([240,275])
#		plt.plot([240,275], [240,275], ls="--", c=".3")
		plt.plot([240+np.std(obs['Topen'][:]-obs['Tforest'][:])+(0.176-0.0028*(240-273)),275], [240,275-np.std(obs['Topen'][:]-obs['Tforest'][:])-(0.176-0.0028*(275-273))], ls="--",lw=0.8, c='orange')
		plt.plot([240,275-np.std(obs['Topen'][:]-obs['Tforest'][:])-(0.176-0.0028*(275-273))], [240+np.std(obs['Topen'][:]-obs['Tforest'][:])+(0.176-0.0028*(240-273)),275], ls="--",lw=0.8, c='orange')
		plt.plot([243,275], [240,272], ls="--",lw=0.3, c='red')
		plt.plot([240,272], [243,275], ls="--",lw=0.3, c='red')
		plt.plot([246,275], [240,269], ls="--",lw=0.3, c='red')
		plt.plot([240,269], [246,275], ls="--",lw=0.3, c='red')
		plt.plot([249,275], [240,266], ls="--",lw=0.3, c='red')
		plt.plot([240,266], [249,275], ls="--",lw=0.3, c='red')

#		plt.legend('red o - both')
#		+-(0.176 - 0.0028 * temperature) C

		plt.xlabel('Model data ['+data1[dummy1][var1].units+']')
		plt.ylabel('Observations ['+data1[dummy1][var1].units+']')
		plt.title(data1[dummy1][var1].long_name+' filtered by clouds and wind')
		plt.savefig(outdir+'scatter_last_'+model1+'_'+var1+'_'+str(period)+'.pdf')

		plt.clf()


	print 'Scatterplot for '+model1+' finished'


	return
