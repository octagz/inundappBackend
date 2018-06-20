# -*- coding: utf-8 -*-

import numpy as np 
from MLInterfaz import MLInterfaz
from sklearn import svm, preprocessing
import pandas as pd 

#Este adaptador asume recibir un dataset con pandas
class AdaptadorScikitSVM(MLInterfaz):


	def __init__(self, feature='hayInundacion'):
		self.feature = feature

	#Tiene que incluir la columna del feature a predecir
	def entrenar(self,dataset,kernel="rbf",C=1.0):

		data = dataset.obtenerDatos() #Obtengo el pandas de la abstracción
		data = data.reindex(np.random.permutation(data.index))
		data = data.iloc[0:20000]
		X,y = self._prepararDataset(data)

		clf = svm.SVC(kernel=kernel,C=C,cache_size=1000,verbose=True)
		print("Entrenando...")
		clf.fit(X,y)
		print("Fin Entrenamiento.")
		print("SCORE:")
		print clf.score(X,y)

		self.clasificador = clf

	#Sci kit no provee SVM incremental.
	def entrenarIncremental(self,dataset):
		pass
		
	#El dataset no tiene la columna 'hayInundacion'
	#Normaliza los datos de consulta
	def consultarModelo(self,dataset):
		if(self.clasificador is None):
			rise_exception("No se ha entrenado previamente")
		
		dataset = dataset.obtenerDatos()
		X = preprocessing.scale(dataset.loc[:,dataset.columns!=self.feature])
		rta = self.clasificador.predict(X)
		return rta
