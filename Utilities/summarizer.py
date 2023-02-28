from collections import Counter
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def extract_summary(text,alpha):
    
    filtered_text = re.sub(r'[^a-zA-Z0-9\s]',' ',text).lower()
    words = filtered_text.split()
    filtered_words = [word for word in words if word not in stop_words]
    freq_table = Counter(filtered_words)
    
    sentences = sent_tokenize(text)
    sent_scores = {}
    for sentence in sentences:
        for word,freq in freq_table.items():
            if word in sentence.lower():
                if sentence in sent_scores:
                    sent_scores[sentence] += freq
                else:
                    sent_scores[sentence] = freq
    
    total_score = sum(sent_scores.values())
    total_sent = len(sent_scores)
    avg_score = total_score/total_sent
    
    summary = ''
    for sentence,score in sent_scores.items():
        if score > alpha*avg_score:
            summary += ' ' + sentence
    
    return summary.lstrip()