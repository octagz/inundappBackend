# -*- coding: utf-8 -*-
import pandas as pd

#El csv tiene que tener encabezado con los nombres de los atributos
def encontrarValor(lat,lon,recurso,feature):
	#Conversión a formato QGis
	lat = lat * 100000
	lon = lon * 100000
	df = pd.read_csv('recursos/'+recurso,delim_whitespace=True)

	distanciaLat = ( df['Latitud'][1]-df['Latitud'][0] ) / 2.0

	qLong = df.query('Latitud =='+str(df['Latitud'][0]))
	distanciaLon = (qLong[1:2].iloc[0]['Longitud'] - qLong[2:3].iloc[0]['Longitud'] ) /2.0 

	q = df.query('Latitud >='+str(lat-distanciaLat)+' and Latitud <'+str(lat+distanciaLat)+' and Longitud >='+str(lon-distanciaLon)+' and Longitud <'+str(lon+distanciaLon))

	if q.empty:
		return None
	else:
		return q.iloc[0][feature]

print encontrarValor(38.419382,59.406622,'test.xyz','Poblacion')