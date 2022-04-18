from hashlib import new
from operator import mod
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import plotly.express as px
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import pairwise_distances, cosine_distances, cosine_similarity
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
# <--- end of imports --->

# <--- Spotify API authentications --->
#Authentication
client_credentials_manager = SpotifyClientCredentials(client_id = '2101cd224f5948e19c4c782d76744ed3', client_secret = '879abdfca432449facc9d8566fb40ab6')

#create a spotipy object
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#import afrobeats playlist
afrobeats_playlist = pd.read_csv('streamlit/afrobeats.csv')

# <--- Function definitions --->
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

# <--- End of function definitions --->
#set page config
st.set_page_config(
    page_title='Afrobeats Recommeder System')

# <--- Side bar --->
#option 1
st.sidebar.subheader('Option 1')

#form to enter playlist url
playlist_url = st.sidebar.text_input('Enter Playlist URL')

#create enter button
recommend_button = st.sidebar.button(label='Recommend Songs')

# <--- Sliders --->
#option2

st.sidebar.subheader('Option 2')

def slider_value():
    danceability = st.sidebar.slider('Danceability',0.0,0.97)
    energy = st.sidebar.slider('Energy',0.174,0.995)
    loudness = st.sidebar.slider('Loudness',-21.272,0.995)
    # mode = st.sidebar.slider('Mode',0.0,1.0)
    # speechiness = st.sidebar.slider('Speechiness',0.0,0.55)
    # acousticness = st.sidebar.slider('Acousticness',0.000294,0.976)
    instrumentalness = 	st.sidebar.slider('Instrumentalness',0.0,0.888)
    # liveness = st.sidebar.slider('Liveness',0.0218,0.879)
    # valence = st.sidebar.slider('Valence',0.0,0.981)
    tempo = st.sidebar.slider('Tempo',0.0,233.936)

    res_dict = {'danceability': danceability,
                'energy': energy,
                #'acousticness': acousticness,
                'instrumentalness': instrumentalness,
               #'liveness': liveness,
                'loudness': loudness,
                #'speechiness': speechiness,
                'tempo': tempo,
                #'valence': valence
                'track_name': 'user',
                'genre': 'user' }

    res_df = pd.DataFrame(res_dict, index=[0])
    return res_df

slider = slider_value()
slider_button = st.sidebar.button('Recommend Song')

# chill = st.sidebar.button(label='Chill')
# high_energy = st.sidebar.button(label='High Energy')
# instrumental = st.sidebar.button(label='Instrumental')
# top_ten = st.sidebar.button(label='Top Ten')
# my_recommendation = st.sidebar.button(label='My Recommendations')
# <--- end of side bar --->

# <--- main page --->

st.title('Afrobeats Recommendation System')

if recommend_button:
        
    #Get the uri from the url
    playlist_uri = playlist_url.split("/")[-1].split("?")[0]
    user_playlist = raw_data(playlist_uri, 'user')

    #concat user_playlist and afrobeats_playlist
    df = pd.concat([afrobeats_playlist, user_playlist])
    df.reset_index(inplace=True, drop=True)

    #create features and define X     
    features = ['danceability','energy','loudness','instrumentalness','tempo']
    X = df[features]

    #<-- clustering -->
    #setup pipeline for kmeans
    # pipeline = Pipeline([
    #                 ('scaler', StandardScaler()), 
    #                 ('kmeans', KMeans(n_clusters=4))
    # ])

    # #fit X 
    # pipeline.fit(X)
    # df['cluster'] = pipeline.predict(X)

    #<-- Dimensionality reduction -->
    #set up pipline for TSNE 
    #TSNE reduces it into two dimensions for good vizualization
    # pipeline = Pipeline([
    #     ('scaler', StandardScaler()),
    #     ('tsne', TSNE(n_components=2, verbose=False))
    # ])
    # X_tnse = pipeline.fit_transform(X)

    # #create a dataframe of the 2-D features
    # tsne_df = pd.DataFrame(columns=['x', 'y'], data=X_tnse)
    # tsne_df['genre'] = df['genre']
    # #tsne_df['cluster'] = df['cluster']
    # tsne_df['track_name'] = df['track_name']

    #PCA
    pipeline_pca = Pipeline([
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=2))
    ])
    pipeline_pca.fit(X)
    #create a dataframe of the 2-D features
    pca_df=pd.DataFrame(pipeline_pca.transform(X), columns=['x','y'])
    pca_df['genre'] = df['genre']
    #pca_df['cluster'] = df['cluster']
    pca_df['track_name'] = df['track_name']

    #<-- Euclidean distance -->
    dist = cdist(pca_df[['x','y']],pca_df[['x','y']])
    recommender_df = pd.DataFrame(dist,
                            columns=df['track_name'],
                            index=df['track_name']).drop(user_playlist['track_name'])

    #get recommendation
    top_df = pd.DataFrame(columns=df.columns)
    top_list = []

    #Get song from users playlis
    for track in user_playlist['track_name']:    
    
        for count in range(len(df)): 
            most_similar = recommender_df[track].sort_values(ascending=True).index[count]
        
            #check if song has already been recommended
            if most_similar in top_list:
                continue
        
            else:
                top_list.append(most_similar)
                break

        #create a dataframe of the recommended songs
        top_df = pd.concat([top_df, df[df['track_name']==most_similar]])

    #<-- visialization using plotly -->
    fig = px.scatter(pca_df, x='x', y='y',color='genre',color_discrete_sequence=['green','red'],hover_name='track_name')
    st.plotly_chart(fig, use_container_width=True)

    #<-- output the topten songs -->
    for track_uri in top_df['track_uri']:
        components.iframe("https://open.spotify.com/embed/track/"+track_uri+"?utm_source=generator")



        #output the recommended songs
        #st.write(playlist_data['track_name'])
