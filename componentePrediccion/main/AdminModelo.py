# -*- coding: utf-8 -*-
#Tendría que usar DatasetI En lugar de Dataset para que no depende de uno
#en específico
import __init__
import pandas as pd
from Dataset import Dataset


class AdminModelo:

	#El feature a predecir siempre va a ser si hay inundación o no
	def __init__(self):
		self.datasetMapeo = []
		self.nro = 0
		self.pathDefault = "recursos/grilla.csv"
		pass

	def generarDataset(self,Path=None):
		if Path is None:
			self.datasetMapeo.append(Dataset())
		else:
			self.datasetMapeo.append(Dataset(Path))
		indice = self.nro
		self.nro = self.nro+1
		return indice

	def obtenerDataset(self,Id):
		return self.datasetMapeo[Id]

	#Devuelve un dataset para consultar al algoritmo de ML sin la columna
	#de si hay inundación
	def generarDatasetConsulta(self,Fecha, Path=None):
		if(Path is None):
			d = Dataset(self.pathDefault)
		else:
			d = Dataset(Path)

		d.completarDataset(Fecha=Fecha)
		#Antes de eliminar duplicados, se debería guardar los valores de las variables dinámicas para luego
		#reconstruir.
		d.eliminarDuplicados()
		
		return d
		
	#Es parte del mecanismo de retroalimentación. Obtiene las últimas entradas
	#desde esa fecha hasta hoy. Si no hay nada para retroalimentar, devuelve None.
	def generarDatasetEntrenamiento(self,Fecha):
		d = Dataset()
		d.actualizarModelo(Fecha=Fecha)
		cantEntradas = d.obtenerCantidad()
		if cantEntradas==0:
			return None
		indices = range(cantEntradas)
		columnaHayInundacion = pd.Dataframe(columns=['hayInundacion'],index=indices)
		d.agregarFeature(columnaHayInundacion)
		return d