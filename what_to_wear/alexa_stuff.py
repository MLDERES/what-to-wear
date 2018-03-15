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
                       statement, delegate, version, confirm_slot)

import traceback
import re
from utils import states, get_human_friendly_location

POSTAL_CODE = "postal"
LOCALE = "locale"
GET_ADDRESS = "GetAddress"
CYCLING = 'WhatToWearCyclingIntent'

STARTED = "started"
IN_PROGRESS = "in progress"
COMPLETED = 'completed'

app = Flask(__name__)
app.config['ASK_PRETTY_DEBUG_LOGS']=True
app.config['ASK_VERIFY_TIMESTAMP_DEBUG'] = True

# This defines the endpoint where to get to the handler
ask = Ask(app, "/")

# for flask in particular this is the way to build out the web
log = logging.getLogger('flask_ask')
log.setLevel(logging.DEBUG)
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

# For now, we are just going to return my zip code, later we will ask Alexa to give this information from a response we'll build
def get_location():
    return 'AR/Bentonville'

################################################
# This is working code, but I wanted to a bit more dialog if we don't get a date and time
# 
################################################
# Return values from every intent are simply strings either wrapped in a statement() or a question()
#  https://alexatutorial.com/flask-ask/requests.html#mapping-alexa-requests-to-view-functions
# @ask.intent(CYCLING, 
#     mapping={'city':'Where', 'dt':"WhenDate",'t':"WhatTime"}, 
#     convert={'dt':'date','t':'time'})
#     #default={"city":'72712', 'dt':datetime.date.today})
# def old_what_to_wear_cycling(city,dt, t):
#     # if we don't get a city, then we need to ask Alexa for the postal code
#     #dump_request_info()
    
#     log.debug('Got to the what to wear function.  Where="{}" When="{}" Time="{}"\n'.format(city,dt,t))
#     if 'Where' in convert_errors or city == None:
#         city = get_location()
#     log.debug("Got a city {}".format(city))

#     if 'WhenDate' in convert_errors or dt == None:
#         log.debug("Didn't get passed a date.  Asking for one.")
#         return delegate()

#     if 'WhatTime' in convert_errors or t == None:
#         log.debug("Didn't get passed a time.  Asking for one.")
#         return delegate()

#     log.debug("Calling get_weather({},{},{}".format(dt,t.hour,city))
#     forecast = weather_observation.get_weather(dt,t.hour,city)
#     log.debug("Got a weather forecast.")

#     road_cycle = clothing_options.road_cycling()
#     alexa_reply = road_cycle.get_alexa_reply(forecast)
#     return statement(alexa_reply)
    
@ask.intent(CYCLING, 
    mapping={'location':'Where', 'dt':"WhenDate",'t':"WhatTime"}, 
    convert={'dt':'date','t':'time'},
    default={"location":get_location})
def what_to_wear_cycling(dt, t, location):
    # if we don't get a city, then we need to ask Alexa for the postal code
    #dump_request_info()
    import states

    log.debug('Got to the what to wear function. dialogState={}  Where="{}" When="{}" Time="{}"\n'.format(session["dialogState"],location,dt,t))
    if (session["dialogState"]!="COMPLETED"):
        if 'Where' in convert_errors or location == None:
            #city = get_location()
            return confirm_slot("Where", "Are you leaving from {}".format(states._get_human_friendly_location(location)))
        log.debug("Got a location {}".format(location))

        if 'WhenDate' in convert_errors or dt == None:
            log.debug("Didn't get passed a date.  Asking for one.")
            return delegate()

        if 'WhatTime' in convert_errors or t == None:
            log.debug("Didn't get passed a time.  Asking for one.")
            return delegate()

    return statement(_determine_what_to_wear(dt,t.hour,location))

def _determine_what_to_wear(dt, t, location):
    # Now we can go on
    log.debug("Calling get_weather({},{},{})".format(dt,t,location))
    forecast = weather_observation.get_weather(dt,t,location)
    log.debug("Got a weather forecast.")

    road_cycle = clothing_options.road_cycling()
    alexa_reply = road_cycle.get_alexa_reply(forecast)
    return alexa_reply



@ask.intent("WhatToWearRunningIntent")
def what_to_wear_running():
    pass

@ask.intent("AMAZON.CancelIntent")
def cancel_intent():
    return (statement("okay"))





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
    # # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  
    # # add formatter to handler
    handler.setFormatter(formatter)
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    log.debug(datetime.datetime.now())
    app.run(port = 5101, debug=True)
