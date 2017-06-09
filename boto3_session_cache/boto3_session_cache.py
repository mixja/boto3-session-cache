import botocore.session
import boto3
from .cache import JSONFileCache

def session():
  session = botocore.session.get_session()
  cred_chain = session.get_component('credential_provider')
  provider = cred_chain.get_provider('assume-role')
  provider.cache = JSONFileCache()
  return session

def client(service_name, **kwargs):
  return boto3.Session(botocore_session=session()).client(service_name, **kwargs)

def resource(service_name, **kwargs):
  return boto3.Session(botocore_session=session()).resource(service_name, **kwargs)