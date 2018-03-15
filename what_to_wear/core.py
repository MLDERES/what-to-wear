import unittest
import json
import logging
from pprint import pprint
import random
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from dateutil import parser
import datetime

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/temp/cache/data',
    'cache.lock_dir': '/temp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

class _clothing_option(object):
    """ Base class for different activity options.
        Reading from JSON, 
    """    
    ACTIVITY_TYPE_KEY = "" # Should be overriden in child classes to know where to look in the JSON config
    # Override in other subclasses if this list should be different
    BODY_PARTS_KEYS = []
    ALWAYS_KEY = "always"

    
    _configuration = None
    
    _alexa_prefixes = { 
        "initial": 
            [   "It looks like ", 
                "Oh my ", 
                "Well ", 
                "Temperature seems ", 
                "Weather underground says "],
        "clothing":
            [   "I suggest wearing ",
                "Based on the weather conditions, you should consider ",
                "Looks like today would be a good day to wear ",
                "If I were riding I'd wear "],
        ALWAYS_KEY:
            [   "Of course, you should always ",
                "It would be insane not to wear ",
                "Also, you should always wear ",
                "And I never go out without "]}
    
    def __init__(self, temp_offset = 0):
        self._temp_offset = temp_offset
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Creating an instance of %s",self.__class__.__name__)

    def _get_condition_for_temp(self, temp_f):
        """ Given a temperature (Farenheit), return a key (condition) used
            to gather up configuratons 
        """ 
        condition = "cold"
        t = int(temp_f) + self._temp_offset
        if (t < 40):
            condition = "cold"
        elif (t < 48):
            condition = "cool"
        elif (t < 58):
            condition = "mild"
        elif (t < 68):
            condition = "warm"
        elif (t < 75):
            condition = "very warm"
        else:
            condition = "hot"
        return condition
    
    def _load_clothing_options(self):
        """ This is the default option for loading up the clothing options.  It can be overridden in child 
            classes if there is other set-up/defaults that child
        """
        with open('clothing_options.json') as file_stream:
            config = json.load(file_stream)
        if (config is None):
            logging.error("Unable to load the config file clothing_options.json")
        if self.ACTIVITY_TYPE_KEY == "":
            raise(NotImplementedError()) 
        self._configuration = config[self.ACTIVITY_TYPE_KEY]
        
    def _get_outfit(self, temp_f, conditions=None):
        """ This function will return the outfit to suggest, given the temperature and any weather conditions
            that might be important
        """
        if(self._configuration is None):
            self._load_clothing_options()

        # Now let's get the outfit based on the temperature
        self._condition_temp = self._get_condition_for_temp(temp_f)
        
        if(self.ALWAYS_KEY in self._configuration):
            self._always = self._configuration[self.ALWAYS_KEY]
        
        if(self._condition_temp in self._configuration) :
            self._outfit = self._configuration[self._condition_temp]
        
    def _build_generic_from_dictionary(self, dct, keys=None):
        reply = ""
        following_list = False
        if(keys is None):
            keys = dct.keys()
        for k in keys:
            if k in dct :
                # Deal with lists
                reply += " and also " if following_list else ""
                if type(dct[k]) is list:
                    if len(reply) > 0 :
                        reply += 'and '
                    reply += 'either '
                    reply += ' or '.join(dct[k])
                    following_list = True
                # And non-lists
                elif len(dct[k]) > 0:
                    following_list = False
                    reply += dct[k] + ','
        reply = reply.strip(',')
        pos = reply.rfind(',')
        # Here we are just taking out the last , to replace it with 'and'
        if pos > 0:
            reply = reply[:pos] + " and " + reply[pos+1:]
            reply = reply.replace("and and","and")
        return reply

    def _build_alexa_always_reply(self):
        reply_always = ""
        if not self._always is None:
            reply_always += self.alexa_always_prefix 
            reply_always += self._build_generic_from_dictionary(self._always)
        return reply_always

    def _build_alexa_reply_main(self):
        reply_clothing = ""
        if self._outfit is None:
            raise(ValueError())

        reply_clothing += self.alexa_clothing_prefix
        reply_clothing += self._build_generic_from_dictionary(self._outfit, self.BODY_PARTS_KEYS)
        return reply_clothing


    def build_alexa_reply(self, forecast):
        # Here's where we are going to build Alexa's reply
        ##  A: It looks like it is going to be warm (cold, frigid, chilly, hot, mild, super hot)
        temp = forecast.feels_like_f
        self._get_outfit(temp)
        reply_temperature = self.alexa_initial_prefix + self._condition_temp + ". {} degrees.".format(temp) 
        if(self._outfit is not None):
            reply = reply_temperature + ". " + self._build_alexa_reply_main() + ". " + self._build_alexa_always_reply()
        else:
            reply = reply_temperature
            reply += "Unfortunately, I don't know how to tell you to dress for that condition."
        return reply
       
    
    # These are defined as propeties so that they could be overridden in subclasses if desired
    @property
    def alexa_initial_prefix(self): 
        return random.choice(self._alexa_prefixes["initial"]) + "it is going to be "

    @property
    def alexa_clothing_prefix(self):
        # For example
        # A:  I suggest you wear .....
        return random.choice(self._alexa_prefixes["clothing"])

    @property
    def alexa_always_prefix(self):
        # For example
        #  A:  Of course, ALWAYS wear .... (helmet / sunscreen)
        return random.choice(self._alexa_prefixes["always"])

