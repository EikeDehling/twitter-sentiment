import nltk
import csv
import random
import pickle
from tweet import Tweet

# Load tweets
data = csv.reader(open('telecom.csv', 'rb'), delimiter=',', quotechar='|')
tweets = [Tweet(txt, sent) for sent, txt in data]

# Divide into training and evaluation set
random.shuffle(tweets)
tweets_for_training = int(0.75 * len(tweets))
training_tweets = tweets[:tweets_for_training]
test_tweets = tweets[tweets_for_training:]

# Create training set and train classifier
#training_set = [(t.get_feature_vector(), t.sentiment) for t in training_tweets]
training_set = nltk.classify.util.apply_features(lambda t: (t.get_feature_vector(), t.sentiment), training_tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)

# Save trained classifier for later use
with open('classifier.pickle', 'wb') as f:
    pickle.dump(classifier, f)

classifier.show_most_informative_features()

# Evaluate performance of the classifier on the test_tweets
correct = sum(1 for t in test_tweets if t.sentiment == classifier.classify(t.get_feature_vector()))

print classifier.classify(test_tweets[0].get_feature_vector())
print classifier.prob_classify(test_tweets[0].get_feature_vector()).__dict__

print
print "Classified {0} of {1} tweets correctly, that is {2}%".format(correct,
                                                                    len(test_tweets),
                                                                    int(float(correct)/float(len(test_tweets))*100.0))
