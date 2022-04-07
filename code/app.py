from operator import mod
import streamlit as st
import pickle
import time


st.set_page_config(
    page_title='Afrobeats Recommeder'
)

st.title('Afrobeats Recommendation System')


st.sidebar.subheader('Enter Spotify playlist URL below')

st.sidebar.text_input('url')

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