import json
import random
import time
import geocoder

import requests
from requests.models import Response

from .config import *
from .exceptions import *
from .__init__ import __version__


# Main module interface
class RestSession(object):
    def __init__(
        self,
        logger,
        user_email,
        user_password,
        client_id,   
        single_request_timeout=SINGLE_REQUEST_TIMEOUT,
        retry_4xx_error=RETRY_4XX_ERROR,
        retry_4xx_error_wait_time=RETRY_4XX_ERROR_WAIT_TIME,
        maximum_retries=MAXIMUM_RETRIES
    ):
        super(RestSession, self).__init__()

        # Initialize attributes and properties
        self._version = __version__
        self._user_email = str(user_email)
        self._user_password = str(user_password)
        self._client_id = str(client_id)        
        self._single_request_timeout = single_request_timeout
        self._retry_4xx_error = retry_4xx_error
        self._retry_4xx_error_wait_time = retry_4xx_error_wait_time
        self._maximum_retries = maximum_retries              

        self._access_token = None
        self._main_contract_id = None   

        # Initialize a new `requests` session
        self._req_session = requests.session()
        self._req_session.encoding = 'utf-8'
        
        # Get Location data. Needed for POST requests
        g = geocoder.ip('me')

        # Headers for the session
        self._req_session.headers = {            
            'Content-Type': 'application/json',
            'device-latitude': str(g.latlng[0]),
            'device-longitude': str(g.latlng[1])           
        }

        # Log API calls
        self._logger = logger
        self._parameters = {'version': self._version}
        self._parameters.update(locals())
        self._parameters.pop('self')
        self._parameters.pop('logger')
        self._parameters.pop('__class__')
        self._parameters.pop('user_password')
        
        if self._logger:
            self._logger.info(f'GBM Plus API session initialized with these parameters: {self._parameters}')


    def request(self, metadata, method, url, **kwargs):
        # Metadata on endpoint
        tag = metadata['tags'][0]
        operation = metadata['operation']

        # Update request kwargs with session defaults
        kwargs.setdefault('timeout', self._single_request_timeout)
            
        # Logger        
        if self._logger:
            self._logger.debug(metadata)

        # Set maximum number of retries
        retries = self._maximum_retries

        response = None
        while retries > 0:
            # Make the HTTP request to the API endpoint
            try:
                if response:
                    response.close()
                if self._logger:
                    self._logger.info(f'{method} {url}')
                response = self._req_session.request(method, url, allow_redirects=False, **kwargs)
                reason = response.reason if response.reason else ''
                status = response.status_code
            except requests.exceptions.RequestException as e:
                if self._logger:
                    self._logger.warning(f'{tag}, {operation} - {e}, retrying in 1 second')
                time.sleep(1)
                retries -= 1
                if retries == 0:
                    raise APIError(metadata, response)                    
                else:
                    continue

            # 2XX success
            if response.ok:            
                if self._logger:
                    self._logger.info(f'{tag}, {operation} - {status} {reason}')
                # For non-empty response to GET, ensure valid JSON
                try:
                    if method == 'GET' and response.content.strip():
                        response.json()
                    return response
                except json.decoder.JSONDecodeError as e:
                    if self._logger:
                        self._logger.warning(f'{tag}, {operation} - {e}, retrying in 1 second')
                    time.sleep(1)
                    retries -= 1
                    if retries == 0:
                        raise APIError(metadata, response)
                    else:
                        continue            

            # 5XX errors
            elif status >= 500:
                if self._logger:
                    self._logger.warning(f'{tag}, {operation} - {status} {reason}, retrying in 1 second')
                time.sleep(1)
                retries -= 1
                if retries == 0:
                    raise APIError(metadata, response)

            # 4XX errors
            else:
                try:
                    message = response.json()
                except ValueError:
                    message = response.content[:100]
                
                if self._retry_4xx_error:
                    wait = random.randint(1, self._retry_4xx_error_wait_time)
                    if self._logger:
                        self._logger.warning(f'{tag}, {operation} - {status} {reason}, retrying in {wait} seconds')
                    time.sleep(wait)
                    retries -= 1
                    if retries == 0:
                        raise APIError(metadata, response)

                # All other client-side errors
                else:
                    if self._logger:
                        self._logger.error(f'{tag}, {operation} - {status} {reason}, {message}')
                    raise APIError(metadata, response)
        

    def get(self, metadata, url, params=None):
        metadata['method'] = 'GET'
        metadata['url'] = url
        metadata['params'] = params
        response = self.request(metadata, 'GET', url, params=params)
        ret = None
        if response:
            if response.content.strip():
                ret = response.json()
            response.close()
        return ret


    def post(self, metadata, url, json=None):
        metadata['method'] = 'POST'
        metadata['url'] = url
        metadata['json'] = json
        response = self.request(metadata, 'POST', url, json=json)
        ret = None
        if response:
            if response.content.strip():
                ret = response.json()
            response.close()
        return ret

    def put(self, metadata, url, json=None):
        metadata['method'] = 'PUT'
        metadata['url'] = url
        metadata['json'] = json
        response = self.request(metadata, 'PUT', url, json=json)
        ret = None
        if response:
            if response.content.strip():
                ret = response.json()
            response.close()
        return ret

    def delete(self, metadata, url):
        metadata['method'] = 'DELETE'
        metadata['url'] = url
        response = self.request(metadata, 'DELETE', url)
        if response:
            response.close()
        return None

    def authenticate(self): 
        """
        **Authenticates user**
        https://auth.gbm.com/api/v1/session/user
        """

        metadata = {
            'tags': ['rest_session'],
            'operation': 'authenticate'
        }

        resource = "https://auth.gbm.com/api/v1/session/user"

        payload = {"clientid": self._client_id, "user": self._user_email, "password": self._user_password}

        response = self.post(metadata, resource, payload)

        if response:
            self._access_token = response.get('accessToken')

            # Update session headers with authentication
            self._req_session.headers['Authorization'] = 'Bearer ' + self._access_token                                             
        else:
            raise AuthenticationError()

    def getMainContract(self):
        """
        **Gets main contract ID that is used for many requests**
        https://api.gbm.com/v1/contracts
        """

        metadata = {
            'tags': ['dashboard', 'contract', 'account', 'main_contract'],
            'operation': 'getMainContract'
        }

        resource = "https://api.gbm.com/v1/contracts"

        response = self.get(metadata, resource)[0]

        if response:
            self._main_contract_id = response.get('contract_id')