from django.shortcuts import render
from django.http import *
from SentimentAnalyzer.forms import *
from textblob import TextBlob
import sys, tweepy

# Create your views here.
class  TwitterTweets():

	def __init__(self):
		API_key = "HulhTW9uuqdlykNbMHp86vJrH"
		API_secret = 'jBOTSUhz7VkozRtQFJGin1AzHvmBQ7T6e7uIV4YmSMvktJqKLj'
		Access_token = '900287585792266240-AZfFrOVorLmXVCdjiEFbvBkqDQmK5tA'
		Access_token_secret = 'yCzgaokBZR7RHWT1UqeGSGAqwXJ4kaxPt7zb58XvxL1yq'
		self.auth = tweepy.OAuthHandler(API_key, API_secret)
		self.auth.set_access_token(Access_token, Access_token_secret)
		self.api = API(self.auth)

	def remove_unnecessary_symbols(self, tweet):
		  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_sentiment(self, tweet):
		analysis = TextBlob(self.remove_unnecessary_symbols(tweet))
		if analysis.sentiment.polarity > 0:
			return 'Positive'
		elif analysis.sentiment.polarity == 0:
			return 'Neutral'
		else:
			return 'Negative'


	def get_tweets(self, query, count):
		tweets = []
		obtain_tweets = self.api.search(query, count)
		for tweet in obtain_tweets:
			parsed_tweet = {}
			parsed_tweet['text'] = tweet.text
			parsed_tweet['sentiment'] = self.get_sentiment(tweet.text)
			if tweet.retweet_count > 0:
				if parsed_tweet not in tweets:
					tweets.append(parsed_tweet)
			else:
				tweets.append(parsed_tweet)
		return tweets


def show(request):
	form_temp = SearchForm()
	return render(request, 'index.html', {'form':form_temp})

def graph_sentiment(request):
	pos = 0
	neg = 0
	neu = 0
	if request.method == 'POST':
		api = TwitterTweets
		q = request.POST['tweet_search']
		tweets = api.get_tweets(q, count = 100)

		for tweet in tweets:
			if tweet['sentiment'] == 'Positive':
				pos = pos + 1

			if tweet['sentiment'] == 'Negative':
				neg = neg + 1

			if tweet['sentiment'] == 'Neutral':
				neu = neu + 1

		labels = ['Positive', 'Negative', 'Neutral']
		data = [pos, neg, neu]
		return render(request, 'pie-chart.html', {
		'labels': labels,
		'data' : data,
		})


