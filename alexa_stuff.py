import datetime
import json
import logging
from time import strftime
from pprint import pprint
from random import randint

import requests
from diskcache import Cache
from flask import Flask, render_template
from flask_ask import (Ask, convert_errors, question, request, session,
                       statement, delegate, version)

import clothing_options
import weather_observation
import traceback

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
log = logging.getLogger('werkzeug')
log.debug("just started")

@app.route('/')
def homepage():
    log.debug('hit the homepage')
    t = datetime.datetime.now()
    return "Welcome to What to Wear {}".format(t)

@ask.launch
def launch():
    log.debug('Got to the launch method')
    return statement("What outdoor activity are you planning?")

# Return values from every intent are simply strings either wrapped in a statement() or a question()
#  https://alexatutorial.com/flask-ask/requests.html#mapping-alexa-requests-to-view-functions
@ask.intent(CYCLING, 
    mapping={'city':'Where', 'dt':"WhenDate",'t':"WhatTime"}, 
    convert={'dt':'date','t':'time'})
    #default={"city":'72712', 'dt':datetime.date.today})
def what_to_wear_cycling(city,dt, t):
    # if we don't get a city, then we need to ask Alexa for the postal code
    #dump_request_info()
    
    log.debug('Got to the what to wear function.  Where="{}" When="{}" Time="{}"\n'.format(city,dt,t))
    if 'Where' in convert_errors or city == None:
        city = get_location()
    log.debug("Got a city {}".format(city))

    if 'WhenDate' in convert_errors or dt == None:
        log.debug("Didn't get passed a date.  Asking for one.")
        return delegate()

    if 'WhatTime' in convert_errors or t == None:
        log.debug("Didn't get passed a time.  Asking for one.")
        return delegate()

    log.debug("Calling get_weather({},{},{}".format(dt,t.hour,city))
    forecast = weather_observation.get_weather(dt,t.hour,city)
    log.debug("Got a weather forecast.")

    road_cycle = clothing_options.road_cycling()
    alexa_reply = road_cycle.get_alexa_reply(forecast)
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
    logging.info("Dumping request.....")
    logging.info("Request ID: {}".format(request.requestId))
    logging.info("Request Type: {}".format(request.type))
    logging.info("Request Timestamp: {}".format(request.timestamp))
    logging.info("Session New?: {}".format(session.new))
    logging.info("User ID: {}".format(session.user.userId))
    logging.info("Alexa Version: {}".format(version))

def get_message(msg_key):
    return messages[msg_key]

if __name__ == '__main__':
    handler = logging.FileHandler("c:/temp/whattowear.log")
    log = logging.getLogger(__name__)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # add formatter to handler
    handler.setFormatter(formatter)
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    log.debug(datetime.datetime.now())
    app.run(port = 5101, debug=True)
