import os
import spotipy
import spotipy.util as util


#Authorization of Spotify Credentials
token = util.oauth2.SpotifyClientCredentials(client_id=os.environ['SPOT_ID'], client_secret=os.environ['SPOT_SECRET'])
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

def getURI(spotifyURL):
    return ("spotify:track:" + spotifyURL.replace('https://', '').split('/')[2].split('?')[0])

def getTrackInfo(uri):
    return spotify.track(uri)

def parseTrack(uri, url):
    spotifyLink = url
    track = getTrackInfo(uri)
    trackName =  track['name']
    artistName = track['artists'][0]['name']
    return {"uri":uri, "track":trackName, "artist":artistName, "link":spotifyLink}