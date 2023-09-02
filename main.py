import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6a4586e768f1310bf7e372f4f047a508&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+ data['poster_path']
def recommend(movie):
    movie =movie.lower()
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x:x[1])

    recommended_movies=[]
    recommended_movies_poster =[]
    for i in movies_list[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #posters
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'What to watch next',movies['title'].values)

if st.button('Recommend'):
    names,posters= recommend(selected_movie_name)
    names_up = [name.upper() for name in names]
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names_up[0])
        st.image(posters[0])
    with col2:
        st.text(names_up[1])
        st.image(posters[1])
    with col3:
        st.text(names_up[2])
        st.image(posters[2])
    with col4:
        st.text(names_up[3])
        st.image(posters[3])
    with col5:
        st.text(names_up[4])
        st.image(posters[4])
