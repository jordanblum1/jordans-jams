
import os
from flask import Flask, session
from flask_pymongo import PyMongo
from pymongo import MongoClient
from twilio.rest import Client

#connect to database that stores both the jams and the phone numbers
def mongoConnect():
    user = os.environ['MDB_USERNAME']
    password = os.environ['MDB_PASSWORD']
    mongoLink = os.environ['MDB_LINK']
    return MongoClient("mongodb+srv://"+user+":"+password+"@"+mongoLink)

#connect to twilio api & account
def twilioConnect():
    twilioSID = os.environ['TWILIO_SID']
    twilioAuthToken = os.environ['TWILIO_AUTH']
    return Client(twilioSID, twilioAuthToken)
    
def jordansJams():
    twilioClient = twilioConnect()
    db = mongoConnect()
    jamsDB = db['jordans-jams']

    #add logic to send out the jams baby

def is_subscriber(phoneNumber):
    db = mongoConnect()
    number = db.find({"Numbers": phoneNumber})


    if(number.count() != 0):
        return True
    return False

def newUser():

    db = mongoConnect()
    numberCollection = db['jordans-jams']['Numbers']

    numberCollection.insert({'phoneNumber':phoneNumber})
    return getJams(newUser = true)

def removeUser(phoneNumber):
    db = mongoConnect()
    numberCollection = db['jordans-jams']
    db.Numbers.delete_one({'phoneNumber': phoneNumber})

def getJams():

    db = mongoConnect()
    jams = db['jordans-jams']









def addSongs():
    #cache the session
    counter = session.get('counter', 0)
    counter += 1
    session['counter'] = counter

    #Create response to text back w/ twiml
    resp = MessagingResponse()

    #Open database to check texting number if it is admin number
    #adding songs collection too
    numbers = mongo.db.numbers
    number = request.form['From']
    songs = mongo.db.songs
    
    if number == '+18478484251' and counter <= 0:
        print('Admin number verified.')
        

    if counter >= 1 and number == '+18478484251':
        if songs.db.dataSize() >= 2:
            message_body = 'There are already songs in the database. Want to overwrite'
            resp.message_body
    
