# -*- coding: utf-8 -*-
import __init__
import abc
from DatasetI import DatasetI
import pandas as pd
import sys,os
import nombreColumnas
from WBIO.PrecipAcumuladaWBIO import PrecipAcumuladaWBIO
from WBIO.PrecipitacionWBIO import PrecipitacionWBIO
from ServicioLocal import ServicioLocal
import utils
from datetime import datetime
#Librería utilizada: Pandas
#Feature a predecir: hayInundacion
#Features utilizados: 
#	Fecha, latitud, longitud -> Para el JOIN posterior a la consulta
#	Precipitacion:PrecipitacionOWM
#	Precipitacion acumulada de los últimos X=3 días: PrecipAcumuladaOWM
class Dataset(DatasetI):
	
	#De minima el dataset tiene las columnas latitud y longitud. Luego se agregan las variables dinámicas y fijas
	#Se asume que si se levanta un dataset de un path, el archivo no tiene filas duplicadas
	def __init__(self,path=None):
		super(Dataset,self).__init__(path)

		self.mapeoServicios = {nombreColumnas.precipClave:PrecipitacionWBIO(),
								nombreColumnas.preAcumClave:PrecipAcumuladaWBIO()}

		self.pathVariablesFijas = 'grilla.csv'
		self.variablesFijas = [nombreColumnas.drenajeClave,
								 nombreColumnas.poblacionClave,
								 nombreColumnas.alturaClave,
								 nombreColumnas.slopeClave,
								 nombreColumnas.depreClave]

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

	def eliminarDuplicados(self):
		self.datos = self.datos.drop_duplicates()

	#Fecha en args es la fecha de inicio del período hasta hoy
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
			self.datos = pd.concat([self.datos,fila])
			#Ahora hay que agregar la entrada a self.datos

	#filas debe ser un dataframe pandas
	def agregarFila(self,Dataset):
		filas = Dataset.obtenerDatos()
		self.datos = pd.concat([self.datos, filas])

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
	#consultando a los servicios web de su mapeo.
	#Además guarda en el atributo variablesDinámicas los valores obtenidos.
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

		#Inicializo un pandas con las variables dinamicas
		self.variablesDinamicas = pd.DataFrame(columns=self.mapeoServicios.keys())
		for f in self.mapeoServicios.keys():
			self.variablesDinamicas[f]=self.datos[f]

	def obtenerCantidad(self):
		return len(self.datos.index)

	def imprimir(self):
		print self.datos

	#Valores debería ser un pandas.
	def establecerDatosDinamicos(self,Valores):
		self.variablesDinamicas = Valores

	#Valores es un arreglo que determina el valor del campo hayInundacion
	#Si se levantó de un path el dataset, ya van a haber dropeado duplicados
	#y no va a ser necesario hacer un join con la grilla original.
	def agregarResultados(self, Valores):
		s = pd.Series(Valores,name="hayInundacion")
		self.agregarFeature(s)
		absolute_path = os.path.abspath(os.path.dirname('../modelo/recursos/'))
		grilla = pd.read_csv(absolute_path+'/'+self.pathVariablesFijas)

		#Join entre grilla y los resultados.
		indiceDeUnion = self.variablesFijas + self.mapeoServicios.keys()

		#Es para el circuito de generacion de dataset de consulta del modelo
		if hasattr(self, 'variablesDinamicas'):
			grilla = pd.concat([grilla,self.variablesDinamicas],axis=1)
			self.datos = grilla.set_index(indiceDeUnion).join(self.datos.set_index(indiceDeUnion))


#dataset = Dataset()
#dataset.imprimir()
#dataset.actualizarModelo(Fecha = datetime(2018,4,10,21,0))
#dataset.imprimir()