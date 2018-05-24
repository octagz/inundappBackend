# -*- coding: utf-8 -*-
import __init__
import pyowm
import claves
import time
import math
from datetime import datetime,timedelta
from abc import ABCMeta, abstractmethod

from ServicioWeb import ServicioWeb

class ServicioWebOWM(ServicioWeb):
	__metaclass__ = ABCMeta

	def __init__(self):
		self.owm = pyowm.OWM(claves.Key_OWM)

	def obtenerServicio(self,coords,Fecha=None):

		if Fecha is None:
			self.fecha = datetime.today()
		else:
			self.fecha= Fecha

		self.fecha.replace(hour=0, #Inicio del dia
										minute=0,
										second=0,
										microsecond=0)
		#Restricciones de la api, de hoy hasta 5 días en adelante
		if (self.fecha.date() >= datetime.today().date()) and (self.fecha.date() < datetime.today().date()+timedelta(days=5)) :
			fc = self.owm.three_hours_forecast_at_coords(coords[0],coords[1])
			forecast = fc.get_forecast()
			suma = 0;
			for weather in forecast:

				timestampApi = weather.get_reference_time()-10800
				ts = time.mktime(self.fecha.timetuple())
				dia = 60*60*24
				if(timestampApi>= ts and timestampApi<ts+dia):
					suma = suma + self.obtenerValor(weather)

			return suma
		else:
			raise Exception('Este servicio no sirve para la fecha dada')


	@abstractmethod
	def obtenerValor(self,weather):
		pass
