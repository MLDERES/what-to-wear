from pprint import pprint
import json
import unittest
import logging
import requests

WU_API_KEY = '7d65568686ff9c25'

class Observation ():
    
    def __init__(self, temp_f, ws, wdir, heat_index):
        self.feels_like_f = temp_f
        self.wind_speed = ws
        self.wind_direction = wdir
        self.heat_index_f = heat_index

    def __str__(self):
        return "Feels like {}.\n Windspeed: {}\n Direction: {}\nHeat Index: {}".format(self.feels_like_f, self.wind_speed, self.wind_direction, self.heat_index_f)

def get_observation(dct):
        if 'current_observation' in dct:
            #logging.debug(pprint(current_ob))
            current_ob = dct["current_observation"]
            #pprint(current_ob)
            return Observation(current_ob['feelslike_f'],current_ob['wind_mph'],current_ob['wind_dir'],current_ob['heat_index_f'])
        return dct

def get_weather(zipCode='72712', dbg=False):
        ob = None 
        if dbg:
            f = open('weather_underground.json')
            ob = json.load(f,object_hook=get_observation)       
        else:
            logging.debug('get_weather zipCode = '+ zipCode)
            request = 'http://api.wunderground.com/api/7d65568686ff9c25/geolookup/conditions/hourly/q/'+zipCode+'.json'
            f = requests.get(request)
            ob = json.loads(f.text,object_hook=get_observation)
            #logging.debug (json.dumps(json.loads(f.text), indent=4, sort_keys=False))
            # [logger.debug('x:{}'.format(x,parsed_json['current_observation'][x])) for x in parsed_json['current_observation'].keys]
            # location = parsed_json['location']['city']
            # temp_f = parsed_json['current_observation']['temp_f']
            # #print ("Current temperature in %s is: %s".format(location, temp_f))
        f.close()
        return ob
      

class TestRunner(unittest.TestCase):
    
    def __init__(self, test):
        super(TestRunner,self).__init__(test)
    def setUp(self):
         # Any setup code required to run the tests
        pass

    def test_fromFile(self):
        ob = get_weather(dbg=True)
        print(ob)
        self.assertTrue(ob is not None)

    #@unittest.skip('Not ready to test the web part yet')
    def test_fromWeb(self):
        ob = get_weather(dbg=False)
        print(ob)
        self.assertTrue(True)

if __name__ == "__main__":
    # doctest.testmod()
    unittest.main(verbosity=0)    

        