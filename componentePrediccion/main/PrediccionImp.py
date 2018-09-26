# -*- coding: utf-8 -*-
import __init__
import abc
from PrediccionInterfaz import PrediccionInterfaz
from ResultadoPrediccion import ResultadoPrediccion
import pandas as pd
from datetime import datetime,timedelta 

class PrediccionImp(PrediccionInterfaz):

	#Asume que modeloML está previamente entrenado
	def __init__(self, adminModelo, modeloML):
		self.adminModelo = adminModelo
		self.modeloML = modeloML


	def actualizarModelo(self,Fecha):
		dfRetroalimentacion = self.adminModelo.generarDatasetEntrenamiento(Fecha=Fecha)
		resultado = self.modeloML.entrenarIncremental(dfRetroalimentacion)


	#Consulta desde la fecha dentro de 4 días
	def consultarModelo(self):
		fecha = datetime.now()+timedelta(days=4)
		dfConsulta = self.adminModelo.generarDatasetConsulta(Fecha=fecha)
		resultado = self.modeloML.consultarModelo(dfConsulta)
		
		#Ahora dfConsulta tiene los puntos sin duplicados y el valor de hayInundacion. Hay que reconstruir el area original:
		dfConsulta.agregarResultados(Valores=resultado)

		salida = ResultadoPrediccion(dfConsulta)
		salida.obtenerResultado()


	def consultarModelo(self,args):
		pass