import unittest
import utils
import doctest
import json
from pprint import pprint

class TestRunner(unittest.TestCase):
    
    def __init__(self, test):
        super(TestRunner,self).__init__(test)
        #bind module functions to tester class
        #self.GameBoard = GameBoard


    def setUp(self):
        """ Any setup code required to run the tests in this case we'll load up the json file with the weather data
        """
        pass
        
    def test_SimpleCase(self):
        with open('weather_underground.json') as f:
            self.__weather_data = json.load(f)
            
        pprint(self.__weather_data['current_observation'])
        pprint(self.__weather_data['hourly_forecast'],depth = 2)

        
if __name__ == "__main__":
    # doctest.testmod()
    unittest.main(verbosity=0)