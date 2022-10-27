import string
import tweepy as tw
import pandas as pd


class Twdata():

  CONSUMER_KEY = 'r01r2bfCABaDUQrJBE5DPMad5'
  CONSUMER_SECRET = 'SWdv2zhaMFuGKASpI9lHZmxPoQtuaOIVixMtpBW8GqCOzTc2oS'
  ACCESS_KEY = '1578317341691109378-GDFPDgNtjPu2VTieOvLHe9ChHwWqZA'
  ACCESS_SECRET = 'Pq6uNnKwwGjSDP38tzlaLclRVTrMkycbpp9ImvOuCuMjH'
  auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  api = tw.API(auth, wait_on_rate_limit=True)
  auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

  def __init__(self):
    self.string = string

  def query_search(self, string):
    search_query = f'{string}'
    tweets = tw.Cursor(self.api.search_tweets, q=search_query, lang="es").items(100000)
    tweets_copy = []
    for tweet in tweets:
      tweets_copy.append(tweet)
    print("Total Tweets fetched:", len(tweets_copy))
    
    dfout = pd.DataFrame()

    for tweet in tweets_copy:
      text = self.api.get_status(id=tweet.id, tweet_mode='extended').full_text
      dfout = dfout.append(
          pd.DataFrame(
              {'key_string': string,
              'user_name': tweet.user.name, 
              'screen_name': tweet.user.screen_name,
              'user_location': tweet.user.location,
              'user_description': tweet.user.description,\
              'user_verified': tweet.user.verified,
              'date': tweet.created_at,
              'id': tweet.id,
              'text': text,
              'source': [tweet.source]}
          )
      )

    dfout = dfout.reset_index(drop=True)

    return dfout

  def search_list(self, string_list):

    df = pd.DataFrame()

    for i in string_list:
      df = df.append(self.query_search(i))
    
    return df