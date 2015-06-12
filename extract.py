import sys

def extract(*keys):
  ''' Returns an extractor that simply extracts a key from a tweet. '''
  def extract(tweet):
    value = tweet
    for key in keys:
      if value is None: break
      value = value[key]
      
    return (keys[-1], value)
  return extract

def renaming_extract(name, *keys):
  ''' Returns an extractor that extracts and renames a key from a tweet. '''
  basic = extract(*keys)
  return lambda t: (name, basic(t)[1])

def mapping_extract(mapper, *keys):
  ''' Return an extractor that maps the value at the key from a tweet. '''
  basic = extract(*keys)
  return lambda t: (keys[-1], map(mapper, basic(t)[1]))

def reducing_extract(mapper, reducer, *keys):
  ''' Return an extractor that maps then reduces the value at the key from a tweet. '''
  mapping = mapping_extract(mapper, *keys)
  return lambda t: (keys[-1], reduce(reducer, map(mapper, mapping(t)[1])))

''' 
Defines a list of extractors that operate on a tweet to extract a single property.
The property is returned as a 2-tuple, (name, value).
'''
extractors = [
  renaming_extract('timestamp', 'timestamp_ms'),
  extract('user', 'description'),
  extract('user', 'followers_count'),
  extract('user', 'friends_count'),
  
  mapping_extract(lambda tag: tag['text'], 'entities', 'hashtags'),
  extract('lang'),
  extract('user', 'listed_count'),
  extract('user', 'location'),
  extract('user', 'name'),
  extract('user', 'favourites_count'),
  extract('user', 'screen_name'),
  extract('source'),
  extract('text'),
  extract('user', 'statuses_count'),
  extract('user', 'time_zone'),
  mapping_extract(lambda mention: mention['name'], 'entities', 'user_mentions')
]

def extract_properties_from_tweet(tweet):
  ''' Extracts the properties we want to store with tweets from a single tweet. '''
  return dict(map(lambda e: e(tweet), extractors))

def tweet_to_feature(tweet):
  ''' Transforms a tweet into a GeoJSON feature for Explore to digest. '''
  return {
    'type': 'Feature',
    'geometry': tweet['geo'],
    'properties': extract_properties_from_tweet(tweet)
  }

def tweets_to_feature_collection(generator, count):
  ''' Reads `count' tweets from the generator and creates a GeoJSON feature collection from them. '''
  features = []
  
  while len(features) < count:
    try:
      feature = tweet_to_feature(generator.next())
    except:
      continue
      
    # Ignore tweets without geo information or invalid properties.
    if not feature['geometry']: continue
    if None in feature['properties'].values(): continue
    
    # Twitter messes up its GeoJSON representation of the point.
    feature['geometry']['coordinates'] = feature['geometry']['coordinates'][::-1]

    # Store the feature for pushing.
    features.append(feature)
    
  return {
    'type': 'FeatureCollection',
    'features': features
  }

