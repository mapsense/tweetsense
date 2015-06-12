import requests
import json
import pdb

class Api:
  ''' Represents the Mapsense API. '''

  headers = { 'Content-Type': 'application/json' }

  def __init__(self, key, base = 'https://api.mapsense.co'):
    ''' Constructs an API object given some credentials and the base URL of an environment. '''
    self.headers['X-Api-Key'] = key;
    self.base = base;
    self.session = requests.Session();

  def verifyCredentials(self):
    ''' Checks that the credentials given to this API object are valid. '''
    return self.universes().status_code is 200

  def create(self, params):
    return self._post('/create', params)

  def delete(self, params):
    return self._post('/delete', params)

  def universes(self, params = {}):
    return self._get('/universes', params)

  def push(self, params = {}):
    return self._post('/push', params)

  def generate_schema(self, params = {}):
    return self._post('/schema/generate', params)

  def _get(self, endpoint, params = {}):
    return self.session.get(self.base + endpoint, headers = Api.headers, params = params)

  def _post(self, endpoint, data = {}):
    return self.session.post(self.base + endpoint, headers = Api.headers, data = data)

