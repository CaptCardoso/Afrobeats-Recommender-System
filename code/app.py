from operator import mod
import streamlit as st
import pickle
import time
import functions as fn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

#Authentication
client_credentials_manager = SpotifyClientCredentials(client_id = '2101cd224f5948e19c4c782d76744ed3', client_secret = '879abdfca432449facc9d8566fb40ab6')

#create a spotipy object
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

st.set_page_config(
    page_title='Afrobeats Recommeder'
)

st.title('Afrobeats Recommendation System')


st.sidebar.subheader('Enter Spotify playlist URL below')

#enter playlist url
playlist_url = st.sidebar.text_input('url')

#Get the uri from the url
playlist_uri = playlist_url.split("/")[-1].split("?")[0]

try:
    playlist_data = fn.raw_data(playlist_uri, 'user')
    #output the recommended songs
    
    st.write(playlist_data['track_name'])
except:
    st.write('Something went wrong')
    print('Enter a valid playlist URL')



















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