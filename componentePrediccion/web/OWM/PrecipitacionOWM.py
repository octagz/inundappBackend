# -*- coding: utf-8 -*-
from ServicioWebOWM import ServicioWebOWM
from datetime import datetime 
class PrecipitacionOWM(ServicioWebOWM):

	def obtenerServicio(self,coords,Fecha=None):
		return super(PrecipitacionOWM,self).obtenerServicio(Fecha=Fecha,coords=coords)

	#Precipitaciones acumuladas del dia
	def obtenerValor(self, weather):
		try:
			suma = weather.get_rain()['3h']
		except:
			#Asume que si no tenes valor 3h, no llovió
			suma = 0
			pass
		return suma
	
s = PrecipitacionOWM()
print('Precipitacion acumulada del dia',s.obtenerServicio(Fecha=datetime(2018,5,28,0,0), coords=[-37.8756344,-61.3618317]))