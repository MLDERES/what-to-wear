import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode



app = Flask(__name__)
# This defines the endpoint where to get to the handler
ask = Ask(app, "/")

# for flask in particular this is the way to build out the web
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def launch():
    pass

@ask.intent("YesIntent")
def next_round():

    numbers = [randint(0, 9) for _ in range(3)]

    round_msg = render_template('round', numbers=numbers)

    session.attributes['numbers'] = numbers[::-1]  # reverse

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

def answer(first, second, third):

    winning_numbers = session.attributes['numbers']

    if [first, second, third] == winning_numbers:

        msg = render_template('win')

    else:

        msg = render_template('lose')

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)