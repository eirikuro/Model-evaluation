import numpy as np
import pandas as pd
import xarray as xr
import os
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

def plot(model1,model2,site,var1,var2,obsvar,obsvar2,data1,data2,obs,names1,names2,model1_lvl,model2_lvl,obs_lvl,outdir,period,no,dummy1,filtervar1,filter1,filtervar2,filter2,filterby,no_filters):

	if outdir[-1] != '/':
		outdir = outdir + '/'

	if not os.path.isdir(outdir):
		os.makedirs(outdir)

#	print data1[dummy][var1].shape
#	print data1[dummy][var1].T.shape
#	print obs[obsvar].shape
#	exit()
#	for n in range(len(filename)):
#		try:
#			modeldata[n][var] = modeldata[n][var][:,0,0,:]
#			modeldata[n][var] = modeldata[n][var].T
#			modeldata[n]['zg'] = modeldata[n]['zg'][0,0,0,:]
#		except KeyError:
#			print 'Error'

	if len(data1[dummy1][var1].shape) == 4:
		plotvar = {}
		time = {}
		zg = {}

		for n in range(dummy1,len(names1)):
			if var1 == 'tnt':
				plotvar[n] = data1[n][var1][1:]
				plotvar[n] = plotvar[n]*3600
			else:
				plotvar[n] = data1[n][var1][:]
#		plotvar[n] = plotvar[n]*3600
#		plotvar[n] = plotvar[n][1:]
#		del plotvar[n]['lat']
#		del plotvar[n]['lon']
#		time[n] = data1[n]['time'][1:]
#		zg[n] = data1[n]['zg'][1:]



		plotvar1 = plotvar[dummy1].to_series()
#	plotvar1[:,1] = plotvar[dummy][1,0,0,:].to_series()

#	print plotvar1.shape

#	time1 = time[dummy].to_series()
#	zg1 = zg[dummy].to_series()

		for n in range(dummy1+1,len(names1)):
			temp = plotvar[n].to_series()
			plotvar1 = plotvar1.append(temp)

#		temp2 = time[n].to_series()
#		time1 = time1.append(temp2)

#		temp3 = zg[n].to_series()
#		zg1 = zg1.append(temp3)

#	print plotvar1
#	print plotvar1.shape

#	hdf = aggdf.groupby(['a','b']).size()

		plotvar1 = plotvar1.groupby(['time','level']).mean()

#	del plotvar1['lat']
#	del plotvar1['lon']

#	print plotvar1

		plotvar1reset = plotvar1.reset_index()
		plotvar1reset.columns = ['time','level',var1]
		plotvar1pivot=plotvar1reset.pivot('time','level')

#	levs = [-3,-2.75,-2.5,-2.25,-2,-1.75,-1.5,-1.25,-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3]

#		levs = [240,244,248,252,256,260,264,268,272,276]

		X=plotvar1pivot.columns.levels[1].values
#	X=zg1.values #['Geopotential height']
#	print X
#	print X.shape
		Y=plotvar1pivot.index.values
#	print Y
#	print Y.shape
		Z=plotvar1pivot.values
#	print Z
#	print Z.shape
		Xi,Yi = np.meshgrid(X, Y)
		plt.contourf(Yi, Xi, Z, alpha=0.7, cmap=plt.cm.bwr, levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]) #levels=levs, cmap=plt.cm.bwr)
		plt.gca().invert_yaxis()

		plt.ylim([137,80])
		cbar=plt.colorbar()
#	cbar.ax.set_yti
#	plt.show()

		plt.axvline(x='2018-02-09',color = 'black')
		plt.axvline(x='2018-02-17',color = 'orange')
		plt.axvline(x='2018-02-24',color = 'black')
		plt.axvline(x='2018-02-27',color = 'orange')
		plt.axvline(x='2018-03-13',color = 'orange')
		plt.axvline(x='2018-03-20',color = 'orange')
		plt.axvline(x='2018-03-08',color = 'black')
		plt.axvline(x='2018-03-17',color = 'black')
		plt.axvline(x='2018-03-31',color = 'black')

		plt.savefig(outdir+'cont_'+model1.lower()+'_'+var1+'.pdf')

		plt.clf()

#	exit()

#	plt.contourf(time1,zg1,plotvar1)
#	plt.show()

#	exit()


#	for n in range(dummy,len(names1)):
#		try:
#			plt.contourf(modeldata[n]['time'][start*96:end*96],modeldata[n][var][0,0,0,:],modeldata[n][var][start*96:end*96,0,0,:].T)
#			plt.contourf(modeldata[n]['time'][start*96:end*96],modeldata[n][var][:,start*96:end*96])

#			plt.contourf(data1[n]['time'][:],data1[n][var1][0,0,0,:],data1[n][var1][:,0,0,:].T)

#			plt.contourf(data1[n]['time'][:],np.linspace(1,137,137),data1[n][var1][:,0,0,:].T)
#			plt.contourf(data1[n][var1][:,0,0,:].T)
#		except KeyError:
#			print 'Error'
#	plt.contour(obs[obsvar])
#	plt.colorbar()

	return
