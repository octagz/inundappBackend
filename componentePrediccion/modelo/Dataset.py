# -*- coding: utf-8 -*-
import __init__
import abc
from DatasetI import DatasetI
import pandas as pd
import nombreColumnas
from OWM.PrecipitacionOWM import PrecipitacionOWM
from OWM.TemperaturaOWM import TemperaturaOWM

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
											'Longitud'])
		else:
			self.datos = pd.read_csv(path)

		self.mapeoServicios = {nombreColumnas.tempClave:TemperaturaOWM(),
								nombreColumnas.precipClave:PrecipitacionOWM()}


	def actualizarModelo(self):
		
		pass

	#filas debe ser un dataframe pandas
	def agregarFila(self,filas):
		self.datos = pd.concat([self.datos,filas])

	#agregar columna al dataset
	#df3 = pd.DataFrame(columns=['C'])
	#Si la puedo obtener de un servicio web, feature puede ser vacio
	#Si no, feature será un dataframe de una columna completa
	def agregarFeature(self,feature):
		self.datos = pd.concat([self.datos, feature], axis=1)

	#feature es un string
	def borrarFeature(self,feature):
		self.datos.drop(columns=[feature],axis=1)

	#Considera que hay columnas que ya tienen datos cargados
	#Se fija cuales son los features dinámicos y los completa 
	#consultando a los servicios web de su mapeo
	def completarDataset(self,Fecha):
		columnas = self.datos.columns.values

		for c in columnas:reColumnas.precipC
			servicio = mapeoServicios.get(c)
			if servicio is not None:
				for index, fila in self.datos.iterrows():

					lat = fila[nombreColumnas.latClave]
					lon = fila[nombreColumnas.longClave]

					valorObtenido = servicio.obtenerServicio(Fecha=Fecha,coords=[lat,lon])

					self.datos.at[index,c] = valorObtenido




	def imprimir(self):
		print self.datos


dataset = Dataset()
dataset.imprimir()
dataset.agregarFeature(pd.DataFrame(columns=['Temperatura','Precipitacion']))
dataset.imprimir()