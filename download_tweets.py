import config
import json
import tweepy

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)

def initial_tweet_download():
    """Downloads the backlog of tweets
    """
    data = {}
    data['tweets'] = []

    tweets = api.user_timeline(id='realDonaldTrump', count='200', include_rts=False)
    for tweet in tweets:
        if not tweet.retweeted:
            data['tweets'].append({
                'created_at': str(tweet.created_at),
                'text': tweet.text,
                'id': tweet.id,
                'favorites': tweet.favorite_count,
                'retweets': tweet.retweet_count

            })

    max_id = tweets[len(tweets) - 1].id

    # gets 3200 of latest tweets
    for i in range(0,16):
        tweets, max_id = get_200_new_tweets(max_id)
        for tweet in tweets:
            if not tweet.retweeted:
                data['tweets'].append({
                    'created_at': str(tweet.created_at),
                    'text': tweet.text,
                    'id': tweet.id,
                    'favorites': tweet.favorite_count,
                    'retweets': tweet.retweet_count
                })

    print('Dumping {} tweets'.format(len(data['tweets'])))
    with open('data.txt', 'w') as outfile:  
        json.dump(data, outfile)


def get_200_new_tweets(max_id):
    """Gets the next batch of 200 tweets

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


def main():
    save_all_tweets()


if __name__ == '__main__':
    main()
