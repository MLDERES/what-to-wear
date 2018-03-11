import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, version, convert_errors, request
import json
import requests
import time
import unidecode
import weather_observation
import clothing_options

SPEECHOUTPUT_KEY = "speechOutput"
REPROMPT_KEY = "repromptText"
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
log = logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch():
    pass

# Return values from every intent are simply strings either wrapped in a statement() or a question()
#  https://alexatutorial.com/flask-ask/requests.html#mapping-alexa-requests-to-view-functions
@ask.intent(CYCLING, mapping={'city':'Where', 'dt':"WhenDate",'t':"WhatTime"}, convert={'WhenDate':'date','WhatTime':'time'}, default={"Where":'72712'})
def what_to_wear_cycling(city,dt, t):
    # if we don't get a city, then we need to ask Alexa for the postal code
    dump_request_info()

    if 'Where' in convert_errors:
        city = get_location()
    
    ob = weather_observation.get_weather(city)
    road_cycle = clothing_options.road_cycling()
    road_cycle.get_alexa_reply(ob)
    return statement(ob)
    

@ask.intent("WhatToWearRunningIntent")
def what_to_wear_running():
    pass

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
    log.info("Request ID: {}".format(request.requestId))
    log.info("Request Type: {}".format(request.type))
    log.info("Request Timestamp: {}".format(request.timestamp))
    log.info("Session New?: {}".format(session.new))
    log.info("User ID: {}".format(session.user.userId))
    log.info("Alexa Version: {}".format(version))

def get_message(msg_key):
    return messages[msg_key]

if __name__ == '__main__':
    app.run(debug=True)