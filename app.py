import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from load_pipe import pipe
from Utilities.scrape import get_imdb_reviews, get_wiki_plot
from Utilities.sentiments import mean_sentiment
from Utilities.summarizer import extract_summary
from Utilities.recommend import get_recommendations, tmdb_soup
import warnings

warnings.filterwarnings("ignore")
st.set_page_config(page_title='All About Movies',page_icon='🎬')
hide_menu_style = '''
                  <style>
                  #MainMenu {visibility: hidden;}
                  footer  {visibility: hidden;}
                  </style>
                  '''
st.markdown(hide_menu_style,unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []
if 'sentiment_dict' not in st.session_state:
    st.session_state.sentiment_dict = {}
if 'plots' not in st.session_state:
    st.session_state.plots = {}

st.title('All About Movies 📽️')
st.write('Need to know what the general consensus of reviewers about a movie is? Maybe you just need a short summary of a movie with a few other recommendations. Then this is just the website you need! ')
st.write('Find sentiments of movie reviews, read the plot or even get a custom length summary for it. Get recommendations based on your search history as a bonus!')

tab1, tab2, tab3, tab4 = st.tabs(['Sentiment Analysis','Plot Summarization','Movie Recommendations','Links'])

with tab1:    
    st.header('Sentiment Analysis 😃😐☹️')
    st.info('Ever spent a lot of time reading reviews trying to figure out if you should watch a movie or not?\n\nThis section will do just that for you and analyze the sentiment of the top IMDB reviews of the movies you search, giving you an overall sentiment as well as the number of positive and negative reviews.')
    text = st.text_input('Enter any movie name:')
    analyse = st.button('Find Sentiment')
    title = 0
    skip = 1

    if analyse and text:
        try:
            title, year, movie_reviews25 = get_imdb_reviews(text)
            resultant_array = pipe.predict(movie_reviews25)
            sentiment, psum, l = mean_sentiment(resultant_array)

            if title in st.session_state.history:
                skip = 0
            if skip:
                st.session_state.history.append(title)
            if skip:
                st.session_state.sentiment_dict[title] = {'Overall Sentiment':sentiment,'Positive':psum,'Negative':l-psum}
            
            st.write('Movie: '+title+' ('+year+')')
            st.write(' '.join(['Overall Sentiment:', sentiment]))
            col1, col2 = st.columns(2)
            with col1:
                st.write('Number of positive reviews: {}'.format(psum))
            with col2:
                st.write('Number of negative reviews: {}'.format(l-psum))
            if sentiment == 'Mixed':
                st.write('Looks like the reviews are mixed. Check out the plot summary of the movie to decide for yourself.')
            if sentiment == 'Extremely Positive':
                st.write('Looking good! Go ahead and watch that movie right now.')
            if sentiment == 'Extremely Negative':
                st.write('Ohh no. You might want to skip this one...')
        except:
            st.write('Looks like {} is not a movie name. Try typing the name close to the actual movie name.'.format(text))
    
    with st.expander('Sentiments History'):
        st.info('View the sentiment information for all the movies you searched up till now.')
        if st.session_state.sentiment_dict != {}:
            sdf = pd.DataFrame(st.session_state.sentiment_dict)
            sdf = sdf.transpose()[['Positive','Negative']]
            fig, ax = plt.subplots(figsize=(10,8))
            sdf.plot(kind='bar',ax=ax, ylim=(0,30))
            plt.title('Movie Sentiments',fontsize=15)
            plt.xticks(fontsize=12)
            plt.ylabel('Number of Reviews',fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(fontsize=12)
            plt.tight_layout()
            st.pyplot(fig)


with tab2:
    st.header('Plot Summarization 📋')
    st.info('This section summarizes movie plots from Wikipedia using term frequency based sentence scoring. The alpha value is just a multiplying factor using which you can adjust the length of the summary.\n\nGo ahead and try viewing the movie plot or the summary.')
    if analyse and title and skip:
        try:
            wiki_plot = get_wiki_plot(title,year)
            st.session_state.plots[title] = wiki_plot
        except:
            st.session_state.plots[title] = ''
    
    movie = st.selectbox('Select a movie for which you want to display the plot or the summary.',options=st.session_state.history)
    alpha = st.slider('Change the alpha value to adjust the length of the summary. More alpha --> Less length.',value=1.00,step=0.05,min_value=0.80,max_value=1.20)
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        plot = st.button('Display Movie Plot')
    with col2:
        summarize = st.button('Display Plot Summary')

    if plot and movie:
        if st.session_state.plots[movie] == '':
            st.write('Sorry... Cannot scrape the movie plot for this particular movie.')
        else:
            st.write(st.session_state.plots[movie])

    if summarize and movie:
        if st.session_state.plots[movie] == '':
            st.write('Sorry... Cannot scrape the movie plot for this particular movie.')
        else:    
            summary = extract_summary(st.session_state.plots[movie],alpha)
            st.write(summary)


with tab3:
    st.header('Movie Recommendations 🍿')
    st.info('Movie recommendations based on your search history!\n\nThis section utilizes a matrix of cosine similarities calculated between movies to find similar movies. Weightage of movie meta-data is as follows: Genre (2x), Director (2x), Cast and Keywords (1x)\n\nNOTE: While recommendations can be presented for any movie of any year, only English movies between 1970 and 2016 will be recommended for the same.')
    movie = st.selectbox(label='Show Movies Like',options=st.session_state.history)
    recommend = st.button('Show Recommendations')
    if movie and recommend:
        try:
            rec = get_recommendations(movie,tmdb_soup)
            for item in rec:
                st.write(item)
        except:
            st.write('Sorry... Cannot show recommendations for this movie yet :(')


with tab4:
    st.write('[GitHub](https://github.com/Rushi2497)')
    st.write('[LinkedIn](https://www.linkedin.com/in/rushikesh-sawarkar-557607139/)')