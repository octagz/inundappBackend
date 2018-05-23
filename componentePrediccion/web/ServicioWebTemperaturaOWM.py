# -*- coding: utf-8 -*-

import pyowm
import claves
import time
import math

from ServicioWeb import ServicioWeb

class ServicioWebTemperaturaOWM(ServicioWeb):

	def __init__(self):
		self.owm = pyowm.OWM(claves.Key_OWM)
		


	def obtenerServicio(self,coords,Fecha=None):
		if Fecha is None:
			self.fecha = math.trunc(time.time())
		else:
			self.fecha=Fecha
		print(coords)
		#punto = self.owm.weather_at_coords(coords[0],coords[1])
		#resultadoWeather = punto.get_weather(rpyfecha)
		#return resultado.get_temperature('celsius')
		fc = self.owm.three_hours_forecast('Buenos Aires,AR')
		f = fc.get_forecast()
		for weather in f:
			print(weather.get_temperature('celsius'))

		h = self.owm.weather_history_at_place('Buenos Aires,AR',
												self.fecha,
												math.trunc(time.time()))


swtemp = ServicioWebTemperaturaOWM()
swtemp.obtenerServicio(Fecha=1379090800, coords=[-37.8756344,-61.3618317])