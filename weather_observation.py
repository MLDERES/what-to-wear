from pprint import pprint
import json
import unittest
import logging
import requests
import datetime
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/temp/cache/data',
    'cache.lock_dir': '/temp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

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
        return "Forecast for {}-{} time of day {}00. Temp:{} Condition:{} POP: {}".format(self.mth,self.month_day,self.tod,self.feels_like_f, self.condition, self.precip_chance)

    def get_fct_key(month_day=0,month_num=0,hour_of_day=0):
        return "{}_{}_{}".format(month_day,month_num,hour_of_day)


def _build_forecasts(dct):
    forecasts = {}
    def read_int(i):
        return None if int(i) <= NULL_VALUE else int(i)
    
    if FORECAST_KEY in dct:
        for f in dct[FORECAST_KEY]:
            time_dct = f[FCAST_TIME_KEY]
            f_key =Forecast.get_fct_key(month_day = read_int(time_dct[DATE_DAY]),
                                        month_num = read_int(time_dct[DATE_MONTH]),
                                        hour_of_day = read_int(time_dct[DATE_HOUR]))
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

@cache.cache("get_weather",expire=7200)
def get_weather(dt, tod, location='72712',dbg=False):
    forecasts = _fill_forecast(location)
    if(forecasts is None):
        logger.error("Unable to get forecast for location: {}".format(location))
    query_date = dt
    forecast_key = Forecast.get_fct_key(month_day=query_date.day,month_num=query_date.month,hour_of_day=tod)
    return forecasts[forecast_key]

@cache.cache(expire=7200)
def _fill_forecast(location):
    logger.debug('_fill_forecast = '+ location)
    request = _build_weather_request(location) #+'/geolookup/conditions/hourly/q/'+city+'.json'
    with requests.get(request) as f:
        logger.debug("Response from WU")
        logger.debug(f.text)
        wu_response = json.loads(f.text)
    forecasts = _build_forecasts(wu_response)
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
        self.oneday = datetime.timedelta(days=1)
        pass

    @unittest.skip('Not ready to test the web part yet')
    def test_fromFile(self):
        ob = get_weather(datetime.date.today()+self.oneday,16,dbg=True)
        print(ob)
        self.assertTrue(ob is not None)

    #unittest.skip('Not ready to test the web part yet')
    def test_fromWeb(self):
        ob = get_weather(datetime.date.today()+self.oneday,17,dbg=False)
        print(ob)
        self.assertTrue(True)

if __name__ == "__main__":
    # doctest.testmod()
    unittest.main(verbosity=0)    

        