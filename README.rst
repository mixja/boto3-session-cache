boto3-session-cache
===================

This package automatically configures the underlying AWS Python SDK **botocore** session object used by **boto3** with a file-based cache for storing temporary session credentials.

The implementation leverages the session credential cache used by the AWS CLI, meaning you can use cached credentials from running the AWS CLI in separate external processes.

This is particularly useful if you are required to use multi-factor authentication (MFA) for API-based access to AWS, as you can leverage MFA-authenticated temporary session credentials for up to one hour, rather than having to re-enter your credentials each time you use applications that leverage **boto3**.

Usage
-----

This package provides two functions:

- **boto3_session_cache.session** - returns a low-level **botocore.session** object pre-configured with the credential cache
- **boto3_session_cache.client** - returns a **boto3.client** object pre-configured with the credential cache

In most cases using **boto3_session_cache.client** will be sufficient for your needs.

The following demonstrates how to create a client object:

.. code:: python
  
  import boto3_session_cache

  # This is equivalent to calling boto3.client('ecs')
  client = boto3_session_cache.client('ecs')

  # Do stuff with the client
  clusters = client.list_clusters()

  # You can pass kwargs as normal
  client = boto3_session_cache.client('ecs',region_name='us-west-2')

The following demonstrates how to create a session object:

.. code:: python
  
  import boto3_session_cache

  session = boto3_session_cache.session()

  # You can verify the session is configured with the credential cache
  cache = session.get_component('credential_provider').get_provider('assume-role').cache

  # Create a boto3 client from the session
  client = boto3.Session(botocore_session=session()).client('ecs', aws_region='us-west-2')

Verifying Caching Behaviour
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can quickly verify caching behaviour as follows:

.. code:: bash

  $ cat ~/.aws/config
  [profile test-profile-with-mfa]
  source_profile=my-credentials
  role_arn=arn:aws:iam::123456789012:role/admin
  mfa_serial=arn:aws:iam::123456789012:mfa/mixja
  region=us-west-2
  $ export AWS_PROFILE=test-profile-with-mfa

  # Assuming we have not previously authenticated, we will be prompted for MFA
  $ python
  Python 2.7.13 (default, Dec 18 2016, 07:03:39)
  [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)] on darwin
  Type "help", "copyright", "credits" or "license" for more information.
  >>>
  >>> import boto3_session_cache
  >>> client = boto3_session_cache.client('ecs')
  Enter MFA code: ******
  >>> client.list_clusters()
  {u'clusterArns': [], 'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': '4af14fa0-3835-11e7-b7ef-bd75b8900ae6', 'HTTPHeaders': {'x-amzn-requestid': '4af14fa0-3835-11e7-b7ef-bd75b8900ae6', 'content-length': '18', 'server': 'Server', 'connection': 'keep-alive', 'date': 'Sat, 13 May 2017 23:38:40 GMT', 'content-type': 'application/x-amz-json-1.1'}}}
  >>> exit()

  # Let's try that again - this time we won't be prompted for an MFA token as we've cached temporary session credentials
  $ python
  Python 2.7.13 (default, Dec 18 2016, 07:03:39)
  [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)] on darwin
  Type "help", "copyright", "credits" or "license" for more information.
  >>>
  >>> import boto3_session_cache
  >>> client = boto3_session_cache.client('ecs')
  >>> client.list_clusters()
  {u'clusterArns': [], 'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': '4af14fa0-3835-11e7-b7ef-bd75b8900ae6', 'HTTPHeaders': {'x-amzn-requestid': '4af14fa0-3835-11e7-b7ef-bd75b8900ae6', 'content-length': '18', 'server': 'Server', 'connection': 'keep-alive', 'date': 'Sat, 13 May 2017 23:38:40 GMT', 'content-type': 'application/x-amz-json-1.1'}}}

  # Let's try with the regular boto3 client - drat, we have to authenticate for each new Python session
  >>> import boto3
  >>> client = boto3.client('ecs')
  Enter MFA code: ******

Installation
------------

    pip install boto3-session-cache

Requirements
------------

- boto3_

.. _boto3: https://github.com/boto/boto3

Authors
-------

- `Justin Menga`_

.. _Justin Menga: https://github.com/mixja
