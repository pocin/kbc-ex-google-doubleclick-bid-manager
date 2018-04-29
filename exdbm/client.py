"""
Helper stuff

"""
import csv
import datetime
import requests
import logging
from urllib.parse import urljoin

class DBMClient:
    def __init__(self, client_id, client_secret, refresh_token, version='v1'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self._access_token = None
        self.version = version
        self.root_url = 'https://www.googleapis.com/doubleclickbidmanager/{}/'.format(version)

    @property
    def access_token(self):
        if self._access_token is None:
            logging.debug("Authenticating...")
            url = 'https://accounts.google.com/o/oauth2/token'
            data = {
                'refresh_token': self.refresh_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token'
            }
            resp = requests.post(url, data=data)
            try:
                resp.raise_for_status()
            except Exception as e:
                logging.exception(resp.text)
                raise
            else:
                self._access_token = resp.json()['access_token']
        return self._access_token

    def _auth_request(self, method, endpoint, stream=False, **requests_kwargs):
        url = urljoin(self.root_url, endpoint.lstrip('/'))
        headers = {'Authorization': "Bearer {}".format(self.access_token)}
        resp = requests.request(method, url, headers=headers, stream=stream, **requests_kwargs)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            logging.exception(resp.text)
            raise
        else:
            return resp

    def post(self, endpoint, json):
        return self._auth_request("POST", endpoint, json=json)

    def post_stream(self, endpoint, json):
        with self._auth_request("POST", endpoint, json=json, stream=True) as resp:
            yield from resp.iter_content(1024)
