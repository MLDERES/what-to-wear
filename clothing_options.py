import unittest
import json
import logging
from pprint import pprint
import random

class clothing_option(object):
    """ Base class for different activity options.
        Reading from JSON, 
    """    
    _configuration = None
    _clothing_key = ""
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
        "always":
            [   "Of course, you should always ",
                "It would be insane not to ",
                "Also, you should always ",
                "And I never go out without "]}
    
    def __init__(self, temp_offset = 0):
        self._temp_offset = temp_offset
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Creating an instance of %s",self.__class__.__name__)

    def get_condition_for_temp(self, temp_f):
        """ Given a temperature (Farenheit), return a key (condition) used
            to gather up configuratons 
        """ 
        condition = "cold"
        t = temp_f + self._temp_offset
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
    
    def load_clothing_options(self):
        """ This is the default option for loading up the clothing options.  It can be overridden in child 
            classes if there is other set-up/defaults that child
        """
        with open('clothing_options.json') as file_stream:
            config = json.load(file_stream)
        if (config is None):
            logging.error("Unable to load the config file specified by %s", f)
        if self._clothing_key == "":
            raise(NotImplementedError()) 
        self._configuration = config[self._clothing_key]
        
        logging.debug(PrettyPrinter.format(self._configurationcon))
        # Load up the always part
        self.assertEqual({'all': 'sunscreen', 'head': 'helmet'},t_option._configuration["always"])

    def get_outfit(self, source, temp_f, conditions=None):
        """ This function will return the outfit to suggest, given the temperature and any weather conditions
            that might be important
        """
        if(self._configuration == ""):
            self.load_json(source)

        # Now let's get the outfit based on the temperature
        self._condition_temp = self.get_condition_for_temp(temp_f)
        
    def build_alexa_reply_main(self):
        [reply += " " + alexa_reply(k) for k in ]

    def get_alexa_reply(self):
        # Here's where we are going to build Alexa's reply
        ##  A: It looks like it is going to be warm (cold, frigid, chilly, hot, mild, super hot)
        reply_temperature = alexa_initial_prefix + _condition_temp
        reply_clothing = alexa_clothing_prefix + self.build_alexa_reply_main()
        reply_always = alexa_always_prefix + self.build_alexa_always_reply()

    # These are defined as propeties so that they could be overridden in subclasses if desired
    @property()
    def alexa_initial_prefix(self): 
         
        return random.choice(self._alexa_prefixes["initial"]) + "it is going to be "

    @property()
    def alexa_clothing_prefix(self):
        # For example
        # A:  I suggest you wear .....
        return random.choice(self._alexa_prefixes["clothing"])

    @property()
    def alexa_always_prefix(self):
        # For example
        #  A:  Of course, ALWAYS wear .... (helmet / sunscreen)
        return random.choice(self._alexa_prefixes["always"])


################################################
# Subclassing clothing option for "road cycling"
# 
################################################
class road_cycling(clothing_option):    
    _clothing_key= "road cycling"

################################################
# Test harness for this module
# 
################################################
class clothing_option_tester(unittest.TestCase):

    def test_load_json(self):
        t_option = road_cycling   
        with open('clothing_options.json') as fStream:
            t_option.load_json(t_option,fStream)
            pprint(t_option._configuration)
        # Load up the always part
        self.assertEqual({'all': 'sunscreen', 'head': 'helmet'},t_option._configuration["always"])

    def test_get_condition_for_temp(self):
        t_option = road_cycling
        with open('clothing_options.json') as fStream:
            t_option.load_json(t_option,fStream)
        # Load up the always part
        self.assertEqual({'all': 'sunscreen', 'head': 'helmet'},t_option._configuration["always"])


def main():
    unittest.main(verbosity=0)

if __name__ == '__main__':
    main()
