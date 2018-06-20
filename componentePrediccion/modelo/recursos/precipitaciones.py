# -*- coding: utf-8 -*-
import __init__
import requests
import pandas as pd
import nombreColumnas

class precipitaciones:

    def __init__(self, resource):
        self.resource = resource
        self.resourcedf = None
        self.dataframe = None
        self.url = 'http://ide.agroindustria.gob.ar/SIRMin/csirmin_lluvias_diarias/ConsultaPrecipitaciones.php'
        self.SIZE_UPDATE = 40 #.csv updated after 40 resource entries --> update of approximately 40000 new entries
        self.MAX_REQUEST = 4 #ConsultaPrecipitaciones.php up to 4 points(lat&lon) per request

    def loadResource(self):
        self.resourcedf= pd.read_csv(self.resource, delim_whitespace = True)

    def getPayload(self, i, r, payload):
         #according to resource file
        lat = (r[nombreColumnas.latClave] / 100000) * -1
        lon = (r[nombreColumnas.longClave] / 100000) * -1
        #according to web service syntax
        payload['lugares[' + str(i) + '][0]'] = lon 
        payload['lugares[' + str(i) + '][1]'] = lat

    def getDataByPlaces(self):
        if (self.resourcedf == None):
            self.loadResource()
        payload = {}
        self.dataframe = pd.DataFrame(columns=[nombreColumnas.latClave, nombreColumnas.longClave, nombreColumnas.fechaClave, nombreColumnas.precipClave])                   
        for index, row in self.resourcedf.iterrows():
            self.getPayload(index, row, payload)
            if (((index + 1) % self.MAX_REQUEST) == 0):
                results, places = self.sendRequest(payload)
                self.parseData(results, places)
                payload = {} #cleaning payload for next request
                self.printStatus(index, places)
            if (((index + 1) % self.SIZE_UPDATE) == 0):
                self.storeData()

    def printStatus(self, index, places):
        print 'dataframe updated: (rows,columns) = ', self.dataframe.shape
        print 'iteration: ', index
        print 'places: '
        for place in places:
            print 'place: ', place
        print '----------------------------------------------------------------------------------------------------------------------------'

    def storeData(self):
        self.dataframe.to_csv('precipitaciones.csv', index = False)
        print 'dataframe update saved'
              
    def sendRequest(self, payload):
        result = requests.get(url = self.url,
                              params = payload)
        response = result.json()
        data = response[0]
        places = response[1]

        return data, places

    def placeToCoords(self, place):
        coords = place.split('(')[1].split(')')[0].split(',')
        lat = float(coords[1])
        lon = float(coords[0])

        return lat, lon

    def parseData(self, data, places):
        for observation in data: #0..n
            for place in places: #1..4
                lat, lon = self.placeToCoords(place)
                #add new row to dataframe
                df = pd.DataFrame([[lat, lon, observation['fecha'], observation[place]]], columns=[nombreColumnas.latClave, nombreColumnas.longClave, nombreColumnas.fechaClave, nombreColumnas.precipClave])
                self.dataframe = pd.concat([self.dataframe, df], ignore_index = True)

p = precipitaciones('test.xyz')
p.getDataByPlaces()