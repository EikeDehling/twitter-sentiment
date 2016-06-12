import tweepy
import simplejson as json
from twitter_keys import consumer_key, consumer_secret, access_token, access_token_secret
import nltk
import pickle
from tweet import Tweet
from elasticsearch import Elasticsearch

# by default we connect to localhost:9200
es = Elasticsearch()

__author__ = 'dehling'


class MyListener(tweepy.StreamListener):
    n = 0

    def on_data(self, data):
        decoded = json.loads(data)
        text = decoded['text'].encode('ascii', 'ignore')

        print decoded

        #print '|neutral|,|%s|' % text
        t = Tweet(text)
        sentiment = classifier.classify(t.get_feature_vector())
        print '[{sentiment}] @{user} => {tweet}'.format(sentiment=sentiment,
                                                        user=decoded['user']['screen_name'],
                                                        tweet=text)
        #
        #decoded.update(sentiment=sentiment)
        #
        #es.index(index="twitter",
        #         doc_type="tweet",
        #         body=decoded)

        self.n += 1
        return self.n < 250
        #return True

    def on_error(self, status):
        print 'Got error:' + status
        print ''
        return True

    def on_timeout(self):
        print 'Got timeout..'
        return True

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


words = ['de', 'van', 'een', 'het', 'en', 'in', 'is', 'dat', 'op', 'te', 'de', 'zijn', 'voor',
         'met', 'die', 'niet', 'aan', 'er', 'om', 'het', 'ook', 'als', 'dan', 'maar', 'bij',
         'of', 'uit', 'nog', 'worden', 'door', 'naar', 'heeft', 'tot', 'ze', 'wordt', 'over',
         'hij', 'in', 'meer', 'jaar', 'was', 'ik', 'kan', 'je', 'zich', 'al', 'hebben', 'geen',
         'hun', 'we', 'wat', 'een', 'maar', 'werd', 'moet', 'wel', 'kunnen', 'dat', 'nu', 'dit',
         'deze', 'zal', 'ik', 'veel', 'zo', 'en', 'andere', 'nieuwe', 'zou', 'twee', 'moeten',
         'onder', 'eerste', 'haar', 'van', 'wil', 'tegen', 'men', 'mensen', 'gaat', 'tussen',
         'grote', 'waar', 'goed', 'maken', 'dus', 'alleen', 'hij', 'op', 'frank', 'ons', 'u',
         'daar', 'na', 'had', 'gaan', 'alle', 'als', 'er']


#words = ['tele2', 'kpn', 't-mobile', 'tmobile', 'telfort', 'ziggo', 'upc']

#with open('classifier.pickle') as f:
#    classifier = pickle.load(f)

stream = tweepy.Stream(auth, MyListener())
stream.filter(track=words, languages=['nl'])
