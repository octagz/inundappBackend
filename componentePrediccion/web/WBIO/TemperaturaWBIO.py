from ServicioWebWBIO import ServicioWebWBIO

class TemperaturaWBIO(ServicioWebWBIO):

	def __init__(self):
		super(TemperaturaWBIO,self).__init__()

	def nombre_servicio(self):
		return 'temp'


#s = TemperaturaWBIO()
#print(s.obtenerServicio(Fecha=datetime(2018,5,24), coords=[-37.8756344,-61.3618317]))