elif slider_button:
    #concat user_playlist and afrobeats_playlist
    df = pd.concat([afrobeats_playlist, slider])
    df.reset_index(inplace=True, drop=True)

    #create features and define X     
    features = ['danceability','energy','loudness','instrumentalness','tempo']
    X = df[features]

    #<-- clustering -->
    #setup pipeline for kmeans
    # pipeline = Pipeline([
    #                 ('scaler', StandardScaler()), 
    #                 ('kmeans', KMeans(n_clusters=4))
    # ])

    # #fit X 
    # pipeline.fit(X)
    # df['cluster'] = pipeline.predict(X)

    #<-- Dimensionality reduction -->
    #set up pipline for TSNE 
    #TSNE reduces it into two dimensions for good vizualization
    # pipeline = Pipeline([
    #     ('scaler', StandardScaler()),
    #     ('tsne', TSNE(n_components=2, verbose=False))
    # ])
    # X_tnse = pipeline.fit_transform(X)

    # #create a dataframe of the 2-D features
    # tsne_df = pd.DataFrame(columns=['x', 'y'], data=X_tnse)
    # tsne_df['genre'] = df['genre']
    # #tsne_df['cluster'] = df['cluster']
    # tsne_df['track_name'] = df['track_name']

    #PCA
    pipeline_pca = Pipeline([
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=2))
    ])
    pipeline_pca.fit(X)
    #create a dataframe of the 2-D features
    pca_df=pd.DataFrame(pipeline_pca.transform(X), columns=['x','y'])
    pca_df['genre'] = df['genre']
    #pca_df['cluster'] = df['cluster']
    pca_df['track_name'] = df['track_name']

    #<-- Euclidean distance -->
    dist = cdist(pca_df[['x','y']],pca_df[['x','y']])
    recommender_df = pd.DataFrame(dist,
                            columns=df['track_name'],
                            index=df['track_name']).drop(slider['track_name'])

    #get recommendation
    top_df = pd.DataFrame(columns=df.columns)
    top_list = []

    #Get song from users playlis
    for track in slider['track_name']:    
    
        for count in range(len(df)): 
            most_similar = recommender_df[track].sort_values(ascending=True).index[count]
        
            #check if song has already been recommended
            if most_similar in top_list:
                continue
        
            else:
                top_list.append(most_similar)
                break

        #create a dataframe of the recommended songs
        top_df = pd.concat([top_df, df[df['track_name']==most_similar]])

    #<-- visialization using plotly -->
    fig = px.scatter(pca_df, x='x', y='y',color='genre',color_discrete_sequence=['green','red'],hover_name='track_name')
    st.plotly_chart(fig, use_container_width=True)

    #<-- output the topten songs -->
    for track_uri in top_df['track_uri']:
        components.iframe("https://open.spotify.com/embed/track/"+track_uri+"?utm_source=generator")


    #st.write(slider)


else:
    st.subheader('My recommended Afrobeat playlist')
    components.iframe("https://open.spotify.com/embed/playlist/7aPeucRdbg7Bbt7TIGMiui", width=700, height=600)
     
