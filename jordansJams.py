'''Jams file that does all the heavy lifting'''
import os
import time
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.base import exceptions
from twilio.rest import Client
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from connect import Connect
from trackInfo import getTrackInfo

#add env vars to Heroku
def twilio_connect():
    '''twillio connect client'''
    twilioSID = os.environ['TWILIO_SID']
    twilioAuthToken = os.environ['TWILIO_AUTH']
    return Client(twilioSID, twilioAuthToken)

def spotify():
    '''spotify client connect'''
    client_credentials_manager = SpotifyClientCredentials()
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def default_message(number):
    '''sent whenever anyone texts non-keywords'''
    twilio_client = twilio_connect()
    message = "Thanks for being a subscriber! If you would like the current jams for the week text: \'JAMS\'"
    twilio_client.messages.create(
            to=number,
            from_="+14152124859",
            body=message)
    return "200 OK -- Message sent successfully."

def is_subscriber(phone_number):
    '''checks if number in mongo'''
    db = Connect.get_connection().jordansJams.numbers
    if db.find_one({"_id":phone_number}) is not None:
        return True
    return False

def new_user(phone_number):
    '''adds new number if not already in mongo'''
    db = Connect.get_connection()
    numbers = db.jordansJams.numbers
    numbers.insert_one({'_id':phone_number})
    twilio_client = twilio_connect()
    welcome = "Welcome to Jordan's Jams! Here you'll find Jordan's newest tunes every week. Every Wednesday you will get the songs Jordan has been jamming out to over the past 7 days. Here is what he's been listening to this week."
    twilio_client.messages.create(
            to=phone_number,
            from_="+14152124859",
            body=welcome)
    return get_jams(phone_number)

def remove_user(phone_number):
    '''method to remove a user from the subscriber list'''
    twilio_client = twilio_connect()
    message = "Sorry to see you go! Text anything back if you would like to re-subscribe and jam on."
    db = Connect.get_connection().jordansJams.numbers
    twilio_client.messages.create(
            to=phone_number,
            from_="+14152124859",
            body=message)
    db.delete_one({'_id': phone_number})

def get_jams(phone_number):
    '''method to get weekly songs and send to user'''
    db = Connect.get_connection().jordansJams
    twilio_client = twilio_connect()

    songs = db.songs.find()

    jam_count = songs.count()

    if jam_count < 1:
        sorry = "Sorry, unfortunately jams have not been added for this week. Check back later!"
        twilio_client.messages.create(
            to=phone_number,
            from_="+14152124859",
            body=sorry)
        return "Songs requested. No available. Please add more songs"


    intro = "Good morning! Jordan's top 2 jams for the week are:"

    twilio_client.messages.create(
            to=phone_number,
            from_="+14152124859",
            body=intro)

    for song in songs:
        track = song['track']
        artist = song['artist']
        link = song['link']
        message = track + " by: " + artist 
        twilio_client.messages.create(
            to=phone_number,
            from_="+14152124859",
            body=message)
        twilio_client.messages.create(
            to=phone_number,
            from_="+14152124859",
            body=link)
        time.sleep(2)

    return "Songs successfully sent."

def verify(request_number):
    '''method to verify if the sending number is the admin number'''
    twilio_client = twilio_connect()

    admin_num = os.environ['ADMIN_NUM']

    if request_number == admin_num:
        return True

    message_body = "Sorry, you are not authorized to add songs."
    twilio_client.messages.create(to=request_number, from_="+14152124859", body=message_body)
    return False

def clear_songs(request_number):
    '''method to clear songs from database'''
    db = Connect.get_connection()
    songs = db.jordansJams.songs

    #Create response to text back w/ twiml
    resp = MessagingResponse()

    #Clear all songs in database if more than 2 songs & message is 'clear'
    if songs.count() >= 2 and verify(request_number):
        songs.remove({ })
        message_body = "All jams have been cleared."
        resp.message(message_body)
        return str(resp)
    else:
        message_body = "Jams have already been cleared."
        resp.message(message_body)
        return str(resp)
    

def add_songs(request_number, request_message, session_count):
    '''method to adds the weekly songs to the db'''

    number = request_number

    db = Connect.get_connection()
    songs = db.jordansJams.songs

    #Create response to text back w/ twiml
    resp = MessagingResponse()
    just_sent = False

    #check if song already exists in database
    if "open.spotify.com" in request_message:
        track = getTrackInfo(request_message)
        if songs.find_one({"uri":track['uri']}) is not None:
            message_body = "That song has already been added. Please add another."
            resp.message(message_body)
            return str(resp)
                 
    #add song to database
    if "open.spotify.com" in request_message and session_count >= 1:
        parsed_track = getTrackInfo(request_message)
        songs.insert_one(parsed_track)
        uri = parsed_track['uri']
        sp = spotify()
        sp.user_playlist_add_tracks(playlist_id='6MfEs3eSEY27X5QOzioqW8', items=["spotify:track:{}".format(uri)], position=None)
        just_sent = True

    if session_count >= 1 and verify(number):
        if songs.count() == 0:
            message_body = "Please send in your 2 songs for the week."
            resp.message(message_body)
            return str(resp)
        elif songs.count() == 1 and verify(number):
            message_body = "Please send in your 2nd song."
            resp.message(message_body)
            return str(resp)
        elif songs.count() == 2 and verify(number) and just_sent:
            message_body = "Thanks for sending in your weekly songs!"
            just_sent = False
            resp.message(message_body)
            return str(resp)
        else:
            message_body = "There are 2 songs currently in the database. Would you like to clear? If so, type CLEAR"
            resp.message(message_body)
            return str(resp)

    resp.message("Error adding weekly songs. Please check for maintenance.")
    return str(resp)

def notify_jordan():
    '''sends message to jordan for weekly jams'''
    print("Notifying Jordan -- Weekly Jams request should be sent shortly.")
    twilio_client = twilio_connect()
    admin_num = os.environ['ADMIN_NUM']
    message_body = "Hey Jordan! It's time to submit your weekly jams."
    twilio_client.messages.create(to=admin_num, from_="+14152124859", body=message_body)
    clear_songs(admin_num)