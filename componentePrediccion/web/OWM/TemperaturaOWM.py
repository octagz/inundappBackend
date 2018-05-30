# -*- coding: utf-8 -*-
from ServicioWebOWM import ServicioWebOWM
from datetime import datetime

class TemperaturaOWM(ServicioWebOWM):


	def obtenerServicio(self,coords,Fecha=None):
		return super(TemperaturaOWM,self).obtenerServicio(Fecha=Fecha,coords=coords)

	#Temperatura promedio del día. Para hacer el promedio del dia, se suma
	#la soctava parte del valor de cada período de 3 horas.
	def obtenerValor(self, weather):
		#print('sumo: ',weather.get_temperature('celsius')['temp'], weather.get_reference_time())
		return weather.get_temperature('celsius')['temp']/8.0

#swtemp = TemperaturaOWM()
#print('Promedio del dia',swtemp.obtenerServicio(Fecha=datetime(2018,5,26,0,0), coords=[-37.8756344,-61.3618317]))