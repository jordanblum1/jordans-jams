from flask import Flask, request, session
from flask_pymongo import PyMongo
from pymongo import MongoClient
from connect import Connect
from twilio.twiml.messaging_response import Message, MessagingResponse
from jordansJams import addSongs, getJams, clearSongs

SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

mongo = Connect.get_connection()
numbers = mongo.jordansJams.numbers

@app.route('/')
def index():
    return "Up and Running!!"

@app.route('/jams', methods=['POST'])
def sms():

    counter = session.get('counter', 0)
    counter += 1
    session['counter'] = counter

    resp = MessagingResponse()
    number = request.form['From']
    inboundMessage = request.form['Body']

    if inboundMessage == "ADD" and counter >= 1:
        return addSongs(number, inboundMessage, counter)
    if inboundMessage == "CLEAR":
        return clearSongs(number)
    if inboundMessage == "JAMS":
        return getJams(number)

    message_body = 'Error, that is not a possible entry.'
    resp.message(message_body)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)