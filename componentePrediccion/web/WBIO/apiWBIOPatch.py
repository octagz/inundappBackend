from weatherbit.api import Api
import datetime

class apiWBIOPatch(Api):

	def __init__(self, key, granularity=None, https=False):
		super(apiWBIOPatch,self).__init__(key,granularity,https)
		self.version = 'v2.0'

		if granularity:
			self.history_granularity = granularity
	
	def set_history_granularity(self, granularity):
    		self.history_granularity = granularity

	#daily atm
	def get_history(self, **kwargs):

		if kwargs is None:
			raise Exception('Arguments Required.')

		if self.history_granularity:
        		kwargs['granularity'] = self.history_granularity
		else:
				raise Exception('Granularity is not set on the Api object, or it has not been supplied via call.') 	

		if 'start_date' not in kwargs or 'end_date' not in kwargs:
			raise Exception('start_date, and end_date required.')

		start_date = kwargs['start_date']
		end_date = kwargs['end_date']

		# Convert start_date, and end_dates into strings.
		#Todo: Make timezone aware using pytz.
		if type(start_date) is datetime.date:
		    kwargs['start_date'] = start_date.strftime('%Y-%m-%d')

		if type(end_date) is datetime.date:
			kwargs['end_date'] = end_date.strftime('%Y-%m-%d')

		url = self.get_history_url(**kwargs)

		return self._make_request(url, self._parse_history)