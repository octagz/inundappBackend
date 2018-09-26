# -*- coding: utf-8 -*-
import os
from Dataset import Dataset

class ResultadoPrediccion:

	def __init__(self, Dataset):
		self.modelo = Dataset
		self.pathSalida = os.path.abspath(os.path.dirname('../modelo/recursos/'))


	#Se encarga de formatear el dataset
	def obtenerResultado(self):
		dfSalida = self.modelo.obtenerDatos()

		try:
			dfSalida = dfSalida[['Latitud','Longitud','hayInundacion']]
		except (Exception):
			print "No pudieron extraerse columnas innecesarias."

		dfSalida.to_csv(self.pathSalida+'/salida.csv',index=False)
		print "Archivo generado con éxito."

	def obtenerSoloPositivos(self):
		dfSalida = self.modelo.obtenerDatos()
		try:
			dfSalida = dfSalida[['Latitud','Longitud','hayInundacion']]
		except (Exception):
			print "No pudieron extraerse columnas innecesarias."

		dfSalida = dfSalida.loc[dfSalida['hayInundacion']==1]

		dfSalida.to_csv(self.pathSalida+'/salidaSoloPositivos.csv',index=False)