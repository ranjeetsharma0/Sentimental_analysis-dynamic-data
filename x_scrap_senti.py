import pandas as pd
from ntscraper import Nitter
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import time

# Load the sentiment analysis model and tokenizer once
roberta_model_name = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta_model_name)
tokenizer = AutoTokenizer.from_pretrained(roberta_model_name)

labels = ["Negative", "Neutral", "Positive"]

def analyze_tweets(username, number_of_tweets=10):
    # Initialize the Nitter scraper
    scraper = Nitter(log_level=1, skip_instance_check=False)

    # Fetch tweets with retry logic
    for attempt in range(3):  # Try up to 3 times
        tweets = scraper.get_tweets(username, mode="user", number=number_of_tweets)

        if tweets and 'tweets' in tweets and tweets['tweets']:
            break
        else:
            print("Fetching error or no tweets found. Retrying...")
            time.sleep(5)  # Wait before retrying

    if not tweets or 'tweets' not in tweets or not tweets['tweets']:
        print("No tweets found or unable to fetch tweets.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Prepare data for analysis
    results = []

    for tweet in tweets['tweets']:
        tweet_text = tweet['text']

        # Preprocess the tweet text
        tweet_words = []
        for word in tweet_text.split():
            if word.startswith('@'):
                word = '@user'
            elif word.startswith('http'):
                word = 'http'
            tweet_words.append(word)

        tweet_proc = ' '.join(tweet_words)

        # Perform sentiment analysis
        encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
        output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        # Collect sentiment results
        sentiment_result = {labels[i]: scores[i] for i in range(len(scores))}
        sentiment_result['tweet'] = tweet_text
        results.append(sentiment_result)

    # Convert results to DataFrame
    df = pd.DataFrame(results)
    return df

# Example usage
username = "derke"  # Replace with any username you want to analyze
number_of_tweets = 10  # Change this to fetch more tweets

sentiment_df = analyze_tweets(username, number_of_tweets)

# Display the results
print(sentiment_df)
