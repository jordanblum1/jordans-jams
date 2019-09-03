import os
import time
from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from connect import Connect
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.base import exceptions
from twilio.rest import Client

#add env vars to Heroku
def twilioConnect():
    #twilioSID = os.environ['TWILIO_SID']
    #twilioAuthToken = os.environ['TWILIO_AUTH']
    return Client('AC0ed1eb8b97d3465050670f36b2f3e03f', '343e9844b3ad99c3eb22fca94bf57ba7')

def is_subscriber(phoneNumber):
    db = Connect.get_connection().numbers
    if db.find_one({"numbers": phoneNumber}) != None:
        return True
    return False

def newUser():
    db = Connect.get_connection()
    numbers = db.jordansJams.numbers
    numbers.insert_one({'phoneNumber':phoneNumber})
    return getJams(newUser = true)

def removeUser(phoneNumber):
    db = Connect.get_connection().jordansJams.numbers
    db.delete_one({'phoneNumber': phoneNumber})

def getJams(phoneNumber):

    db = Connect.get_connection().jordansJams
    twilioClient = twilioConnect()

    songs = db.songs.find()
    message = "Hello! Here are the newest jams for this week: "

    twilioClient.messages.create(
            to=phoneNumber,
            from_="+14152124859",
            body=message)

    time.sleep(1)

    for song in songs:
        link = '{0}'.format(song['songLink'])
        twilioClient.messages.create(
            to=phoneNumber,
            from_="+14152124859",
            body=link)
        time.sleep(.5)

    return "Songs successfully sent."

def verify(requestNumber):
    #verify if this is an Admin phone number
    #mask this later
    if requestNumber == '+18478484251':
        return True
    else:
        message_body = "Sorry, you are not authorized to add songs."
        twilioClient.messages.create(to=requestNumber, from_="+14152124859", body=message_body)
        return False

def clearSongs(requestNumber):
    db = Connect.get_connection()
    numbers = db.jordansJams.numbers
    songs = db.jordansJams.songs

    #Create response to text back w/ twiml
    resp = MessagingResponse()

    #Clear all songs in database if more than 2 songs & message is 'clear'
    if songs.count >= 2 and verify(requestNumber):
        songs.remove({ })
        message_body = "All songs have been cleared."
        resp.message(message_body)
        return str(resp)
    

def addSongs(requestNumber, requestMessage, sessionCount):

    number = requestNumber

    db = Connect.get_connection()
    numbers = db.jordansJams.numbers
    songs = db.jordansJams.songs

    #Create response to text back w/ twiml
    resp = MessagingResponse()

    #check if song already exists in database
    if songs.find_one({"songLink":requestMessage}) != None:
        message_body = "That song has already been added. Please add another."
        resp.message(message_body)
        return str(resp)
        
    #add song to database
    if "open.spotify.com" in requestMessage and sessionCount >= 1:
        songs.insert_one({"songLink":requestMessage})
        print "Added song"
    
    if sessionCount >= 1 and verify(number):
        if songs.count() == 0:
            message_body = "Please send in your 2 songs for the week."
            resp.message(message_body)
            return str(resp)
        elif songs.count() == 1 and verify(number):
            message_body = "Please send in your 2nd song."
            resp.message(message_body)
            return str(resp)
        elif songs.count() == 2 and verify(number):
            message_body = "Thanks for sending in your weekly songs!"
            resp.message(message_body)
            print sessionCount
            return str(resp)
        else:
            message_body = "There are 2 songs currently in the database. Would you like to clear? If so, type CLEAR"
            resp.message(message_body)
            return str(resp)

    resp.message("Error adding weekly songs. Please check for maintenance.")
    return str(resp)