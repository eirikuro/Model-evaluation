import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import glob
import datetime as dt
from collections import defaultdict
from netCDF4 import Dataset
from itertools import compress

def readin(modeldir1,modeldir2,obsdir,site,startdate,enddate,model1,model2,period,no):


	if modeldir1[-1] != '/':
		modeldir1 = modeldir1 + '/'
	if modeldir2[-1] != '/':
		modeldir2 = modeldir2 + '/'
	if obsdir[-1] != '/':
		obsdir = obsdir + '/'

	if period == 1:
		start = 0
		end = 1
	elif period == 2:
		start = 0
		end = 2
	elif period == 3:
		start = 0
		end = 2
	elif period == 4:
		start = 1
		end = 2
	elif period == 5:
#		start1 = 0
#		end1 = 1
		start = 0
		end = 2
#		start3 = 0
#		end3 = 2
#		start4 = 1
#		end4 = 2

#	else:
#		if period == 1:
#			start = 0
#			end = 0.125
#		elif period == 2:
#			start = 0
#			end = 0.25
#		elif period == 3:
#			start = 0
#			end = 0.25
#		elif period == 4:
#			start = 0.125
#			end = 0.25
#		elif period == 5:
#			start1 = 0
#			end1 = 0.125
#			start2 = 0
#			end2 = 0.25
#			start3 = 0
#			end3 = 0.25
#			start4 = 0.125
#			end4 = 0.25



	names1 = sorted(glob.glob(modeldir1+'*.nc'))


	data1 = {}
	data2 = {}

	startd = dt.datetime.strptime(startdate, "%Y-%m-%d")
	endd = dt.datetime.strptime(enddate, "%Y-%m-%d")
	month1 = startd.month
	month2 = endd.month
	date1 = startd.date

	for n in range(len(names1)):
		data1[n] = xr.open_dataset(names1[n])

		if data1[n].time.dt.month[0] < month1 or data1[n].time.dt.month[0] > month2:
			del data1[n]
		else:
			data1[n] = data1[n].isel(time=slice(int(start*96),int(end*96)))
			data1[n] = data1[n].sel(time=slice(startdate,enddate))


	dummy1 = len(names1)-len(data1)


	print 'Finished reading in data from '+model1


	names2 = sorted(glob.glob(modeldir2+'*.nc'))

	if no == 2:

		for n in range(len(names2)):
			data2[n] = xr.open_dataset(names2[n])

			if data2[n].time.dt.month[0] < month1 or data2[n].time.dt.month[0] > month2:
				del data2[n]
			else:
				data2[n] = data2[n].isel(time=slice(int(start*12),int(end*12)))
				data2[n] = data2[n].sel(time=slice(startdate,enddate))


		print 'Finised reading in data from '+model2

	dummy2 = len(names2)-len(data2)

	name = glob.glob(obsdir+'*.nc')

#	obs = {}

#	for n in range(len(name)):
	obs = xr.open_dataset(name[0])
#	print obs['ta'].shape
	obs = obs.sel(time=slice(startdate,enddate))
#	print obs['ta'].shape
	obs['ta'] = obs['ta']+273
	obs['Topen'] = obs['Topen']+273
	obs['Tforest'] = obs['Tforest']+273
	obs['N'] = obs['N']*12.5


#	Reading observation data from radiosonde
	obs_vertical = pd.read_csv(obsdir+'luotaus_martin4.dat', delimiter='\s+', engine='python') #, encoding='latin-1'


	obs_vertical = obs_vertical[obs_vertical.DATE != '----']

#	print obs_vertical.shape

	obs_vertical = obs_vertical.stack().str.replace(',','.').unstack()

#	for i in range(1,len(obs_vertical)):
#		obs_vertical.DATA_VALUE[i] = float(obs_vertical.DATA_VALUE[i])
#		obs_vertical.ALTITUDE[i] = float(obs_vertical.ALTITUDE[i])
#		obs_vertical.PRESSURE[i] = float(obs_vertical.PRESSURE[i])
#		print i

#	temp = obs_vertical.DATA_VALUE.convert_objects(convert_numeric=True)

#	temp = pd.to_numeric(obs_vertical.DATA_VALUE)
	obs_vertical.DATA_VALUE = pd.to_numeric(obs_vertical.DATA_VALUE)
	obs_vertical.ALTITUDE = pd.to_numeric(obs_vertical.ALTITUDE)
	obs_vertical.PRESSURE = pd.to_numeric(obs_vertical.PRESSURE)

