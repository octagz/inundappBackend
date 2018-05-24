from ServicioWebWBIO import ServicioWebWBIO

class PrecipitacionWBIO(ServicioWebWBIO):

	def __init__(self):
		super(PrecipitacionWBIO,self).__init__()

	def nombre_servicio(self):
		return 'precip'
