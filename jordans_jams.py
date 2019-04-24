
import os
from flask import Flask, session
from flask_pymongo import PyMongo
from pymongo import MongoClient

def mongoConnect():
    user = os.environ['MDB_USERNAME']
    password = os.environ['MDB_PASSWORD']
    mongoLink = os.environ['MDB_LINK']
    return MongoClient("mongodb+srv://"+user+":"+password+"@"+mongoLink)

def newUser():

    #Create a response to text back w/ twiml
    resp = MessagingResponse()

    #open up number database and add phone number
    numbers = mongo.db.numbers
    number = request.form['From']

    #try to add the number, if it already exists then
    #send a message back that they are already subscribed
    #
    #If not, then add them 
    try:
        numbers.insert({'_id': request.form['From']})
    except:
        message_body = 'You are already subscribed to Jordan\'s Jams. Look out for new songs to come!'
        resp.message(message_body)
        return str(resp)
    message_body = 'Thanks for subscribing to Jordan\'s Jams. Text TUNES if you would like this weeks currently songs.'
    resp.message(message_body)

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
        



def getTunes():
    #Create response to text the link w/ twiml
    resp = MessagingResponse()

    #Open up phone and song database
