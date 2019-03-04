from twilio.rest import Client


#This is the information that allows twilio api to connect to my account
account = "AC0ed1eb8b97d3465050670f36b2f3e03f"
token = "343e9844b3ad99c3eb22fca94bf57ba7"
client = Client(account, token)

#Spotify account credentials
spotifyId = "12269f2380624428bc0d8d4feb824939"
spotifySecret= "db39f3309e3148a4974fad5824f11e5d"

bodySong = "https://api.spotify.com/v1/playlists/3tIKt09tCSqYW5I3Msh4mm/tracks"

#This is where the logic message should go
message = client.messages.create(to="+18478484251", from_="+14152124859",
                                 body=bodySong)