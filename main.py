import unittest
import requests
import json
import logging
from weather_observation import Observation, get_weather

logger = logging.getLogger("what_to_wear")
logger.setLevel(logging.DEBUG)


fh= logging.FileHandler("main.log")
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s = %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)



def make_the_call(self, location, clothing_type="cycling"):
    # Get the weather
    # Create the right clothing option class
    # Return the Alexa response 
    ob = get_weather(location)


class TestAlexaReponse(unittest.TestCase):
    def __init__(self, test):
        super(TestAlexaReponse,self).__init__(test)

    def setUp(self):
         # Any setup code required to run the tests
        pass

    def test_make_the_call(self):
        pass

if __name__ == "__main__":
    # doctest.testmod()
    unittest.main(verbosity=0)