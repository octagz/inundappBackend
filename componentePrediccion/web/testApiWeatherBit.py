# -*- coding: utf-8 -*-

from weatherbit.api import Api
api_key = "cab3491bd2254e8aa0aab3e59a6b52fd"
lat = 38.00
long = -125.75

api = Api(api_key)

# Optional - Use HTTPS instead.
# api.set_https(True)

# Set the granularity of the API - Options: ['daily','hourly','3hourly']
# Will only affect forecast requests.

#forecast = api.get_forecast(lat=lat, lon=long)

# You can also query by city:
#forecast = api.get_forecast(city="Bahia Blanca,AR")

# Or City, state, and country:
history = api.get_history(lat="",lon="", start_date="2018-05-20",end_date="2018-05-21")
print(history.get_series([]))




# To get a time series of temperature, and precipitation:
#print(forecast.get_series(['temp','precip']))