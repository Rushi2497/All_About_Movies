import pandas as pd
from Utilities.scrape import get_tmdb_soup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tmdb_soup = pd.read_csv('all_about_movies/Dormant/tmdb_soup.csv')
tmdb_soup.release_date = tmdb_soup.release_date.astype('str')

def get_recommendations(title,tmdb_soup):
    
    if sum(tmdb_soup.title == title) == 0:
        soup = get_tmdb_soup(title)
        tmdb_soup = pd.concat([tmdb_soup,pd.DataFrame({'index':2954,'title':title,'release_date':'0','soup':soup,'vote_average':0,'vote_count':0},index=[0])],ignore_index=True)
    
    all_soup = tmdb_soup.soup
    CV = CountVectorizer()
    matrix = CV.fit_transform(all_soup)
    similarity_matrix = cosine_similarity(matrix,matrix)

    index = tmdb_soup['index'][tmdb_soup['title'] == title].iloc[0]
    sim_scores = list(enumerate(similarity_matrix[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:51]
    indices = [i[0] for i in sim_scores]
    
    rec = tmdb_soup[['title','release_date','vote_average','vote_count']].iloc[indices]
    rec = rec[['title','release_date']][(rec.vote_average>=6.0) & (rec.vote_count>=500)].head(10)
    rec = rec.apply(lambda x: x['title'] + ' (' + x['release_date'] + ')',axis=1)
    
    return rec