# -*- coding: utf-8 -*-

import numpy as np 
from MLInterfaz import MLInterfaz
from sklearn import preprocessing
from sklearn.linear_model import SGDClassifier
import pandas as pd 

class AdaptadorScikitSGD(MLInterfaz):


	def __init__(self, feature='hayInundacion'):
		self.feature = feature

	#Tiene que incluir la columna del feature a predecir
	def entrenar(self,dataset,loss="hinge",penalty="12"):
		dataset = dataset.reindex(np.random.permutation(dataset.index))
		X,y = self._prepararDataset(dataset)

		clf = SGDClassifier(loss=loss,penalty=penalty)

		clf.fit(X,y)
		self.clasificador = clf

	#Sci kit no provee SVM incremental.
	def entrenarIncremental(dataset):
		pass
		

	def consultarModelo(dataset):
		if(self.clasificador is None):
			rise_exception("No se ha entrenado previamente")
		
		rta = self.clasificador.predict(dataset)
		return rta
