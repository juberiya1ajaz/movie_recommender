import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
import datetime

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d494e44caecb9d7d695a654d72f9d71d&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]
    
    recommended_movies=[]
    recommended_movies_posters =[]
    for i in movies_list:
       movie_id = movies.iloc[i[0]].movie_id 
       #fetching title
       recommended_movies.append(movies.iloc[i[0]].title)
       #fetching poster from API
       recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similar.pkl','rb'))
st.snow()

##heading
st.markdown("<h1 style='text-align: center; color: White; weight:bold'>Movie Recommender Sytem</h1>", unsafe_allow_html=True)

#image
image = Image.open('cinema.jpg')
st.image(image)

st.subheader('Are you above 12+')
agree = st.checkbox('I agree')
disagree = st.checkbox('I disagree')
if agree:
  st.write('Great! You can proceed')
#if not then stop the execuition
if disagree:
    st.error('Sorry you can not proceed')
    st.stop()
st.date_input(
    "When's your birthday",
    datetime.date(2006, 7, 6))

selected_movie_name = st.selectbox(
  "Type or select a movie from the dropdown",
 movies['title'].values
 )
name=st.text_input("Your name", key = "name")
if not name:
  st.warning('Please input a name.')
  st.stop()
st.write("Welcome to you on our webiste,", st.session_state.name)


if st.button('Show Recommendations'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
score = st.slider('How will you rate our webiste?', 0.0, 100.0, (80.0))
st.write('Score:', score)