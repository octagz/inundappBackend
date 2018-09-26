# -*- coding: utf-8 -*-
import __init__
from abc import ABCMeta, abstractmethod
from Grilla import Grilla

class DatasetI(object):
	__metaclass__ = ABCMeta
	
	def __init__(self,path):
		self.path = path
		#self.zonaCobertura = Grilla()

	@abstractmethod
	def actualizarModelo(self,Fecha):
		pass

	@abstractmethod
	def agregarFila(self,filas):
		pass

	@abstractmethod
	def agregarFeature(self,feature):
		pass

	@abstractmethod
	def borrarFeature(self,feature):
		pass

	@abstractmethod
	def completarDataset(self,Fecha):
		pass
