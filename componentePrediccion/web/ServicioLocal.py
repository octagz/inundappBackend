# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import requests
import math
import time
from datetime import datetime,timedelta
from ServicioWeb import ServicioWeb

class ServicioLocal(ServicioWeb):
	__metaclass__ = ABCMeta

	def __init__(self):
		self.url = 'https://hosting.cs.uns.edu.ar/~inundapp/inundapp/web/api/eventos/'

	#No requiere coordenadas
	def obtenerServicio(self,coords=None,Fecha=None):
		try:
			data = self._sendRequest(Fecha)
		except:
			return None

		return data


	def _sendRequest(self,fecha):
		tsAnterior = math.trunc(time.mktime(fecha.timetuple()))
		tsHoy = math.trunc(time.time())
		self.url = self.url + str(tsAnterior) + '/' + str(tsHoy)
		print self.url
		result = requests.get(url = self.url, timeout=10)
		
		if result.status_code == requests.codes.ok:
			response = result.json()
			respuesta = []
			for r in response:
				nueva = {}
				if r['fenomeno'] == 'Anegamiento' or r['fenomeno'] == 'Inundacion':
					nueva['Fecha'] = r['fecha']
					nueva['Latitud'] = r['latitud']
					nueva['Longitud'] = r['longitud'] 
					respuesta.append(nueva)
		else:
			result.rise_for_status()

		return respuesta


#s = ServicioLocal()
#serv =  s.obtenerServicio(Fecha = datetime(2018,4,22,13,0,5))
#print serv