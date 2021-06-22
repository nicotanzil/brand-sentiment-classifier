import nltk
import random
import pickle
from nltk.corpus import twitter_samples
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

Lemmatizer = WordNetLemmatizer()
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet


# nltk.download('twitter_samples')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

class SentimentAnalysis:
    def __init__(self):
        self.classifier = None
        self.english_stops = set(stopwords.words("english"))
        try:
            f = open('classifier.pickle', 'rb')
            self.classifier = pickle.load(f)
            f.close()
        except:
            print('Classifier model pickle file not found!')
            print('Training new data...')
            self.train()

    def train(self):

        snow = SnowballStemmer("english")

        tokenized_positive = twitter_samples.tokenized('positive_tweets.json')
        tokenized_negative = twitter_samples.tokenized('negative_tweets.json')
        tokenized_sample = twitter_samples.tokenized('tweets.20150430-223406.json')

        print(tokenized_sample[0])

        preprocessed_positive_dataset = []
        preprocessed_negative_dataset = []

        for tokens in tokenized_positive:
            preprocessed_positive_dataset.append(self.preprocessing(tokens))

        for tokens in tokenized_negative:
            preprocessed_negative_dataset.append(self.preprocessing(tokens))

        positive_dataset_dict = self.get_tweets_for_model(preprocessed_positive_dataset)
        negative_dataset_dict = self.get_tweets_for_model(preprocessed_negative_dataset)

        positive_dataset = [(tweet_dict, "Positive")
                            for tweet_dict in positive_dataset_dict]

        negative_dataset = [(tweet_dict, "Negative")
                            for tweet_dict in negative_dataset_dict]

        dataset = positive_dataset + negative_dataset

        random.shuffle(dataset)

        train_data = dataset[:7000]
        test_data = dataset[7000:]

        self.classifier = NaiveBayesClassifier.train(train_data)

        # Save the model to pickle file
        f = open('classifier.pickle', 'wb')
        pickle.dump(self.classifier, f)
        f.close()

        print("Accuracy is:", classify.accuracy(self.classifier, test_data))

    def preprocessing(self, word):
        words = []
        for i in sent_tokenize(word):
            known_pos = pos_tag(word_tokenize(i))
            for a, b in known_pos:
                if a.lower() not in self.english_stops:
                    if b.startswith('N'):
                        words.append(Lemmatizer.lemmatize(a, pos="n"))
                    elif b.startswith('V'):
                        words.append(Lemmatizer.lemmatize(a, pos="v"))
                    elif b.startswith('J'):
                        words.append(Lemmatizer.lemmatize(a, pos="a"))
                    elif b.startswith('R'):
                        words.append(Lemmatizer.lemmatize(a, pos="r"))
                    else:
                        words.append(Lemmatizer.lemmatize(a))
        # print("PREPROCESSING WORDS")
        # print(words)
        words = [n for n in words if n not in self.english_stops]
        return words

    def get_tweets_for_model(self, token_dataset):
        for tweet_tokens in token_dataset:
            yield dict([token, True] for token in tweet_tokens)

    def classify_tweets(self, tweet):
        text = self.preprocessing(tweet)
        result = dict([token, True] for token in text)
        return self.classifier.classify(result)
