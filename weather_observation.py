from pprint import pprint
import json
import unittest
import logging
import requests
import datetime

WU_API_KEY = '7d65568686ff9c25'
# So lets just key our observations off of mon_day_year
#  We'll store pretty date for whatever reason
# And for other conditions, we'll take
FORECAST_KEY = 'hourly_forecast'
FCAST_TIME_KEY = 'FCTTIME'
DATE_KEY = 'UTCDATE'
DATE_HOUR = 'hour'
DATE_MONTH = 'mon'
DATE_DAY = 'mday'
DATE_YEAR = 'year'

CONDITION_KEY = 'condition' # this would be the technical description
FANCY_COND_KEY = 'wx' # this is the human readable condition
FEELS_LIKE_KEY = 'feelslike' # then there is a dict of 'english' or 'metric'
METRIC_KEY = 'metric'
ENG_KEY = 'english'
HEAT_IDX_KEY = 'heatindex'
UV_INDEX_KEY = 'uvi'
TEMP_KEY = 'temp'
WIND_DIR_KEY = 'wdir' # but then we need the 'dir' or 'degrees' key to get it
WIND_SPEED_KEY = 'wspd' # also read dictionary of 'english' or 'metric'
RAIN_CHANCE_KEY = 'pop' # probability of precipitation
NULL_VALUE = -999

class Observation ():
    
    def __init__(self, temp_f, ws, wdir, heat_index):
        self.feels_like_f = temp_f
        self.wind_speed = ws
        self.wind_direction = wdir
        self.heat_index_f = heat_index

    def __str__(self):
        return "Feels like {}.\n Windspeed: {}\n Direction: {}\nHeat Index: {}".format(self.feels_like_f, self.wind_speed, self.wind_direction, self.heat_index_f)

class Forecast():
    def __init__(self):
        super(Forecast,self).__init__()
        self.condition = ""
        self.condition_human = ""
        self.feels_like_f = 0
        self.heat_index_f = 0
        self.temp_f = 0
        self.wind_dir = ''
        self.wind_speed = 0
        self.precip_chance = 0
        self.tod = 0
        self.month_day = 1
        self.mth = 1

    def __str__(self):
        return "Forecast for {} {}. Temp:{} Condition:{} POP: {}".format(self.feels_like_f, self.condition, self.precip_chance)

    def get_fct_key(d=0,m=0,h=0):
        return "{}_{}_{}".format(h,d,m)


def get_forecasts(dct):
    forecasts = {}
    def read_int(i):
        return None if int(i) <= NULL_VALUE else int(i)
    
    if FORECAST_KEY in dct:
        for f in dct[FORECAST_KEY]:
            time_dct = f[FCAST_TIME_KEY]
            f_key =Forecast.get_fct_key(d = read_int(time_dct[DATE_DAY]),
                                        m = read_int(time_dct[DATE_MONTH]),
                                        h = read_int(time_dct[DATE_HOUR]))
            fcast = Forecast()
            fcast.tod = read_int(time_dct[DATE_HOUR])
            fcast.mth = read_int(time_dct[DATE_MONTH])
            fcast.month_day = read_int(time_dct[DATE_DAY])
            fcast.condition = f[CONDITION_KEY]
            fcast.condition_human = f[FANCY_COND_KEY] 
            fcast.feels_like_f = read_int(f[FEELS_LIKE_KEY][ENG_KEY])
            fcast.heat_index_f = read_int(f[HEAT_IDX_KEY][ENG_KEY])
            fcast.temp_f = read_int(f[TEMP_KEY][ENG_KEY])
            fcast.wind_dir = f[WIND_DIR_KEY]['dir']
            fcast.wind_speed = read_int(f[WIND_SPEED_KEY][ENG_KEY])
            fcast.precip_chance = read_int(f[RAIN_CHANCE_KEY])
            forecasts[f_key]=fcast 
        return forecasts
    return dct



def get_observation(dct):
    if 'current_observation' in dct:
        #logging.debug(pprint(current_ob))
        current_ob = dct["current_observation"]
        #pprint(current_ob)
        return Observation(current_ob['feelslike_f'],current_ob['wind_mph'],current_ob['wind_dir'],current_ob['heat_index_f'])
    return dct

def get_weather(dt, location='72712',dbg=False):
        forecasts = None 
        # dt should be the date and the time
        if dbg:
            with open('forecast.json') as f:
                wu_response = json.load(f)       
        else:
            logging.debug('get_weather location = '+ location)
            logging.debug('date time = {}'.format(dt))
            
            request = _build_weather_request(location) #+'/geolookup/conditions/hourly/q/'+city+'.json'
            with requests.get(request) as f:
                #TODO: I'm going to want to cache the response once I create the object with just the fields I need
                print(f.text,"c:/temp/weather.json")
                wu_response = json.loads(f.text)
        forecasts = get_forecasts(wu_response)
        return forecasts

def _build_weather_request(location):
    #http://api.wunderground.com/api/7d65568686ff9c25/features/settings/q/query.format
    # Features = alerts/almanac/astromony/conditions/forecast/hourly/hourly10day etc.
    # settings(optional) = lang, pws(personal weather stations):0 or 1
    # query = location (ST/City, zipcode,Country/City, or lat,long)
    # format = json or xml
    request = 'http://api.wunderground.com/api/'+WU_API_KEY
    request += "/hourly10day"
    request += "/q/"+location
    request += ".json"
    return request

class TestRunner(unittest.TestCase):
    
    def __init__(self, test):
        super(TestRunner,self).__init__(test)
    def setUp(self):
         # Any setup code required to run the tests
        pass

    @unittest.skip('Not ready to test the web part yet')
    def test_fromFile(self):
        ob = get_weather(datetime.date.today,dbg=True)
        print(ob)
        self.assertTrue(ob is not None)

    #unittest.skip('Not ready to test the web part yet')
    def test_fromWeb(self):
        ob = get_weather(datetime.date.today,dbg=False)
        print(ob)
        self.assertTrue(True)

if __name__ == "__main__":
    # doctest.testmod()
    unittest.main(verbosity=0)    

        