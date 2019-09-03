from flask import Flask, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from connect import Connect
from twilio.twiml.messaging_response import Message, MessagingResponse
from jordansJams import addSongs


app = Flask(__name__)

mongo = Connect.get_connection()
numbers = mongo.jordansJams.numbers

@app.route('/sms', methods=['POST'])
def sms():
    resp = MessagingResponse()
    number = request.form['From']
    inboundMessage = request.form["Body"]

    try:
        numbers.insert_one({'_id': number})
    except:
        message_body = 'You are already subscribed to Jordan\'s Jams. Look out for new songs to come!'
        resp.message(message_body)
        return str(resp)

    message_body = 'Thanks for subscribing to Jordan\'s Jams. Text TUNES if you would like this weeks currently songs.'
    resp.message(message_body)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)