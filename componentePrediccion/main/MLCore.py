# -*- coding: utf-8 -*-
import sys, os
import copy
import __init__
from AdminModelo import AdminModelo
from AdaptadorScikitSVM import AdaptadorScikitSVM
from AdaptadorScikitSGD import AdaptadorScikitSGD
from PrediccionImp import PrediccionImp
from ResultadoPrediccion import ResultadoPrediccion
import pandas as pd
import numpy as np

class MLCore:
	
	def __init__(self):
		self.adminModelo = AdminModelo()
		self.modeloML = AdaptadorScikitSVM()

		idDataset = self.adminModelo.generarDataset(Path='entren.csv')
		datasetEntr = self.adminModelo.obtenerDataset(idDataset)

		#self.modeloML.entrenar(datasetEntr)
		#self.prediccion = PrediccionImp(self.adminModelo,self.modeloML)

	def testDataset(self,PathEntre, PathTest=None):
		idDataEntrenamiento = self.adminModelo.generarDataset(Path=PathEntre)
		idDataTest = self.adminModelo.generarDataset(Path=PathTest)

		modeloEspecifico = AdaptadorScikitSVM()

		datasetEntrenamiento = self.adminModelo.obtenerDataset(idDataEntrenamiento)

		modeloEspecifico.entrenar(datasetEntrenamiento)
		datasetTestSinFeature = self.adminModelo.obtenerDataset(idDataTest)
		datasetTestConFeature = copy.deepcopy(datasetTestSinFeature)

		datasetTestSinFeature.borrarFeature(feature='hayInundacion')
		print("Consultando...")
		respuesta = modeloEspecifico.consultarModelo(datasetTestSinFeature)
		#Comparar la respuesta con los verdaderos valores.
		dfTest = datasetTestConFeature.obtenerDatos()
		valores = dfTest['hayInundacion'].values
		#Determinacion eficacia
		aciertos = 0
		for i,r in enumerate(respuesta):
			if (respuesta[i] == valores[i]):
				aciertos=aciertos+1
		efic = float(aciertos)  / float(len(respuesta))

		#self.adminModelo.generarDatasetConsulta(Fecha=datetime())
		print float(efic)

		datasetTestSinFeature.agregarResultados(Valores=respuesta)
		salida = ResultadoPrediccion(Dataset=datasetTestSinFeature)

		salida.obtenerResultado()

def main():
	mlCore = MLCore()
	absolute_path = os.path.abspath(os.path.dirname('../modelo/recursos/'))
	#print absolute_path
	df = pd.read_csv(absolute_path+'/'+'dataset9Julio+SinDup.csv')
	df = df.reindex(np.random.permutation(df.index))
	#df = df.drop(columns=['Poblacion','Slope','enDepresion','LluviaAcumulada','LluviaDia','Drenaje'])
	dfE = df.iloc[:-500]
	dfT = df.iloc[-500:]
	dfE.to_csv(absolute_path+'/'+'dataset9JulioE.csv',index=False)
	dfT.to_csv(absolute_path+'/'+'dataset9JulioT.csv',index=False)
	mlCore.testDataset(PathEntre='dataset9JulioE.csv',PathTest='dataset9JulioT.csv')


if __name__ == "__main__" : main()