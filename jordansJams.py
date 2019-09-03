import os
from flask import Flask, session
from flask_pymongo import PyMongo
from pymongo import MongoClient
from connect import Connect
from twilio.rest import Client
from twilio.base import exceptions

#add env vars to Heroku
def twilioConnect():
    twilioSID = os.environ['TWILIO_SID']
    twilioAuthToken = os.environ['TWILIO_AUTH']
    return Client(twilioSID, twilioAuthToken)

#workOn
def is_subscriber(phoneNumber):
    db = mongoConnect()
    number = db.find({"Numbers": phoneNumber})
    if(number.count() != 0):
        return True
    return False

#Work on
def newUser():
    db = mongoConnect()
    numberCollection = db['jordans-jams']['Numbers']
    numberCollection.insert({'phoneNumber':phoneNumber})
    return getJams(newUser = true)

#work On
def addSongs():
    verified = False
    number = request.form['From']

    db = Connect.get_connection()
    numbers = db.jordansJams.numbers
    songs = db.jordansJams.songs

    counter = session.get('counter', 0)
    counter += 1
    session['counter'] = counter

    #Create response to text back w/ twiml
    resp = MessagingResponse()
    
    if number == '+18478484251':
        verified = True
    
    if counter >= 1 and verified:
        if songs.count() == 0:
            message_body = "Please send in your 2 songs for the week."
            resp.message(message_body)
            return str(resp)
        elif songs.count() == 1:
            message_body = "Please send in your 2nd song."
            resp.message(message_body)
            return str(resp)
        elif songs.count == 2:
            message_body = "Thanks for sending in your weekly songs!"
            resp.message(message_body)
            return str(resp)
        else:
            message_body = "You already have 2 songs. Would you like to clear? If so, type CLEAR"
            resp.message(message_body)
            return str(resp)