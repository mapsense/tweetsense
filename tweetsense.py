import requests
import yaml
import twitter
import mapsense
import pdb
import sys
import json
import os
from datetime import datetime
from extract import tweets_to_feature_collection

def twitter_api(verify = True):
  ''' Given a configuration, builds an authenticated Twitter API object. '''
  api = twitter.Api(
    os.environ['TWITTER_CONSUMER_KEY'],
    os.environ['TWITTER_CONSUMER_SECRET'],
    os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

  if verify: api.VerifyCredentials()
  return api

def mapsense_api(verify = True):
  ''' Given a configuration, builds an authenticated Explore API object. '''

  api = mapsense.Api(os.environ['MAPSENSE_API_KEY']);
  if verify: api.verifyCredentials()
  return api

if __name__ == '__main__':
  print 'Initializing Tweetsense application...'

  # Set up the API objects.
  twitter_api = twitter_api()
  mapsense_api = mapsense_api()

  # Request a stream using the given track criteria.
  stream = twitter_api.GetStreamFilter(track = os.environ['TWEETSENSE_TRACK']);

  # Create the universe for the tweets.
  with open('schema.json', 'r') as schema_file:
    schema = json.loads(schema_file.read())
    schema['universe'] = os.environ['TWEETSENSE_UNIVERSE']
    mapsense_api.create(json.dumps(schema))
  
  # Start streaming.
  while True:
    mapsense_api.push(json.dumps({
      'universe': os.environ['TWEETSENSE_UNIVERSE'],
      'ignoreInvalidFieldValues': 'true',
      'source': tweets_to_feature_collection(stream, 10)
    }))

    print 'Pushing to Mapsense @', datetime.now()
    sys.stdout.flush()
      
