from operator import mod
import streamlit as st
import streamlit.components.v1 as components
import pickle
import time
import functions as fn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
# <--- end of imports --->

# <--- Spotify API authentications --->
#Authentication
client_credentials_manager = SpotifyClientCredentials(client_id = '2101cd224f5948e19c4c782d76744ed3', client_secret = '879abdfca432449facc9d8566fb40ab6')

#create a spotipy object
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


# <--- Page layout setup --->
st.set_page_config(
    page_title='Afrobeats Recommeder System')

st.title('Afrobeats Recommendation System')

st.sidebar.subheader('Enter Spotify playlist URL below')


#enter playlist url
playlist_url = st.sidebar.text_input('')

#Get the uri from the url
playlist_uri = playlist_url.split("/")[-1].split("?")[0]

try:
    user_playlist = fn.raw_data(playlist_uri, 'user')

    #output the recommended songs
    #st.write(playlist_data['track_name'])
except:
    st.write('Something went wrong')


#import afrobeats playlist
afrobeats_playlist = pd.read_csv('../data/afrobeats.csv')

#concat user_playlist and afrobeats_playlist
df = pd.concat([afrobeats_playlist, user_playlist])
df.reset_index(inplace=True, drop=True)

#<-- clustering -->
#define X     
features = ['danceability','energy','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo']
X = df[features]

#setup pipeline for kmeans
pipeline = Pipeline([
                    ('scaler', StandardScaler()), 
                    ('kmeans', KMeans(n_clusters=6))
])

#fit X 
pipeline.fit(X)
df['cluster'] = pipeline.predict(X)

#<-- Dimensionality reduction -->
#set up pipline for TSNE 
#TSNE reduces it into two dimensions for good vizualization
pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('tsne', TSNE(n_components=2, verbose=False))
])
X_tnse = pipeline.fit_transform(X)


tsne_df = pd.DataFrame(columns=['x', 'y'], data=X_tnse)
tsne_df['genre'] = df['genre']
tsne_df['cluster'] = df['cluster']
tsne_df['track_name'] = df['track_name']

#<-- Cosine Similarity -->
similarities = cosine_similarity(X)
recommender_df = pd.DataFrame(similarities,
                              columns=df['track_name'],
                             index=df['track_name']).drop(user_playlist['track_name'])

top_ten_df = pd.DataFrame(columns=df.columns)
top_ten_list = []
    
#Get song from users playlis
for track in user_playlist['track_name']:    
        
    for count in range(len(df)): 
        most_similar = recommender_df[track].sort_values(ascending=False).index[count]
            
        #check if song has already been recommended
        if most_similar in top_ten_list:
            continue
            
        else:
            top_ten_list.append(most_similar)
            break
                
    #create a dataframe of the recommended songs
    top_ten_df = pd.concat([top_ten_df, df[df['track_name']==most_similar]])

#<-- visialization using plotly -->

fig = px.scatter(tsne_df, x='x', y='y',color='genre',color_discrete_sequence=['green','red'],hover_name='track_name')
st.plotly_chart(fig, use_container_width=True)

#<-- output the topten songs -->
for track_uri in top_ten_df['track_uri']:
    components.iframe("https://open.spotify.com/embed/track/"+track_uri+"?utm_source=generator")












# @st.cache
# def load_model():
#   with open('models/author_pipe.pkl', 'rb') as f:
#     the_model = pickle.load(f)
#   return the_model

# model = load_model()

# st.title('Which author is your muse?')

# st.subheader('Do you write like Jane Austen or Edgar Allan Poe?')

# txt = st.text_area('Write your prose here').strip()

# if st.button('Submit'):
#   if len(txt) > 0:
#     pred = model.predict([txt])[0]
#     probs = list(model.predict_proba([txt])[0])
#     prob = probs[0] if pred == 'Edgar Allan Poe' else probs[1]
#     st.write('You write like ', pred)
#     st.metric('Probability', f'{100 * round(prob, 2)}%')
#   else:
#     st.write('Too pithy. Try writing something.')