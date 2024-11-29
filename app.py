import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movies_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7c359ce0f246c615883d783879866599&language=en-US'.format(movies_id))
    data=response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = cs[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movie_list:
        movies_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster
        recommended_movies_poster.append(fetch_poster(movies_id))
    return recommended_movies,recommended_movies_poster

movie_dict=pickle.load(open('movie.dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)

cs=pickle.load(open('cs.pkl','rb'))

st.title('Movie Recommender System')
selected_movie_names = st.selectbox(
"Select a Movie",
movies['title'].values)

if st.button("Recommend"):
    names,posters=recommend(selected_movie_names)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])