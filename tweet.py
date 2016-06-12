#import nltk
import re

class Tweet(object):
    all_features = set()

    def __init__(self, text, sentiment=None):
        self.sentiment = sentiment
        self.words = self.preprocess(text)
        #self.words = nltk.util.trigrams(self.words)  # Uncomment to classify based on trigrams
        Tweet.all_features |= set(self.words)

    def preprocess(self, text):
        # Lowercase ; remove www.* or https?://* ; remove @mentions ; convert #hashtag to hashtag
        text = text.lower()
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', text)
        text = re.sub('@[^\s]+', '', text)
        text = re.sub(r'#([^\s]+)', r'\1', text)
        return [w.strip('\'"?,.') for w in text.split()]

    def get_feature_vector(self):
        feature_vector = {}
        for w in Tweet.all_features:
            feature_vector[w] = (w in self.words)
        return feature_vector