# -*- coding: utf-8 -*-
import __init__
from datetime import datetime,timedelta
from abc import ABCMeta, abstractmethod

from ServicioWeb import ServicioWeb

class ServicioWebOWM(ServicioWeb):
	__metaclass__ = ABCMeta

	def __init__(self,Cantidad):
		self.Cantidad = Cantidad

	def obtenerServicio(self,coords,Fecha=None):
		



		pass

