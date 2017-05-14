import pytest
import os
import json
from datetime import datetime
from boto3_session_cache import JSONFileCache

CACHE_PATH = os.path.expanduser(os.path.join('~', '.aws', 'cli', 'cache'))

def test_cache_lookup(fs):
  cache = JSONFileCache()
  key = 'my-profile--arn_aws_iam__111111111111_role-admin'
  data = {'test': 'test'}
  os.makedirs(CACHE_PATH)
  with open(CACHE_PATH + '/' + key + '.json', 'w') as f:
    json.dump(data, f)
  assert cache[key] == data
  assert key in cache

def test_cache_write(fs):
  cache = JSONFileCache()
  key = 'my-profile--arn_aws_iam__222222222222_role-admin'
  data = {'test': 'test','date':datetime(2016, 3, 8, 11, 37, 24)}
  cache[key] = data
  with open(CACHE_PATH + '/' + key + '.json') as d:
    assert json.load(d) == {'test':'test','date':'2016-03-08T11:37:24'}

def test_cache_miss(fs):
  cache = JSONFileCache()
  key = 'some-random-key'
  with pytest.raises(KeyError) as excinfo:
    cache[key]
  assert key in str(excinfo.value)

def test_cache_non_serializable(fs):
  cache = JSONFileCache()
  key = 'some-bad-key'
  with pytest.raises(ValueError) as excinfo:
    cache[key] = set()
  assert 'Value cannot be cached, must be JSON serializable' in str(excinfo.value)