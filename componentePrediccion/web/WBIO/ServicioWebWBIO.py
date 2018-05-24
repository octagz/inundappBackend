# -*- coding: utf-8 -*-
import __init__
from apiWBIOPatch import apiWBIOPatch
import claves
import time
import math
from datetime import datetime
from datetime import timedelta
from abc import ABCMeta, abstractproperty
from ServicioWeb import ServicioWeb

class ServicioWebWBIO(ServicioWeb):
	__metaclass__ = ABCMeta

	def __init__(self):
		self.api = apiWBIOPatch(claves.key_WBIO,granularity='daily',https=True)
		

	@abstractproperty
	def nombre_servicio(self):
		pass

	def obtenerServicio(self,coords,Fecha=None):
		hoy = datetime.today().date()
		if Fecha is None:
			self.fecha = hoy
		else:
			self.fecha= Fecha.date()

		if self.fecha < hoy:
			#Uso de datos históricos
			fecha_fin= self.fecha+timedelta(days=1)
			weather = self.api.get_history(lat=coords[0],lon=coords[1],
										 start_date=self.fecha,
										 end_date=fecha_fin)
		else:
			#Uso de forecast
			weather = self.api.get_forecast(lat=coords[0],lon=coords[1])
			
		series = weather.get_series([self.nombre_servicio()])
		encontro = False
		for dia in series:
			if(dia['datetime'].date() == self.fecha):
				precipitacion = dia[self.nombre_servicio()]
				encontro = True
				break

		if encontro:
			#Si no tengo disponible el dato en esa ubicación, consulto a la estación mas cercana
			if precipitacion is None:
				precipitacion = self._solicitudAuxiliar(weather,fecha_fin)
			return precipitacion
		else:
			return -1

	#Si no tengo disponible el dato en esa ubicación, consulto a la estación mas cercana
	def _solicitudAuxiliar(self,weather,fecha_fin):
		ciudad = weather.city_name
		pais = weather.country_code
		weather = self.api.get_history(country=pais, city=ciudad,
										 start_date=self.fecha,
										 end_date=fecha_fin)
		series = weather.get_series([self.nombre_servicio()])
		return series[0][self.nombre_servicio()]

