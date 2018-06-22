# -*- coding: utf-8 -*-
import sys
import copy
import __init__
from AdminModelo import AdminModelo
from AdaptadorScikitSVM import AdaptadorScikitSVM
from AdaptadorScikitSGD import AdaptadorScikitSGD
from PrediccionImp import PrediccionImp


class MLCore:
	
	def __init__(self):
		self.adminModelo = AdminModelo()
		self.modeloML = AdaptadorScikitSVM()

		idDataset = self.adminModelo.generarDataset(Path='entren.csv')
		datasetEntr = self.adminModelo.obtenerDataset(idDataset)

		#self.modeloML.entrenar(datasetEntr)
		#self.prediccion = PrediccionImp(self.adminModelo,self.modeloML)

	def testDataset(self,PathEntre, PathTest):
		idDataEntrenamiento = self.adminModelo.generarDataset(Path=PathEntre)
		idDataTest = self.adminModelo.generarDataset(Path=PathTest)

		modeloEspecifico = AdaptadorScikitSVM()

		modeloEspecifico.entrenar(self.adminModelo.obtenerDataset(idDataEntrenamiento))
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

		print float(efic)





def main():
	mlCore = MLCore()
	mlCore.testDataset(PathEntre='entren.csv',PathTest='datasetEntrenamiento.csv')


if __name__ == "__main__" : main()