################################################
# Subclassing clothing option for "road cycling"
# 
################################################
class RoadCycling(_clothing_option):    
    ACTIVITY_TYPE_KEY= "road cycling"
    BODY_PARTS_KEYS = ["head","face","upper_body","lower_body","arms","hands","legs","feet"]

_WU_API_KEY = '7d65568686ff9c25'
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

    def gen_fct_key(month_day=0,month_num=0,hour_of_day=0):
        return "{}_{}_{}".format(month_day,month_num,hour_of_day)

    def _build_forecasts(dct):
        forecasts = {}
        def read_int(i):
            return None if int(i) <= NULL_VALUE else int(i)
        
        if FORECAST_KEY in dct:
            for f in dct[FORECAST_KEY]:
                time_dct = f[FCAST_TIME_KEY]
                f_key =Forecast.gen_fct_key(month_day = read_int(time_dct[DATE_DAY]),
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

    #@cache.cache(expire=7200)
    @classmethod
    def find_weather(location, forecast_date, time_of_day,dbg=False):
        log.debug("In get_weather.  dt={} tod={} location={}".format(forecast_date,time_of_day,location))
        
        if(not (type(forecast_date) is datetime.date)):
            query_date = parser.parse(forecast_date).date
        else:
            query_date = forecast_date

        forecasts = Forecast._fill_forecast(location)
        if(forecasts is None):
            log.error("Unable to get forecast for location: {}".format(location))
        
        if (not (type(time_of_day) is datetime.time)):
            tod = int(time_of_day)
            if( tod > 23 or tod < 0):
                raise ValueError("time_of_day should be either a datetime.time object or an integer between 0 and 23")
            else:
                tod = time_of_day.hour
                
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

    @classmethod()
    def _build_weather_request(location):
        #http://api.wunderground.com/api/7d65568686ff9c25/features/settings/q/query.format
        # Features = alerts/almanac/astromony/conditions/forecast/hourly/hourly10day etc.
        # settings(optional) = lang, pws(personal weather stations):0 or 1
        # query = location (ST/City, zipcode,Country/City, or lat,long)
        # format = json or xml
        request = 'http://api.wunderground.com/api/'+_WU_API_KEY
        request += "/hourly10day"
        request += "/q/"+ location.strip(' /')
        request += ".json"
        return request




if __name__ == '__main__':
    print (Forecast.gen_fct_key(10,1,10))
    print (Forecast.find_weather("AR/Bentonville",forecast_date=datetime.date.today(),time_of_day=date.time.now()))
    unittest.main(verbosity=0)
