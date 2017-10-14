import config
import json
import tweepy

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)

def initial_tweet_download():
    """Download the backlog of tweets."""
    data = {}

    tweets = api.user_timeline(id='realDonaldTrump', count='200', include_rts=False)
    for tweet in tweets:
        if not tweet.retweeted and str(tweet.id) not in data:
            data[str(tweet.id)] = {
                'created_at': str(tweet.created_at),
                'text': tweet.text,
                'favorites': tweet.favorite_count,
                'retweets': tweet.retweet_count
            }

    max_id = tweets[len(tweets) - 1].id

    # gets 3200 of latest tweets
    for i in range(0,16):
        tweets, max_id = get_200_new_tweets(max_id)
        for tweet in tweets:
            if not tweet.retweeted and str(tweet.id) not in data:
                data[str(tweet.id)] = {
                'created_at': str(tweet.created_at),
                'text': tweet.text,
                'favorites': tweet.favorite_count,
                'retweets': tweet.retweet_count
            }

    with open('data.json', 'w') as outfile:  
        json.dump(data, outfile)


def get_200_new_tweets(max_id):
    """Get the next batch of 200 tweets.

    :param max_id: the id of the last tweet
    :return: tweets and the max_id of last tweet as a tuple
    """
    try:
        tweets = api.user_timeline(id='realDonaldTrump', count='200', max_id=max_id, include_rts=False)
    except tweepy.TweepError as e:
        print("Exception: {}".format(e))

    tweets.pop(0)
    max_id = tweets[len(tweets) - 1].id
    return (tweets, max_id)


def get_new_tweets():
    """Get latest tweets. 

    Set this to 200 in case the dumbass somehow tweets 200 times in a day
    Prob figure out better logic for this later.
    """
    try:
        tweets = api.user_timeline(id='realDonaldTrump', count='200', include_rts=False)
    except tweepy.TweepError as e:
        print("Exception: {}".format(e))

    with open('data.json', 'r') as outfile:  
        data = json.load(outfile)

    for tweet in tweets:
        if not tweet.retweeted and str(tweet.id) not in data:
            data[str(tweet.id)] = {
                'created_at': str(tweet.created_at),
                'text': tweet.text,
                'favorites': tweet.favorite_count,
                'retweets': tweet.retweet_count
            }
            print("New tweet! Adding...")

    with open('data.json', 'w') as outfile:  
        json.dump(data, outfile)


def get_most_favorited_tweet():
    """Return the tweet with the most favorites and it's id."""
    max_favorite_count = 0
    max_favorite_count_tweet_id = ''

    with open('data.json', 'r') as outfile:  
        tweets = json.load(outfile)

    for tweet_id in tweets:        
        if tweets[tweet_id]['retweets'] > max_favorite_count:
            max_favorite_count = tweets[tweet_id]['retweets']
            max_favorite_tweet_id = tweet_id

    return (max_favorite_tweet_id, max_favorite_count)


def main():
    # initial_tweet_download()
    get_new_tweets()
    tweet_id, fav = get_most_favorited_tweet()
    print(tweet_id)
    print(fav)

if __name__ == '__main__':
    main()
