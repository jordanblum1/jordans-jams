from flask import Flask, request, session, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
from connect import Connect
from twilio.twiml.messaging_response import Message, MessagingResponse
from jordansJams import verify, addSongs, getJams, clearSongs, is_subscriber, newUser, removeUser, twilioConnect, default_message

SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

mongo = Connect.get_connection()
numbers = mongo.jordansJams.numbers

@app.route('/')
def index():
    return render_template('jordansJams.html')

@app.route('/addFromWeb/<number>', methods = ['POST'])
def webAdd(number):
    return newUser(number)

@app.route('/jams', methods=['POST'])
def sms():

    resp = MessagingResponse()
    number = request.form['From']
    inboundMessage = (request.form['Body']).upper()

    counter = session.get('counter', 0)
    counter += 1
    session['counter'] = counter

    exit_words = ["STOP", "END", "UNSUBSCRIBE", "REMOVE"]
    if inboundMessage.upper() in exit_words:
        return removeUser(number)

    if inboundMessage == "CLEAR":
        session['counter'] = 0
        return clearSongs(number)
    if inboundMessage == "JAMS":
        return getJams(number)
    if (inboundMessage == "ADD") or (counter >= 1 and "open.spotify.com" in inboundMessage):
        if verify(number):
            return addSongs(number, inboundMessage, counter)
    if not is_subscriber(number):
        return newUser(number)
    if is_subscriber(number):
        return default_message(number)

    message_body = 'Error, that is not a possible entry.'
    resp.message(message_body)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)