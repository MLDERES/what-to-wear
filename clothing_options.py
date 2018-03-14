import unittest
import json
import logging
from pprint import pprint
import random
from weather_observation import Forecast

class clothing_option(object):
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


    def get_alexa_reply(self, forecast):
        # Here's where we are going to build Alexa's reply
        ##  A: It looks like it is going to be warm (cold, frigid, chilly, hot, mild, super hot)
        temp = forecast.feels_like_f
        self._get_outfit(temp)
        reply_temperature = self.alexa_initial_prefix + self._condition_temp + ". {} degrees.".format(temp) 
        if(self._outfit is not None):
            reply = reply_temperature + ".,,, " + self._build_alexa_reply_main() + ".,,," + self._build_alexa_always_reply()
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
class road_cycling(clothing_option):    
    ACTIVITY_TYPE_KEY= "road cycling"
    BODY_PARTS_KEYS = ["head","face","upper_body","lower_body","arms","hands","legs","feet"]


################################################
# Test harness for this module
# 
################################################
class clothing_option_tester(unittest.TestCase):

    unittest.skip('Not ready yet')
    def test_get_alexa_reply(self):
        fcast = Forecast()
        fcast.feels_like_f = 56
        fcast.precip_chance = 10
        fcast.wind_dir = "NNE"
        fcast.wind_speed = 3
        fcast.condition = 'Sunny'
        road = road_cycling()
        msg = road.get_alexa_reply(fcast)
        pprint(msg)

    def test_build_response(self):
        d = {"head": "",'body': ['long-sleeve baselayer', 'short sleeve jersey']}
        
        co = clothing_option()
        reply = co._build_generic_from_dictionary(d)
        self.assertEqual(reply, "either long-sleeve baselayer or short sleeve jersey")

        d["lower_body"]="long pants"
        reply = co._build_generic_from_dictionary(d)
        self.assertEqual(reply, "either long-sleeve baselayer or short sleeve jersey and also long pants")

        d["legs"]="long socks"
        d["something"]="toe covers"
        reply = co._build_generic_from_dictionary(d)
        self.assertEqual(reply, "either long-sleeve baselayer or short sleeve jersey and also long pants,long socks and toe covers")

        d["s2"]=["shoes","laces"]
        reply = co._build_generic_from_dictionary(d)
        print (reply)
        self.assertEqual(reply, "either long-sleeve baselayer or short sleeve jersey and also"+
                    " long pants,long socks,toe covers and either shoes or laces")




if __name__ == '__main__':
    unittest.main(verbosity=0)
