import requests

from pyctapi import exceptions


class Transport(object):
    """Implement transport between api servers and clinet."""

    def __init__(self, endpoint):
        """Init.
        :param str endpoint: Api endpoint
        """
        self.endpoint = endpoint.rstrip('/')

    def perform_request(self, api, params: dict, method='GET', headers=None, timeout=1):
        url = f'{self.endpoint}{api}'
        headers["User-Agent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0'
        
        try:
            if method == 'POST':
                resp = requests.post(url, json=params, headers=headers)
            else:
                resp = requests.get(url, params=params, headers=headers)
            return resp.json()
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
            raise exceptions.TimeoutError(status_code=504, reason=str(e))
