import os
import spotipy
import spotipy.util as util


def getTrackInfo(url):
    #Authorization of Spotify Credentials
    token = util.oauth2.SpotifyClientCredentials(client_id=os.environ['SPOT_ID'], client_secret=os.environ['SPOT_SECRET'])
    cache_token = token.get_access_token()
    spotify = spotipy.Spotify(cache_token)

    #Connect to Spotify
    spotifyLink = url
    track = spotify.track(url)
    trackName =  track['name']
    artistName = track['artists'][0]['name']
    uri = track['uri']
    return {"uri":uri, "track":trackName, "artist":artistName, "link":spotifyLink}