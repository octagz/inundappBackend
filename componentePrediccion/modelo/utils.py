# -*- coding: utf-8 -*-
import pandas as pd
#from qgis.core import *

#El csv tiene que tener encabezado con los nombres de los atributos
#Lo que primero varia es la latitud
def encontrarValorLatLong(lat,lon,recurso,feature):
	#Conversión a formato QGis
	lat = lat * 100000
	lon = lon * 100000

	if recurso.split('.')[1]=='xyz':
		df = pd.read_csv('recursos/'+recurso,delim_whitespace=True)
	else:
		df = pd.read_csv('recursos/'+recurso)

	distanciaLat = ( df['Latitud'][1]-df['Latitud'][0] ) / 2.0

	qLong = df.query('Latitud =='+str(df['Latitud'][0]))
	distanciaLon = (qLong[1:2].iloc[0]['Longitud'] - qLong[2:3].iloc[0]['Longitud'] ) /2.0 

	q = df.query('Latitud >='+str(lat-distanciaLat)+' and Latitud <'+str(lat+distanciaLat)+' and Longitud >='+str(lon-distanciaLon)+' and Longitud <'+str(lon+distanciaLon))

	if q.empty:
		return None
	else:
		return q.iloc[0][feature]

#Lo que primero varia es la longitud
def encontrarValorLongLat(lat,lon,recurso,feature):
	#Conversión a formato QGis
	#lat = lat * 100000
	#lon = lon * 100000

	if recurso.split('.')[1]=='xyz':
		df = pd.read_csv('recursos/'+recurso,delim_whitespace=True)
	else:
		df = pd.read_csv('recursos/'+recurso)
	
	distanciaLon = ( df['Longitud'][1]-df['Longitud'][0] ) / 2.0

	qLong = df.query('Longitud =='+str(df['Longitud'][0]))
	distanciaLat = (qLong[1:2].iloc[0]['Latitud'] - qLong[2:3].iloc[0]['Latitud'] ) /2.0 
	
	q = df.query('Longitud >='+str(lon-distanciaLon)+' and Longitud <'+str(lon+distanciaLon)+' and Latitud >='+str(lat-distanciaLat)+' and Latitud <'+str(lat+distanciaLat))

	if q.empty:
		return None
	else:
		return q.iloc[0][feature]

def unirDatos():
	df = pd.read_csv('SuelosCSV.xyz',delim_whitespace=True,names=['Latitud','Longitud','Drenaje'])
	dfPob = pd.read_csv('PoblacionCSV.xyz',delim_whitespace=True,names=['Latitud','Longitud','Poblacion'])
	df.drop(['Latitud','Longitud'],axis=1)
	dfFinal = pd.concat([dfPob,df],axis=1)
	dfFinal.round(6)
	q = dfFinal.drop(dfFinal[dfFinal.Drenaje == 0.0].index)
	q.reset_index()
	q.to_csv('SuelosyPoblacion.csv')

#print encontrarValorLongLat(-37.8763,-62.0032,'SuelosyPoblacion.csv','Poblacion')

#Obtener valores unicos
#df['Columna'].unique()
#Eliminar valores afuera del poligono
#dfSueloPulido = dfSuelo.drop(dfSuelo[dfSuelo.Drenaje==dfSuelo['Drenaje'][0].index)
#dfPobPulido = dfPoblacion.drop(dfPoblacion[dfPoblacion.Poblacion==dfPoblacion['Poblacion'][0].index)
#dfSlopePul = dfSlope.drop(dfSlope[dfSlope.Slope==dfSlope['Slope'][0].index)
#dfDeprePul = dfDepre.drop(dfDepre[dfDepre.enDepresion==dfDepre['enDepresion'][0].index)
#DSM

#Procedicmiento
#dfFinal = pd.concat([df1,df2,df3],axis=1)
#dfTest = dfTest.loc[:,~dfTest.columns.duplicated()]

#Interseccion: dfTest = drenaje.join(poblacion,how='inner',lsuffix='_caller',rsuffix='_other')

#If you have an ArcGIS Spatial Analyst license you can use 
#the tool Sample (Spatial Analyst).
# This tool creates a ZXY-ascii file from your raster file.

def pulirDataset(Path,Feature,Round,ValorARemover):
	df = pd.read_csv(Path,delim_whitespace=True,names=['Latitud','Longitud',Feature])
	dfPul = df.drop(df[df.Feature==ValorARemover].index)
	return dfPul


def generadorShape():

	qgs = QgsApplication([], False)
	qgs.initQgis()

	layer = QgsVectorLayer("/recursos/resultado.csv","grilla","ogr")
	if not layer:
		print "No cargó"

	
	defStyle = QgsStyleV2().defaultStyle()
	defaultColorRampNames = defStyle.colorRampNames()
	ramp = defStyle.colorRamp('Blues')

	renderer = QgsHeatmapRenderer()
	renderer.setRadius(10000)
	renderer.setColorRamp(ramp)
	renderer.setWeightExpression('enDepresion')
	layer.setRendererV2(renderer)

	qgs.exitQgis()

