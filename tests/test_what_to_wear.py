import unittest
import datetime


class ForecastTests(unittest.TestCase):
   
    def __init__(self, test):
        super(WeatherTests,self).__init__(test)
        self._location = "AR/Bentonville"

    def setUp(self):
         # Any setup code required to run the tests
        self.oneday = datetime.timedelta(days=1)
        pass

    @unittest.skip('Not wanting to test from a file anymore')
    def test_fromFile(self):
        ob = get_weather(datetime.date.today()+self.oneday,16,self._location,dbg=True)
        print(ob)
        self.assertTrue(ob is not None)


    def test_fromWeb(self):
        ob = get_weather(datetime.date.today()+self.oneday,self._location, 17,dbg=False)
        print(ob)
        self.assertTrue(True)


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



if __name__ == "__main__":
    # doctest.testmod()
    unittest.main(verbosity=0)    

