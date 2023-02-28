def mean_sentiment(resultant_array):
    
    mean = resultant_array.mean()
    psum = resultant_array.sum()
    
    if mean < 0.2:
        avg_sentiment = 'Extremely Negative'
    elif mean < 0.4:
        avg_sentiment =  'Negative'
    elif mean > 0.8:
        avg_sentiment = 'Extremely Positive'
    elif mean > 0.6:
        avg_sentiment = 'Positive'
    else:
        avg_sentiment = 'Mixed'
    
    return avg_sentiment, psum