#	temp = obs_vertical.DATA_VALUE.values

#	print type(obs_vertical.DATA_VALUE[329787])


	for i in range(1,9):
		obs_vertical = obs_vertical[obs_vertical.DATE != '2018010'+str(i)]
	for i in range(10,31):
		obs_vertical = obs_vertical[obs_vertical.DATE != '201801'+str(i)]
#	print obs_vertical.shape



#	obs_vertical = obs_vertical.replace(',','.')

	wind_vert = obs_vertical[obs_vertical.PARAMETER == '332']
	winddir_vert = obs_vertical[obs_vertical.PARAMETER == '333']
	temp_vert = obs_vertical[obs_vertical.PARAMETER == '336']
	dew_vert = obs_vertical[obs_vertical.PARAMETER == '337']

#	print type(temp_vert.DATA_VALUE[329787])


#	obs_vertical_VARIABLES = obs_vertical.loc[:, ['DATE', 'TIME', 'ALTITUDE', 'PRESSURE', 'PARAMETER', 'DATA_VALUE'] ]

#	DATA_MATRIX = obs_vertical_VARIABLES.values[1:,:]

#	DATE = DATA_MATRIX[:,0]

#	DATUM = []

#	for i in range(len(DATE)):
#		if int(float(DATA_MATRIX[i,0])) > 20180200 and int(float(DATA_MATRIX[i,0])) < 20180229: # and int(float(DATA_MATRIX[i,1])) == 12: # and int(float(DATA_MATRIX[i,0])) < 20180229:
#			DATUM.append(DATA_MATRIX[i,:])

#	WIND_VELOCITY = []

#	ALTITUDE_WIND_VELOCITY = []

#	DAY = []

#	HOUR = []

#	WIND_DIRECTION = []

#	ALTITUDE_WIND_DIRECTION = []

#	TEMPERATURE = []

#	ALTITUDE_TEMPERATURE = []

#	PRESSURE_TEMPERATURE = []

#	DEWPOINT = []

#	ALTITUDE_DEWPOINT = []

#	PRESSURE_DEWPOINT = []

#	for i in range(len(DATUM)):
#		if DATUM[i][4] == str(332):
#			WIND_VELOCITY.append(DATUM[i][5].replace(',','.'))
#			ALTITUDE_WIND_VELOCITY.append(DATUM[i][2].replace(',','.'))
#			DAY.append(DATUM[i][0].replace(',','.'))
#			HOUR.append(DATUM[i][1].replace(',','.'))

#		if DATUM[i][4] == str(333):
#			WIND_DIRECTION.append(DATUM[i][5].replace(',','.'))
#			ALTITUDE_WIND_DIRECTION.append(DATUM[i][2].replace(',','.'))

#		if DATUM[i][4] == str(336):
#			TEMPERATURE.append(DATUM[i][5].replace(',','.'))
#			ALTITUDE_TEMPERATURE.append(DATUM[i][2].replace(',','.'))
#			PRESSURE_TEMPERATURE.append(DATUM[i][3].replace(',','.'))

#		if DATUM[i][4] == str(337):
#			DEWPOINT.append(DATUM[i][5].replace(',','.'))
#			ALTITUDE_DEWPOINT.append(DATUM[i][2].replace(',','.'))
#			PRESSURE_DEWPOINT.append(DATUM[i][3].replace(',','.'))

#	obs_vert = [DAY, HOUR, WIND_VELOCITY, ALTITUDE_WIND_VELOCITY, WIND_DIRECTION, ALTITUDE_WIND_DIRECTION, TEMPERATURE, ALTITUDE_TEMPERATURE, PRESSURE_TEMPERATURE, DEWPOINT, ALTITUDE_DEWPOINT, PRESSURE_DEWPOINT]

#	print obs_vert.shape

#	obs_vert = np.transpose(obs_vert)

#	print obs_vert.shape

	print 'Finished reading in data from '+site

	return data1,data2,obs,wind_vert,winddir_vert,temp_vert,dew_vert,names1,names2,dummy1,dummy2








