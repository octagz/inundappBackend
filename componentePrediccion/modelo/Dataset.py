# -*- coding: utf-8 -*-

import abc
from DatasetI import DatasetI
import pandas as pd

#Librería utilizada: Pandas
#Escala: 1:50000
#Feature a predecir: hayInundacion
#Features utilizados: 
#	Fecha, latitud, longitud
#	Precipitacion:ServicioWebPrecipitacionOWA
#	Temperatura: ServicioWebTemperaturaOWA
class Dataset(DatasetI):
	
	def __init__(self,path=None):
		super(Dataset,self).__init__(path)
		self.escala = 1.0/50000.0
		self.featureAPredecir = 'hayInundacion'
		if self.path is None:	
			self.datos = pd.DataFrame(columns=['Fecha',
											'Latitud',
											'Longitud',
											'Precipitacion'
											'Temperatura'])
		else:
			self.datos = pd.read_csv(path)


	def actualizarModelo(self):
		pass

	def agregarFila(self,filas):
		pass

	def agregarFeature(self,feature):
		pass

	def borrarFeature(self,feature):
		pass

	def completarDataset(self):
		pass