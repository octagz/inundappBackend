# -*- coding: utf-8 -*-

from ServicioWebWBIO import ServicioWebWBIO
from datetime import datetime,timedelta
import time

class PrecipAcumuladaWBIO(ServicioWebWBIO):

	def __init__(self):
		super(PrecipAcumuladaWBIO,self).__init__()

	#La lluvia acumulada a x dia no incluye la de ese dia,
	# sino la de los tres días anteriores
	def obtenerServicio(self,coords,Fecha=None):
		hoy = datetime.today()
		if Fecha is None:
			self.fecha = hoy
		else:
			self.fecha= Fecha

		fechaDiaAnt1 = self.fecha-timedelta(days=1)
		fechaDiaAnt2 = self.fecha-timedelta(days=2)
		fechaDiaAnt3 = self.fecha-timedelta(days=3)

		dia1 = super(PrecipAcumuladaWBIO,self).obtenerServicio(Fecha=fechaDiaAnt1, coords=coords)
		dia2 = super(PrecipAcumuladaWBIO,self).obtenerServicio(Fecha=fechaDiaAnt2, coords=coords)
		dia3 = super(PrecipAcumuladaWBIO,self).obtenerServicio(Fecha=fechaDiaAnt3, coords=coords)
		
		#print "dia1:"+str(dia1)+" dia2:"+str(dia2)+" dia3:"+str(dia3)

		#Parche para que no se rompa en caso de no encontrar valor
		if dia1 is None:
			dia1=0
		if dia2 is None:
			dia2=0
		if dia3 is None:
			dia3=0

		return dia1+dia2+dia3


	def nombre_servicio(self):
		return 'precip'

#s = PrecipAcumuladaWBIO()
#print(s.obtenerServicio(Fecha=datetime(2018,6,25,12,0), coords=[-37.8756344,-61.3618317]))