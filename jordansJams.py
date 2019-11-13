import os
import time
from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from connect import Connect
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.base import exceptions
from twilio.rest import Client
from trackInfo import getURI, parseTrack

#add env vars to Heroku
def twilioConnect():
    twilioSID = os.environ['TWILIO_SID']
    twilioAuthToken = os.environ['TWILIO_AUTH']
    return Client(twilioSID, twilioAuthToken)

def default_message(number):
    twilioClient = twilioConnect()
    message = "Thanks for being a subscriber! If you would like the current jams for the week text: \'JAMS\'"
    twilioClient.messages.create(
            to=number,
            from_="+14152124859",
            body=message)
    return "200 OK -- Message sent successfully."

def is_subscriber(phoneNumber):
    db = Connect.get_connection().jordansJams.numbers
    if db.find_one({"_id":phoneNumber}) != None:
        return True
    return False

def newUser(phoneNumber):
    db = Connect.get_connection()
    numbers = db.jordansJams.numbers
    numbers.insert_one({'_id':phoneNumber})
    twilioClient = twilioConnect()
    welcome = "Welcome to Jordan's Jams! Here you'll find Jordan's newest tunes every week. Every Wednesday you will get the songs Jordan has been jamming out to over the past 7 days. Here is what he's been listening to this week."
    twilioClient.messages.create(
            to=phoneNumber,
            from_="+14152124859",
            body=welcome)
    return getJams(phoneNumber)

def removeUser(phoneNumber):
    twilioClient = twilioConnect()
    message = "Sorry to see you go! Text anything back if you would like to re-subscribe and jam on."
    db = Connect.get_connection().jordansJams.numbers
    twilioClient.messages.create(
            to=phoneNumber,
            from_="+14152124859",
            body=message)
    db.delete_one({'_id': phoneNumber})

def getJams(phoneNumber):

    db = Connect.get_connection().jordansJams
    twilioClient = twilioConnect()

    songs = db.songs.find()

    jamCount = songs.count()

    if jamCount < 1:
        sorry = "Sorry, unfortunately jams have not been added for this week. Check back later!"
        twilioClient.messages.create(
            to=phoneNumber,
            from_="+14152124859",
            body=sorry)
        return "Songs requested. No available. Please add more songs"


    intro = "This weeks newest jams are:"

    twilioClient.messages.create(
            to=phoneNumber,
            from_="+14152124859",
            body=intro)

    time.sleep(1)

    for song in songs:
        track = song['track']
        artist = song['artist']
        link = song['link']
        message = track + " by: " + artist 
        twilioClient.messages.create(
            to=phoneNumber,
            from_="+14152124859",
            body=message)
        twilioClient.messages.create(
            to=phoneNumber,
            from_="+14152124859",
            body=link)
        time.sleep(.5)

    return "Songs successfully sent."

def verify(requestNumber):
    #verify if this is an Admin phone number
    #mask this later
    twilioClient = twilioConnect()

    adminNum = os.environ['ADMIN_NUM']
	
    if requestNumber == adminNum:
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
    if songs.count() >= 2 and verify(requestNumber):
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
    justSent = False

    #check if song already exists in database
    if "open.spotify.com" in requestMessage and songs.find_one({"uri":getURI(requestMessage)}) != None:
        message_body = "That song has already been added. Please add another."
        resp.message(message_body)
        return str(resp)
        
    #add song to database
    if "open.spotify.com" in requestMessage and sessionCount >= 1:
        uri = getURI(requestMessage)
        parsedTrack = parseTrack(uri, requestMessage)
        songs.insert_one(parsedTrack)
        justSent = True
    

    if sessionCount >= 1 and verify(number):
        if songs.count() == 0:
            message_body = "Please send in your 2 songs for the week."
            resp.message(message_body)
            return str(resp)
        elif songs.count() == 1 and verify(number):
            message_body = "Please send in your 2nd song."
            resp.message(message_body)
            return str(resp)
        elif songs.count() == 2 and verify(number) and justSent:
            message_body = "Thanks for sending in your weekly songs!"
            justSent = False
            resp.message(message_body)
            return str(resp)
        else:
            message_body = "There are 2 songs currently in the database. Would you like to clear? If so, type CLEAR"
            resp.message(message_body)
            return str(resp)

    resp.message("Error adding weekly songs. Please check for maintenance.")
    return str(resp)

def notifyJordan():
    twilioClient = twilioConnect()
    adminNum = os.environ['ADMIN_NUM']
    message_body = "Hey Jordan! It's time to submit your weekly jams."
    twilioClient.messages.create(to=adminNum, from_="+14152124859", body=message_body)