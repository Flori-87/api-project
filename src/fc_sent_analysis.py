import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
nltk.download("vader_lexicon")
#nltk.download('stopwords')

sia = SentimentIntensityAnalyzer()

def sentAnalysis(sentence):
    for key in sentence.keys():
        if key == "status":
            return sentence
    for key,value in sentence.items():
        sentiment = sia.polarity_scores(value[0])
        sentence[key].append(sentiment)
    return sentence