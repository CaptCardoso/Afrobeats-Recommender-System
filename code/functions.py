import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import pandas as pd

#Authentication
client_credentials_manager = SpotifyClientCredentials(client_id = '2101cd224f5948e19c4c782d76744ed3', client_secret = '879abdfca432449facc9d8566fb40ab6')

#create a spotipy object
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_track_info(playlist):
    
    #split the playlist_uri is at the end of the playlists url. I'll use the .split method to extract it
    uri = playlist.split("/")[-1].split("?")[0]
    
    #from the spotipy library, use the playlist_tracks() method to extract each track from the playlist uri
    #It comes in a nested dictionary format
    
    results = sp.playlist_tracks(uri)
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    
    #create an empty dictionary with the info we want to extract as columns
    info = {
    'track_uri':[],
    'track_name':[],
    'artist_name':[],
    'artist_info':[],
    'artist_uri':[],
    'artist_popularity':[],
    'artist_genre':[],
    'album':[],
    'track_pop':[],
    }
    
    features = {'danceability': [],
     'energy': [],
     'key': [],
     'loudness': [],
     'mode': [],
     'speechiness': [],
     'acousticness': [],
     'instrumentalness': [],
     'liveness': [],
     'valence': [],
     'tempo': [],
     'type': [],
     'id': [],
     'uri': [],
     'track_href': [],
     'analysis_url': [],
     'duration_ms': [],
     'time_signature': []
               }
    
    #using a for loop, get the the info for each song and put it into the empty dictionary
    for track in tracks:
    
        #URI
        info['track_uri'].append((track["track"]["uri"]).split(':')[2])

        #Track name
        info['track_name'].append(track["track"]["name"])

        #Main Artist
        info['artist_uri'].append((track["track"]["artists"][0]["uri"]).split(':')[2])
        info['artist_info'].append(sp.artist(track["track"]["artists"][0]["uri"]))

        #Name, popularity, genre
        info['artist_name'].append(track["track"]["artists"][0]["name"])
        info['artist_popularity'].append(sp.artist(track["track"]["artists"][0]["uri"])["popularity"])
        info['artist_genre'].append(sp.artist(track["track"]["artists"][0]["uri"])["genres"])

        #Album
        info['album'].append(track["track"]["album"]["name"])

        #Popularity of the track
        info['track_pop'].append(track["track"]["popularity"])
        
        #Transform the info dictionary into a dataframe
        info_df = pd.DataFrame(info)
        
        #loop through the tracks to their features and assign it to the empty dictionary
        track_uri = track["track"]["uri"].split(':')[2] 
        
        try:
            for key,value in (sp.audio_features(track_uri)[0]).items():
                features[key].append(value)
            
        except:
            print(f'failed on track {track["track"]["name"]}')
            continue
        #time.sleep(1)
        
    #Transform the features dictionary into a dataframe
    features_df = pd.DataFrame(features)
 
    return info_df.join(features_df)

#This function gets the raw data from spotify function above and tags it
def raw_data(user_playlist_url, genre):
    user_playlist_info = get_track_info(user_playlist_url)
    #add user genre
    user_playlist_info.loc[:,'genre'] = genre
    return user_playlist_info


#