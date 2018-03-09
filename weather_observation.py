from pprint import pprint
import json
import unittest
import logging
import requests

class observation (dict):

    WU_API_KEY = '7d65568686ff9c25'
   
    def as_observation(dct):
        if 'current_observation' in dct:
            #logging.debug(pprint(current_ob))
            current_ob = dct["current_observation"]
            ob = observation(current_ob['feelslike_f'],current_ob['wind_mph'],current_ob['wind_dir'],current_ob['heat_index_f'])
            return ob
        return current_ob

    def __init__(self, temp_f, ws, wdir, heat_index):
        self.feels_like_f = temp_f
        self.wind_speed = ws
        self.wind_direction = wdir
        self.heat_index_f = heat_index

    @classmethod
    def get_weather(zipCode='72712'):
        logging.debug('get_weather zipCode = '+ zipCode)
        request = 'http://api.wunderground.com/api/7d65568686ff9c25/geolookup/conditions/hourly/q/'+zipCode+'.json'
        f = requests.get(request)
        ob = json.loads(f,object_hook=as_observation)
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
        with open('weather_underground.json') as f:
            ob = json.load(f,object_hook=observation.as_observation)
        pprint(ob)
        
if __name__ == "__main__":
    # doctest.testmod()
    unittest.main(verbosity=0)    

        