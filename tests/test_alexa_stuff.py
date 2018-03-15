
import unittest
import os
import six
import sys
import time
import subprocess

from requests import post

import flask_ask


launch = {
  "version": "1.0",
	"session": {
		"new": true,
		"sessionId": "amzn1.echo-api.session.5a514ed4-39cf-44f5-80e9-67db22279f48",
		"application": {
			"applicationId": "amzn1.ask.skill.46947903-05d0-44b2-969f-104b49dae4f0"
		},
		"user": {
			"userId": "amzn1.ask.account.AEEOLMTPBSL5SJUBG25WDS5XUZCUO5UGHEJTS3IFTPD3EJSDP7ASX63RJZLLZXH3IN4QFQPULRBPVUJ4WZ56E5ZZEGXWERW44DCXID75GUKJRNM4FKKUKIR4R5WLS6B54GFQEWX2GWLJWWZPE7TTHBIBBG3IA4UFAUNPJ2HIFFTPGJDK5YY4ZPV5HSEZCGZDSRBQPLSQIY6ZJWA"
		}
	},
	"context": {
		"AudioPlayer": {
			"playerActivity": "IDLE"
		},
		"Display": {
			"token": ""
		},
		"System": {
			"application": {
				"applicationId": "amzn1.ask.skill.46947903-05d0-44b2-969f-104b49dae4f0"
			},
			"user": {
				"userId": "amzn1.ask.account.AEEOLMTPBSL5SJUBG25WDS5XUZCUO5UGHEJTS3IFTPD3EJSDP7ASX63RJZLLZXH3IN4QFQPULRBPVUJ4WZ56E5ZZEGXWERW44DCXID75GUKJRNM4FKKUKIR4R5WLS6B54GFQEWX2GWLJWWZPE7TTHBIBBG3IA4UFAUNPJ2HIFFTPGJDK5YY4ZPV5HSEZCGZDSRBQPLSQIY6ZJWA"
			},
			"device": {
				"deviceId": "amzn1.ask.device.AHZCXFXKPDQAF47M3IEX6TJRAOUH64UYTJ2LIL52DBAHM4XFCJKZBD5LT3SMS27GMQGNX2JA4XPIRD3XYOVRSB44XERU3AM3Q4OFBAVMKLGWUZIFAOS37UNI4OIHKQV3AW6NHYUDXY2PA4DHTJ5DEOR7FPQA",
				"supportedInterfaces": {
					"AudioPlayer": {},
					"Display": {
						"templateVersion": "1.0",
						"markupVersion": "1.0"
					}
				}
			},
			"apiEndpoint": "https://api.amazonalexa.com",
			"apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjQ2OTQ3OTAzLTA1ZDAtNDRiMi05NjlmLTEwNGI0OWRhZTRmMCIsImV4cCI6MTUyMTE0MjQ2OCwiaWF0IjoxNTIxMTM4ODY4LCJuYmYiOjE1MjExMzg4NjgsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUhaQ1hGWEtQRFFBRjQ3TTNJRVg2VEpSQU9VSDY0VVlUSjJMSUw1MkRCQUhNNFhGQ0pLWkJENUxUM1NNUzI3R01RR05YMkpBNFhQSVJEM1hZT1ZSU0I0NFhFUlUzQU0zUTRPRkJBVk1LTEdXVVpJRkFPUzM3VU5JNE9JSEtRVjNBVzZOSFlVRFhZMlBBNERIVEo1REVPUjdGUFFBIiwidXNlcklkIjoiYW16bjEuYXNrLmFjY291bnQuQUVFT0xNVFBCU0w1U0pVQkcyNVdEUzVYVVpDVU81VUdIRUpUUzNJRlRQRDNFSlNEUDdBU1g2M1JKWkxMWlhIM0lONFFGUVBVTFJCUFZVSjRXWjU2RTVaWkVHWFdFUlc0NERDWElENzVHVUtKUk5NNEZLS1VLSVI0UjVXTFM2QjU0R0ZRRVdYMkdXTEpXV1pQRTdUVEhCSUJCRzNJQTRVRkFVTlBKMkhJRkZUUEdKREs1WVk0WlBWNUhTRVpDR1pEU1JCUVBMU1FJWTZaSldBIn19.Auwhy2TokmCDH3vert-ZheoGwXb1R-SuP9U5IDcJBOqY9Rw8itVVXxAtPsR71ZwV5bS_F2B5Bbly745pHC2VO3jhTfiK7PhpJS6J-TA3HE4YXwzTnsxs90YNjMUCzHL7xnHNQpMkRkAVsNQd8HoPUnHvrl4CpmVruxUy-83FNvEqq1tuZWjEDkmIAtvM194p9_BtPelRZGx1fJa6_4u19YwjPIoECuObPiHBJIaMLD-33onsEQIIdTPnYcKjhkBh0kZk0O5SOobHZp--Ov_Wi-VePGbazX_xYNVmUsYqdkBseiN0kX7og9524t5VHWQuyI7a6b1I-P4E2ajGjJIxdw"
		}
	},
	"request": {
		"type": "IntentRequest",
		"requestId": "amzn1.echo-api.request.27bb39ce-a43b-4b56-98af-faadd3a72818",
		"timestamp": "2018-03-15T18:34:28Z",
		"locale": "en-US",
		"intent": {
			"name": "WhatToWearCyclingIntent",
			"confirmationStatus": "NONE",
			"slots": {
				"Where": {
					"name": "Where",
					"confirmationStatus": "NONE"
				},
				"WhenDate": {
					"name": "WhenDate",
					"value": "2018-03-17",
					"confirmationStatus": "NONE"
				},
				"WhatTime": {
					"name": "WhatTime",
					"value": "10",
					"confirmationStatus": "NONE"
				}
			}
		},
		"dialogState": "STARTED"
	}
}

@unittest.skipIf(six.PY2, "Not yet supported on Python 2.x")
class SmokeTestUsingSamples(unittest.TestCase):
    """ Try launching each sample and sending some requests to them. """

    def setUp(self):
        self.python = sys.executable
        self.env = {'PYTHONPATH': project_root,
                    'ASK_VERIFY_REQUESTS': 'false'}
        if os.name == 'nt':
            self.env['SYSTEMROOT'] = os.getenv('SYSTEMROOT')
            self.env['PATH'] = os.getenv('PATH')

    def _launch(self, sample):
        prefix = os.path.join(project_root, 'samples/')
        path = prefix + sample
        process = subprocess.Popen([self.python, path], env=self.env)
        time.sleep(1)
        self.assertIsNone(process.poll(),
                          msg='Poll should work,'
                          'otherwise we failed to launch')
        self.process = process

    def _post(self, route='/', data={}):
        url = 'http://127.0.0.1:5000' + str(route)
        print('POSTing to %s' % url)
        response = post(url, json=data)
        self.assertEqual(200, response.status_code)
        return response

    @staticmethod
    def _get_text(http_response):
        data = http_response.json()
        return data.get('response', {})\
                   .get('outputSpeech', {})\
                   .get('text', None)

    @staticmethod
    def _get_reprompt(http_response):
        data = http_response.json()
        return data.get('response', {})\
                   .get('reprompt', {})\
                   .get('outputSpeech', {})\
                   .get('text', None)

    def tearDown(self):
        try:
            self.process.terminate()
            self.process.communicate(timeout=1)
        except Exception as e:
            try:
                print('[%s]...trying to kill.' % str(e))
                self.process.kill()
                self.process.communicate(timeout=1)
            except Exception as e:
                print('Error killing test python process: %s' % str(e))
                print('*** it is recommended you manually kill with PID %s',
                      self.process.pid)