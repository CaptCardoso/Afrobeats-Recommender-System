# Spotify Afrobeats Recommendation System

*By Afolabi Cardoso*

---

The popularity of West African music commonly called Afrobeats has increased tremendously as a result of social media. Everyday there seems to be a new tiktok challenge being created with the latest Afrobeats song.

By using distance matrix and kmeans clustering, I have created a recommender system that will create an Afrobeats playlist based on the songs in the users spotify playlist.

This recommender system helps to guide newcomers into the world of Afrobeat.

---
## Contents

[Brief History of Afrobeats](#Brief-History-of-Afrobeats) | [Data](#Data) | [Methodology](#Methodology) | [Feature Engineering](#Feature-Engineering) |  [EDA](#EDA) | [Modeling](#Modeling) | [Streamlit](#Streamlit) | [Conclusion](#Conclusion) | [Recommendations](#Recommendations) | [References](#References)

---
## Brief History of Afrobeats

### Origins
Afrobeats (not to be confused with Afrobeat or Afroswing), also known as Afro-pop, Afro-fusion (also styled as Afropop and Afrofusion), is an umbrella term to describe popular music from West Africa and the diaspora that initially developed in Nigeria, Ghana, and the UK in the 2000s and 2010s. Afrobeats is less of a style per se, and more of a descriptor for the fusion of sounds flowing out of Ghana and Nigeria. Genres such as hiplife, jùjú music, highlife and naija beats, among others, were amalgamated under the 'afrobeats' umbrella.

Afrobeats is primarily produced in Lagos, Accra, and London. 

Afrobeats (with the s) is commonly conflated with and referred to as Afrobeat (without the s), however, these are two distinct and different sounds and are not the same. Afrobeat is a genre that developed in the 1960s and 1970s, taking influences from Fuji music and Highlife, mixed in with American jazz and funk. Characteristics of Afrobeat include big bands, long instrumental solos, and complex jazzy rhythms. The name was coined by Nigerian afrobeat pioneer **Fela Kuti**. Fela Kuti and his longtime partner, drummer Tony Allen, are credited for laying the groundwork for what would become afrobeats.

This is in contrast to the afrobeats sound, pioneered in the 2000s and 2010s. While afrobeats takes on influences from Afrobeat, it is a diverse fusion of various different genres such as British house music, hiplife, hip hop, dancehall, soca, Jùjú music, highlife, R&B, Ndombolo, Naija beats, Azonto, and Palm-wine music. Unlike Afrobeat, which is a clearly defined genre, afrobeats is more of an overarching term for contemporary West African pop music. The term was created in order to package these various sounds into a more easily accessible label, which were unfamiliar to the UK listeners where the term was first coined. Another, more subtle contrast between the two sounds, is that while Fela Kuti used his music to discuss and criticise contemporary politics, afrobeats typically avoids such topics, thereby making it less politically charged than afrobeat.

### Sound

Afrobeats is most identifiable by its signature driving drum beat rhythms, whether electronic or instrumental. These beats harken to the stylings of a variety of traditional African drum beats across West Africa as well as the precursory genre Afrobeat. The beat in Afrobeats music is not just a base for the melody, but acts as a major character of the song, taking a lead role that is sometimes equal to or of greater importance than the lyrics and almost always more central than the other instrumentals. Afrobeats share a similar momentum and tempo to house music. Usually using the 4/4 time signature common in Western music, afrobeats commonly features a 3–2 or 2–3 rhythm called a clave. Another distinction within Afrobeats is the notably West African, specifically Nigerian or Ghanaian, accented English that is often blended with local slangs, pidgin English, as well as local Nigerian or Ghanaian languages depending on the backgrounds of the performers.

Sampling is sometimes used within Afrobeats music. Burna Boy and Wizkid, for example, have both sampled Fela Kuti.

*Source: [Wikipedia: Afrobeats](https://en.wikipedia.org/wiki/Afrobeats)*

---
## DATA

In putting together the Afrobeats playlist, I used the Spotify music streaming service. 
I selected Afrobeats songs mainly from Ghana and Nigeria ranging from the year 2000 to 2022. The playlist has a wide range of sub-genres such as Afropop, Azonto, Afro-fusion etc. The [Spotify](https://developer.spotify.com/documentation/web-api/quick-start/) API is a music streaming service that has a well detailed API. The [Spotify](https://developer.spotify.com/documentation/web-api/quick-start/) API provides musical features that can be used for analysis, such as danceability, energy, acoustics etc. Full description of the features can be found in the [Spotify Docs](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features)

---
## Methodology

#### Getting the data

To make the API call, I am using the [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/) library to fetch the track features from the [Spotify](https://developer.spotify.com/documentation/web-api/quick-start/) API.

Spotipy is a lightweight Python library for the Spotify Web API. With Spotipy you get full access to all of the music data provided by the Spotify platform.

Source: [Spotipy docs](https://spotipy.readthedocs.io/en/2.19.0/)

#### Featuture Engineering

Not a lot of feature engineering was required because the Spoity library is very well structured.

I did have to perform standard scaler on the features before performing kmeans clustering

#### EDA

I did a scatter plot matrix of all 10 musical features to see which features will be useful in creating clusters. I found that loudness, energy and danceability all had strong correlations. I will use these attributes in creating clusters.

![plot](../images/newplot.png)

The silhoutte score and elbow plot all pointed to 4 as the best number to cluster the tracks.

To further analyse the features, I plotted a time series chart to see how the features has changed over the years

#### Modeling
To have a better visualization of the data, I had to apply a form of dimensionality reduction on the features. I tested out both PCA and TSNE to see which does a better job in reducting all 10 features into 2 dimensions while maintaing the clusters.

**TSNE** which stands for T-distributed Stochastic Neighbor Embedding is a tool to visualize high-dimensional data. It converts similarities between data points to joint probabilities and tries to minimize the Kullback-Leibler divergence between the joint probabilities of the low-dimensional embedding and the high-dimensional data. t-SNE has a cost function that is not convex, i.e. with different initializations we can get different results.

Source: [sklearn docs](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html)

TSNE did a great job in creating a 2D scatter plot, however it took too long to run. To improve performance for my app, I will use PCA as a dimensionality reduction tool.

---
## Streamlit

In order to create a more practical use of my recommendation system, I created a streamlit app.

Access it here: [streamlit](https://share.streamlit.io/captcardoso/afrobeats-recommender-system/streamlit/app.py)



---
## Conclusion

TSNE is a great tool for visualizing high dimensional data, however when used in an App it slows performance 

---
## Recommendations and Next Steps

Build a more interactive app with Flask or Django

Create a recommender that's flexible for all genres not only Afrobeats

---
## References

- [Spotify Dedup](https://spotify-dedup.com/): I used this web app to remove duplicates from my spotifly playlist
- [James Okai](https://open.spotify.com/user/21rd54k5ww3pisr36mqx27duq): He has a wonderful catelogue of afrobeats music updated regularly on spotify. 
- [Extracting Song Data From the Spotify API Using Python](https://towardsdatascience.com/extracting-song-data-from-the-spotify-api-using-python-b1e79388d50): This article was essential in helping me understand the functionality of the Spotify API. *Written by [Cameron Watts](https://cameronwwatts.medium.com/)*