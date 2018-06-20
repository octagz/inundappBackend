# -*- coding: utf-8 -*-
import __init__
import abc
from DatasetI import DatasetI
import pandas as pd
import sys,os
import nombreColumnas
from OWM.PrecipitacionOWM import PrecipitacionOWM
from OWM.TemperaturaOWM import TemperaturaOWM

from WBIO.PrecipitacionWBIO import PrecipitacionWBIO
from WBIO.TemperaturaWBIO import TemperaturaWBIO
from ServicioLocal import ServicioLocal
import utils
from datetime import datetime
#Librería utilizada: Pandas
#Escala: 1:50000
#Feature a predecir: hayInundacion
#Features utilizados: 
#	Fecha, latitud, longitud
#	Precipitacion:PrecipitacionOWM
#	Temperatura: TemperaturaOWM
class Dataset(DatasetI):
	
	#De minima el dataset tiene las columnas latitud y longitud. Luego se agregan las variables dinámicas y fijas
	def __init__(self,path=None):
		super(Dataset,self).__init__(path)
		self.escala = 1.0/50000.0

		self.mapeoServicios = {nombreColumnas.tempClave:TemperaturaWBIO(),
								nombreColumnas.precipClave:PrecipitacionWBIO()}

		self.pathVariablesFijas = 'SuelosyPoblacion.csv'
		self.variablesFijas = [nombreColumnas.drenajeClave, nombreColumnas.poblacionClave]

		if self.path is None:
			self.datos = pd.DataFrame(columns=[nombreColumnas.latClave,
												nombreColumnas.longClave])
			for key,value in self.mapeoServicios.iteritems():
				self.agregarFeature( pd.DataFrame(columns=[key]) )
			for var in self.variablesFijas:
				self.agregarFeature( pd.DataFrame(columns=[var]) )
		else:
			try:
				absolute_path = os.path.abspath(os.path.dirname('../modelo/recursos/'))
				#print absolute_path
				self.datos = pd.read_csv(absolute_path+'/'+path)
			except (Exception) as e:
				print(e)
				

		

	def obtenerDatos(self):
		return self.datos	


	#Fecha indica es la fecha de inicio del período hasta hoy
	def actualizarModelo(self,Fecha):
		
		serv = ServicioLocal()
		entradas = serv.obtenerServicio(Fecha = Fecha)
		cant = len(self.datos.index)
		#entrada => 'latitud' 'longitud' 'fecha'
		for nro, entrada in enumerate(entradas):
			latEntrada = entrada[nombreColumnas.latClave]
			longEntrada = entrada[nombreColumnas.longClave]
			fechaEntrada = datetime.strptime(entrada[nombreColumnas.fechaClave]['date'],'%Y-%m-%d %H:%M:%S')
			indiceEntrada =  cant + nro

			columnas = list(self.datos.columns)
			fila = pd.DataFrame(columns=columnas,index = [indiceEntrada]) #Fila vacia con el encabezado correspondiente
			fila[nombreColumnas.latClave] = latEntrada
			fila[nombreColumnas.longClave] = longEntrada
			
			#Completar variables fijas desde un archivo
			for var in self.variablesFijas:
				valor = utils.encontrarValorLongLat(lat=latEntrada,
											lon= longEntrada,
											recurso=self.pathVariablesFijas,
											feature=var)
				fila[var] = valor
			###########################################
			#Completar variables dinamicas

			for c in columnas:
				#Me quedo con las columnas que tienen un servicio asociado
				servicio = self.mapeoServicios.get(c)
				if servicio is not None:

					try:
						valorObtenido = servicio.obtenerServicio(Fecha=fechaEntrada,coords=[latEntrada,longEntrada])
					except:
						valorObtenido = None

					fila[c] = valorObtenido

			print fila 
			self.agregarFila(filas=fila)
			#Ahora hay que agregar la entrada a self.datos
		
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
		self.datos = self.datos.drop(columns=[feature],axis=1)

	#Considera que hay columnas que ya tienen datos cargados
	#Se fija cuales son los features dinámicos y los completa 
	#consultando a los servicios web de su mapeo
	#Es capaz de completar un dataset con distintas fechas
	#FALTA MODIFICAR PARA QUE LEA LA FECHA DE CADA FILA Y EN BASE A ESO CONSULTE LA API
	def completarDataset(self,Fecha):
		columnas = self.datos.columns

		for c in columnas:#reColumnas.precipC
			servicio = self.mapeoServicios.get(c)
			if servicio is not None:
				for index, fila in self.datos.iterrows():

					lat = fila[nombreColumnas.latClave]
					lon = fila[nombreColumnas.longClave]

					valorObtenido = servicio.obtenerServicio(Fecha=Fecha,coords=[lat,lon])

					self.datos.at[index,c] = valorObtenido



	def obtenerCantidad(self):
		return len(self.datos.index)

	def imprimir(self):
		print self.datos


#dataset = Dataset()
#dataset.imprimir()
#dataset.actualizarModelo(Fecha = datetime(2018,4,8,21,0))
#dataset.imprimir()