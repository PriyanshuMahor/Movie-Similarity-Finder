import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
#Importing Data
df = pd.read_csv('movies_partial.csv')
df = df.dropna(subset='overview').reset_index(drop=True)
df['text'] = df['title'] + " " + df['overview']
df['release_year'] = pd.to_datetime(df['release_date'],errors='coerce').dt.year
#TF-IDF 
tfidf = TfidfVectorizer(
    stop_words='english',
    max_features=5000
)
tfidf_matrix = tfidf.fit_transform(df['text'])

#Similarity Computation
similarity_matrix = cosine_similarity(tfidf_matrix)
#Weighted Ratings
C = df['vote_average'].mean()
m = df['vote_count'].quantile(0.70)

def weightedRating(row):
    v = row["vote_count"]
    R = row["vote_average"]
    return (v/(v+m))*R + (m/(v+m))*C
df["wr_score"] = df.apply(weightedRating,axis=1)

#Popularity dampeaning
df['pop_score'] = np.log1p(df['popularity'])

scaler = MinMaxScaler()
df[['wr_norm','pop_norm']] = scaler.fit_transform(
    df[['wr_score','pop_score']]
)
#Recommender
def find_similar_movies(title,n=10):
    if title not in df['title'].values:
        return f"{title} not found, Recheck the input."
    
    idx = df[df['title'] == title].index[0]

    sim_scores = list(enumerate(similarity_matrix[idx]))
    
    final_scores = []
    for i,sim in sim_scores:
        score = (
            0.6 * sim +
            0.3 * df.loc[i,'wr_norm'] +
            0.1 * df.loc[i,'pop_norm']
        )
        final_scores.append((i,score))
    
    final_scores = sorted(final_scores,key= lambda x: x[1],reverse=True)
    final_scores = final_scores[1:n+1] #skip itself
    
    movie_indices = [i[0] for i in final_scores]
    return df.loc[movie_indices, ['title','release_year','vote_average','vote_count']]