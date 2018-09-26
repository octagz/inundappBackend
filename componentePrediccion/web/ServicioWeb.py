# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class ServicioWeb(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def obtenerServicio(self, coords=None, Fecha=None):
		pass

