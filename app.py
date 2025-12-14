import streamlit as st
from recommender import find_similar_movies, df

st.set_page_config(
    page_icon="233.png",
    page_title= "Movie Similarity Finder",
    layout="centered"
)

st.title("🎥 Movie Similarity Finder")
st.write("Find movies similar to your favourite one.")

movie_title = st.selectbox(
    "Choose a movie", 
    options = sorted(df['title'].unique()),
    index = None,
    placeholder="Movie name..."
)

num_rec = st.slider(
    "Number of Recommendations",
    min_value= 5,
    max_value= 20,
    value=10
)

if st.button("Find Similar Movies"):
    results = find_similar_movies(movie_title,num_rec)
    if results is None:
        st.error("Movie not found.")
    else:
        results = results.copy()
        results["release_year"] = results["release_year"].astype("Int64")
        results['title'] = results['title'] + " (" + results['release_year'].astype(str) + ")"
        results = results.drop(columns='release_year')
        st.subheader("Recommended Movies")
        st.dataframe(results.reset_index(drop=True),use_container_width=True)