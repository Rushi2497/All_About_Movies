# All_About_Movies

This web application is a small project I took to learn various aspects of Natural Language Processing. In an effort to understand NLP and how it can be leveraged to create some very cool utilities, I came up with this idea of implementing the knowledge in the movies domain.

### Motivation

The motivation behind creating 'All About Movies' is that often we spend a lot of time in deciding whether we should watch a movie or not. We google the movie, check the user ratings, and read movie reviews to understand if the general audience like it or not. Not only that, but we also try to understand if the movie suits our taste.
Considering the fact that it takes a lot of time to go through multiple reviews or read about the movie itself, I thought why not create something that can do the job for us. 
<br><br>
I will briefy go through the details of each section in this application explaining what logic or model was used to perform the tasks.

### Sentiment Analysis

Ratings give us an objective benchmark for movies, but as humans we need a subjctive ground to properly judge it. The best way to do that is using sentiment analysis.
This section calculates the sentiment of the top IMDb reviews of a movie scraped from the IMDb website using **requests** and **BeautifulSoup module**. Then it calculates the overall sentiment based on the positive reviews and total number of reviews on the first page of IMDb user reviews. The first page has the most helpful reviews as per IMDb's sorting of reviews by relevence.

Below are preprocessing steps I did to train my ML model which predicts the sentiment of user reviews:
1. Text cleaning - Involves removing non-word characters and punctuation
2. Removing stop words  - Removing the commonly used words in text. I used nltk's stop words for the job.
3. Stemming - Reducing words to base form. For eg - Eating --> Eat. I used nltk's PorterStemmer for this task.

For training I used IMDb 50k reviews data available on Kaggle which is a balanced dataset with 25k reviews for positive and negative sentiments each. Finally, the preprocessed data was fed to a pipeline consisting of a TfidfVectorizer and a Logistic Regression model for training. I used Scikit-Learn's LogisticRegressionCV class with which I achieved 89.99% accuracy on the test set. The pipeline was then pickled to quickly predict new unseen sentiments on the application.

### Plot Summarization

For summarization I took the extractive text summarization approach. This section scrapes the movie plot from the movie's Wikipedia page. Summary is calculated using a word frequency based sentence scoring, the simplest and fastest way to score sentences in a document. Other methods for extractive text summarization are available, like text rank algorithm using similarity matrix of sentences, but I found they are time expensive especially if you are using pre-trained word embeddings like Glove for example. Moreover, upon experimenting with text rank algorithm, I found the summaries to be just as good as the current approach but not any better than it.

### Movie Recommendations

This is one of the interesting hot topics of NLP - recommendation systems. A large amount of companies rely on recommendation systems to run their business. Popular examples being Netflix, or other OTT platforms and even businesses aside from TV/Movie industry that need recommendation systems to sell their products. 
<br><br>
For my project, I am using a **Content-Based Recommendation System**. The meta-data I am using for the movies is taken from TMDB 5000 dataset available on Kaggle. To reduce the time and space usage of the recommendation system, I filtered the data and used only English movies from 1970 to 2016 which reduced the data to just 2953 movies.
<br>
The strategy to recommend movies is as follows:
1. Preprocessing - Removing whitespaces from names (making them unique) and stemming keywords.
2. Create a meta-data soup - I used Director (twice), Cast names (once), Genres (twice) and 5 keywords of the movie to create a text string.
3. If movie searched is from post 2016, fetch data for it from themoviedb.org and create soup with same weightage for meta-data as before.
4. Vectorize the meta-data soup using CountVectorizer and calcualte similarity matrix for movies using cosine similarity.
5. Fetch the most similar movies for the queried movie name and present them if they have a user rating above 6.0

### Future Scope:
1. Addition of word cloud after sentiment analysis to display the most prominent words.
2. Using abstractive text summarization approch for plot summaries.
3. Using other sources for reviews like Rotten Tomatoes instead of only IMDb.
4. Scraping websites can be replaced by using the API for collecting the movie data.

I am open to any suggestions for improving this application and would absolutely love to learn more interesting technologies.
