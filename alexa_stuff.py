import datetime
import json
import logging
import time
from pprint import pprint
from random import randint

import requests
from diskcache import Cache
from flask import Flask, render_template
from flask_ask import (Ask, convert_errors, question, request, session,
                       statement, version)

import clothing_options
import weather_observation

POSTAL_CODE = "postal"
LOCALE = "locale"
GET_ADDRESS = "GetAddress"
CYCLING = 'WhatToWearCyclingIntent'

STARTED = "started"
IN_PROGRESS = "in progress"
COMPLETED = 'completed'

app = Flask(__name__)

# This defines the endpoint where to get to the handler
ask = Ask(app, "/")

# for flask in particular this is the way to build out the web
logger = logging.getLogger("flask_ask")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

@app.route('/')
def homepage():
    t = datetime.datetime.now()
    return "Welcome to What to Wear {}".format(t)

@ask.launch
def launch():
     return statement("What outdoor activity are you planning?")

# Return values from every intent are simply strings either wrapped in a statement() or a question()
#  https://alexatutorial.com/flask-ask/requests.html#mapping-alexa-requests-to-view-functions
@ask.intent(CYCLING, 
    mapping={'city':'Where', 'dt':"WhenDate",'t':"WhatTime"}, 
    convert={'dt':'date','t':'time'}, 
    default={"city":'72712', 'dt':datetime.date.today, 't':datetime.time.hour})
def what_to_wear_cycling(city,dt, t):
    # if we don't get a city, then we need to ask Alexa for the postal code
    #dump_request_info()
    if 'Where' in convert_errors or city == None:
        city = get_location()
    
    logger.debug("Got a city {}".format(city))
    
    forecast = weather_observation.get_weather(dt,t,city)
    road_cycle = clothing_options.road_cycling()
    alexa_reply = road_cycle.get_alexa_reply(ob)
    return statement(alexa_reply)
    

@ask.intent("WhatToWearRunningIntent")
def what_to_wear_running():
    pass

@ask.intent("AMAZON.CancelIntent")
def cancel_intent():
    return (statement("okay"))

# For now, we are just going to return my zip code, later we will ask Alexa to give this information from a response we'll build
def get_location():
    return '72712'

################################################
#  Alexa specific code
# 
################################################
messages = {
    'SKILL_NAME' : "What to wear outside",
    'HELP_MESSAGE': "",
    'STOP_MESSAGE': "",
    'FINISHED_MESSSAGE':"",
    'WELCOME_MESSAGE':""
}

def dump_request_info():
    logger.info("Dumping request.....")
    logger.info("Request ID: {}".format(request.requestId))
    logger.info("Request Type: {}".format(request.type))
    logger.info("Request Timestamp: {}".format(request.timestamp))
    logger.info("Session New?: {}".format(session.new))
    logger.info("User ID: {}".format(session.user.userId))
    logger.info("Alexa Version: {}".format(version))

def get_message(msg_key):
    return messages[msg_key]

if __name__ == '__main__':
    app.run(port = 5101, debug=True)
