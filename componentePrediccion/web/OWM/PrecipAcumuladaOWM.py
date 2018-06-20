# -*- coding: utf-8 -*-
from ServicioWebOWM import ServicioWebOWM
from datetime import datetime 
import time

class PrecipAcumuladaOWM(ServicioWebOWM):

	def obtenerServicio(self,coords,Fecha=None):
		return super(PrecipAcumuladaOWM,self).obtenerServicio(Fecha=Fecha,coords=coords)


	#Precipitaciones acumuladas del dia
	def obtenerValor(self, weather):
		try:
			suma = weather.get_rain()['3h']
		except:
			#Asume que si no tenes valor 3h, no llovió
			suma = 0
			pass
		return suma

	#El periodo es desde 3 dias atrás hasta hoy(No inclusivo)
	def enPeriodo(self,weather):
		timestampApi = weather.get_reference_time()-10800 #Correción uso horario
		ts = time.mktime(self.fecha.timetuple())
		dia = 60*60*24
		return timestampApi<ts and timestampApi>ts-dia*3

#s = PrecipAcumuladaOWM()
#print('Precipitacion acumulada de los 3 dias anteriores: ',s.obtenerServicio(Fecha=datetime(2018,6,15,12,0), coords=[-37.8756344,-61.3618317]))