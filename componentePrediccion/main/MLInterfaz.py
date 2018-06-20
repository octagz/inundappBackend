# -*- coding: utf-8 -*-
from sklearn import preprocessing
from abc import ABCMeta, abstractmethod

class MLInterfaz(object):
	__metaclass__= ABCMeta

	@abstractmethod
	def entrenar(dataset):
		pass

	@abstractmethod
	def entrenarIncremental(dataset):
		pass

	@abstractmethod
	def consultarModelo(dataset):
		pass


	def _prepararDataset(self, dataset):
		# Me guardo en y la columna a predecir
		y = dataset[self.feature].values
		#escala el dataset sin la columna a predecir
		X = preprocessing.scale(dataset.loc[:,dataset.columns!=self.feature])
		return X,y

