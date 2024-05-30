# -*- coding: utf-8 -*-

import logging
import requests
import json
import os
import base64
from time import time
from requests.exceptions import ConnectionError
from cherwellapi.apiclient import CherwellAPIClientError, CherwellAPIClientAuthenticationError


class CherwellRouter(object):
    """
    Base class for Cherwell router classes
    """
    def __init__(self, url, headers, user, password, client_id, ssl_verify, token_expire_minutes=18, timeout=5, maxattempts=3):
        self.api_url = url
        self.api_headers = headers
        self.ssl_verify = ssl_verify
        self.api_timeout = timeout
        self.api_maxattempts = maxattempts
        self.api_user = user
        self.api_token_expire_minutes = token_expire_minutes
        self.api_password = password
        self.api_client_id = client_id

    def load_token(self):
        tries = 0
        while tries < self.api_maxattempts:
            try:
                response = requests.request(
                    'POST',
                    '{0}/token'.format(self.api_url),
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data='grant_type=password&client_id={0}&username={1}&password={2}'.format(
                        self.api_client_id, self.api_user, self.api_password),
                    verify=self.ssl_verify,
                    timeout=self.api_timeout
                    )
                break
            except ConnectionError as e:
                logging.warning('Error requesting Cherwell API token %i/%i\n    Error: %s' % (tries, self.api_maxattempts, e))
                # Atempt to display the failure reason from Cherwell
                try:
                    logging.warning("Query failure reason from Cherwell: %s" % response['result']['msg'])
                except Exception:
                    pass
                if tries == self.api_maxattempts:
                    raise CherwellAPIClientAuthenticationError('Unable to connect to Cherwell for new token {0}: {1}'.format(
                        self.api_url, e))
                tries += 1

        if response.ok:
            response_json = response.json()
            try:
                os.environ['zen_ct'] = bytes.decode(base64.b64encode(bytes(response_json['access_token'], 'utf-8')))
                os.environ['zen_rt'] = bytes.decode(base64.b64encode(bytes(response_json['refresh_token'], 'utf-8')))
                os.environ['zen_tt'] = str(time())
            except Exception as exc:
                raise CherwellAPIClientAuthenticationError('Token request failed: {0}\n{1}'.format(response_json, exc))

        else:
            raise CherwellAPIClientAuthenticationError('Token request failed, no response data returned!')

    def refresh_token(self, ):
        # TODO: For now we can keep getting new tokens,
        #  but we can reduce the amount of passing of passwords by using a refresh token
        pass

    def _router_request(self, data=None, api_version=None, action=None, method='GET', response_timeout=None):
        # Disable warnings from urllib3 if ssl_verify is False, otherwise
        # every request will print an InsecureRequestWarning
        if not self.ssl_verify:
            requests.urllib3.disable_warnings()

        if response_timeout is None:
            response_timeout = self.api_timeout

        # Check for unexpired token
        if 'zen_ct' not in os.environ or 'zen_tt' not in os.environ:
            self.load_token()
        if float(os.environ['zen_tt']) < time() - (self.api_token_expire_minutes * 60):
            logging.warning('Token is about to expire, refreshing')
            self.load_token()

        # Decode token
        api_token = bytes.decode(base64.b64decode(os.environ['zen_ct']), 'utf-8')
        self.api_headers['Authorization'] = 'Bearer {0}'.format(api_token)

        # Make Cherwell API call
        tries = 0
        while tries < self.api_maxattempts:
            try:
                response = requests.request(method,
                                            '{0}/{1}/{2}'.format(self.api_url, api_version, action),
                                            headers=self.api_headers,
                                            data=json.dumps(data).encode('utf-8'),
                                            verify=self.ssl_verify,
                                            timeout=response_timeout
                                            )
                break
            except ConnectionError as e:
                logging.warning('Error calling Cherwell API attempt %i/%i\n    Error: %s\n    Request data: %s' % (
                    tries, self.api_maxattempts, e, data))
                # Atempt to display the failure reason from Cherwell
                try:
                    logging.warning("Query failure reason from Cherwell: %s" % response['result']['msg'])
                except Exception:
                    pass
                if tries == self.api_maxattempts:
                    raise CherwellAPIClientError('Unable to connect to Cherwell server {0}: {1}'.format(self.api_url, e))
                tries += 1

        # Return response
        if response.ok:
            response_json = response.json()
            return response_json

        else:
            raise CherwellAPIClientError('Request failed: {0} {1}'.format(response.status_code, response.reason))
