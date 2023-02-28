import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.pipeline import Pipeline

PS = PorterStemmer()

def tokenize(text):
    text = BeautifulSoup(text,'html.parser').get_text(strip = True)
    text = re.sub(r'[^a-zA-Z0-9\s]',' ',text)
    text = re.sub(r'\n','',text)
    
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    tokens = [PS.stem(word) for word in filtered_words]

    return tokens

pipe = Pipeline(steps=[
                        ('tfid',TfidfVectorizer(tokenizer=tokenize)),
                        ('logcv',LogisticRegressionCV(max_iter=1000,n_jobs=-1))
                      ])