import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


def getTrackInfo(url):
    #Authorization of Spotify Credentials
    client_credentials_manager = SpotifyClientCredentials()
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    #Connect to Spotify
    spotifyLink = url
    track = spotify.track(url)
    trackName =  track['name']
    artistName = track['artists'][0]['name']
    uri = track['uri']
    return {"uri":uri, "track":trackName, "artist":artistName, "link":spotifyLink}