'''
	if site[0].isupper():
		try:
			obs = xr.open_dataset('../'+obsdir+site+'_yopp.nc')
			obs = obs.sel(time=slice(startdate, enddate))
			obs['ta'] = obs['ta']+273
		except IOError:
			try:
				site = site.lower()
				obs = xr.open_dataset('../'+obsdir+site+'_yopp.nc')
				obs = obs.sel(time=slice(startdate, enddate))
				obs['ta'] = obs['ta']+273
			except IOError:
				print 'xxx'
	else:
		try:
			obs = xr.open_dataset('../'+obsdir+site+'_yopp.nc')
			obs = obs.sel(time=slice(startdate, enddate))
			obs['ta'] = obs['ta']+273
		except IOError:
			try:
				site = site.upper()
				obs = xr.open_dataset('../'+obsdir+site+'_yopp.nc')
				obs = obs.sel(time=slice(startdate, enddate))
				obs['ta'] = obs['ta']+273
			except IOError:
				print 'xxx'

	print 'Finished reading in data from '+site


	return data,data2,obs,names1,names2


########### Code to create a list holding all dates and times to use when IFS data is read in ############
	filename = []

	if sop == 1: #The list will only include dates for winter data
		for n in range(2,4):
#			if n == 1: #Filenames for January, first model data is from 24th of January
#				for m in range(24,32):
#					date = '20180'+str(n)+str(m)+'00'
#					date2 = '20180'+str(n)+str(m)+'12'
#					date = int(round(float(date)))
#					date2 = int(float(date2))
#					filename = np.append(filename,date)
#					filename = np.append(filename,date2)
			if n == 2: #Filenames for February
				for m in range(1,29):
					if m < 10:
						date = '20180'+str(n)+'0'+str(m)+'00'
						date2 = '20180'+str(n)+'0'+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
					else:
						date = '20180'+str(n)+str(m)+'00'
						date2 = '20180'+str(n)+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
			else: #Filenames for March
				for m in range(1,32):
					if m < 10:
						date = '20180'+str(n)+'0'+str(m)+'00'
						date2 = '20180'+str(n)+'0'+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
					else:
						date = '20180'+str(n)+str(m)+'00'
						date2 = '20180'+str(n)+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)

	elif sop == 2: #The list will only include dates for summerdata
		for n in range(7,10):
			if n == 7 or n == 8: #Filenames for July and August
				for m in range(1,32):
					if m < 10:
						date = '20180'+str(n)+'0'+str(m)+'00'
						date2 = '20180'+str(n)+'0'+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
					else:
						date = '20180'+str(n)+str(m)+'00'
						date2 = '20180'+str(n)+str(m)+'12'
						date = int(round(float(date)))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
			else: #Filenames for September
				for m in range(1,31):
					if m < 10:
						date = '20180'+str(n)+'0'+str(m)+'00'
						date2 = '20180'+str(n)+'0'+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
					else:
						date = '20180'+str(n)+str(m)+'00'
						date2 = '20180'+str(n)+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)

	else: # The list will include dates for both summer and winter
		for n in range(2,4):
			if n == 2: #Filenames for February
				for m in range(1,29):
					if m < 10:
						date = '20180'+str(n)+'0'+str(m)+'00'
						date2 = '20180'+str(n)+'0'+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
					else:
						date = '20180'+str(n)+str(m)+'00'
						date2 = '20180'+str(n)+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
			else: #Filenames for March
				for m in range(1,32):
					if m < 10:
						date = '20180'+str(n)+'0'+str(m)+'00'
						date2 = '20180'+str(n)+'0'+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
					else:
						date = '20180'+str(n)+str(m)+'00'
						date2 = '20180'+str(n)+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
		for n in range(7,10):
			if n == 7 or n == 8: #Filenames for July and August
				for m in range(1,32):
					if m < 10:
						date = '20180'+str(n)+'0'+str(m)+'00'
						date2 = '20180'+str(n)+'0'+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
					else:
						date = '20180'+str(n)+str(m)+'00'
						date2 = '20180'+str(n)+str(m)+'12'
						date = int(round(float(date)))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
			else: #Filenames for September
				for m in range(1,31):
					if m < 10:
						date = '20180'+str(n)+'0'+str(m)+'00'
						date2 = '20180'+str(n)+'0'+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)
					else:
						date = '20180'+str(n)+str(m)+'00'
						date2 = '20180'+str(n)+str(m)+'12'
						date = int(float(date))
						date2 = int(float(date2))
						filename = np.append(filename,date)
						filename = np.append(filename,date2)



	filename = np.int_(filename) #Formatting all numbers as integers so that there are no decimals

	modeldata = {}
#	sg = defaultdict(dict)
#	ag = defaultdict(dict)


	for n in range(len(filename)):
		if site[0].isupper():
			try:
				modeldata[n] = xr.open_dataset('../'+modeldir+site+'_'+model+'_'+str(filename[n])+'.nc')

#			data = Dataset('../'+modeldir+site+'_'+model+'_'+str(filename[n])+'.nc')
#			sg[n][0] = data.variables[var].long_name
#			sg[n][1] = data.variables[var].units
#			sg[n][2] = data.variables['lat'][:]
#			sg[n][3] = data.variables['lon'][:]
#			sg[n][4] = data.variables['time'][:x]
#			sg[n][5] = data.variables[var][:x,:,:]

#			data.close()

#			if n == 0:
#				sg[n][4] = sg[n][4]	#Creating a timeseries that starts at 0 for the first value
#			elif n % 2 != 0:
#				sg[n][4] = sg[n][4]+(n-1)*12
#			else:
#				sg[n][4] = sg[n][4]+n*12

			except IOError:
				try:
					modeldata[n] = xr.open_dataset('../'+modeldir+model+'_'+site+'_'+str(filename[n])+'.nc')

				except IOError:
					try:
						site = site.lower()
						modeldata[n] = xr.open_dataset('../'+modeldir+site+'_'+model+'_'+str(filename[n])+'.nc')

					except IOError:
						try:
							site = site.lower()
							modeldata[n] = xr.open_dataset('../'+modeldir+model+'_'+site+'_'+str(filename[n])+'.nc')

						except IOError:

							print 'Error: can\'t find file for date '+str(filename[n])
							print n

		else:
			try:
				modeldata[n] = xr.open_dataset('../'+modeldir+site+'_'+model+'_'+str(filename[n])+'.nc')

#			data = Dataset('../'+modeldir+site+'_'+model+'_'+str(filename[n])+'.nc')
#			sg[n][0] = data.variables[var].long_name
#			sg[n][1] = data.variables[var].units
#			sg[n][2] = data.variables['lat'][:]
#			sg[n][3] = data.variables['lon'][:]
#			sg[n][4] = data.variables['time'][:x]
#			sg[n][5] = data.variables[var][:x,:,:]

#			data.close()

#			if n == 0:
#				sg[n][4] = sg[n][4]	#Creating a timeseries that starts at 0 for the first value
#			elif n % 2 != 0:
#				sg[n][4] = sg[n][4]+(n-1)*12
#			else:
#				sg[n][4] = sg[n][4]+n*12

			except IOError:
				try:
					modeldata[n] = xr.open_dataset('../'+modeldir+model+'_'+site+'_'+str(filename[n])+'.nc')

				except IOError:
					try:
						site = site.upper()
						modeldata[n] = xr.open_dataset('../'+modeldir+site+'_'+model+'_'+str(filename[n])+'.nc')

					except IOError:
						try:
							site = site.upper()
							modeldata[n] = xr.open_dataset('../'+modeldir+model+'_'+site+'_'+str(filename[n])+'.nc')

						except IOError:

							print 'Error: can\'t find file for date '+str(filename[n])
							print n



	if site[0].isupper()
		try:
			obs = xr.open_dataset('../'+obsdir+site+'_yopp.nc')
			obs = obs.sel(time=slice(startdate, enddate))
			obs['ta'] = obs['ta']+273
		except IOError:
			try:
				site = site.lower()
				obs = xr.open_dataset('../'+obsdir+site+'_yopp.nc')
				obs = obs.sel(time=slice(startdate, enddate))
				obs['ta'] = obs['ta']+273
			except IOError:
				print 'xxx'
	else:
		try:
			obs = xr.open_dataset('../'+obsdir+site+'_yopp.nc')
			obs = obs.sel(time=slice(startdate, enddate))
			obs['ta'] = obs['ta']+273
		except IOError:
			try:
				site = site.upper()
				obs = xr.open_dataset('../'+obsdir+site+'_yopp.nc')
				obs = obs.sel(time=slice(startdate, enddate))
				obs['ta'] = obs['ta']+273
			except IOError:
				print 'xxx'




#	data = Dataset('../'+obsdir+site+'_yopp.nc')
#	ag[0][0] = data.variables['height'][:]
#	ag[0][1] = data.variables['time'][:]
#	ag[0][2] = data.variables[var][:]


	return modeldata, obs, filename
'''
