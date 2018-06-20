# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class PrediccionInterfaz(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def actualizarModelo(self,Fecha):
		pass

	@abstractmethod
	def consultarModelo(self):
		pass

	@abstractmethod
	def consultarModelo(self,param):
		pass
	


