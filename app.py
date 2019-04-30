import constant, os
from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from jordans_jams import jordansJams, is_subscriber, removeUser, newUser

app = Flask(__name__)

@app.route('/jordans-jams', methods=['POST', 'GET'])
def response():
    
    resp = MessagingResponse()

    inboundNumber = request.form['From']
    inboundMessage = request.form['Body']

    removalKeys = ["STOP", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"]

    #Key Words for Jordan's Jams
    

    return {
        'SUBSCRIBE': newUser()
        'ADD SONGS': initiateSongs()
    }[keyword]

if __name__ == '__main__':
    app.run(debug=True)

#start ngrok server: ngrok http 5000
#start python server: Python mongo_conect.py
#Twilio app should be up and running after that