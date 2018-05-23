# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class DatasetI(object):
	__metaclass__ = ABCMeta
	
	def __init__(self,path):
		self.path=path

	@abstractmethod
	def actualizarModelo(self):
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
	def completarDataset(self):
		pass
