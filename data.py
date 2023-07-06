import requests
import time
import random

class TickerData:
    """
    
    """
    def __init__(self,ticker:str , session=None):
        self.ticker = ticker
        self._session = session or requests

    def get(self, url, user_agent_headers=None, params=None, proxy=None, timeout=20):

        response = self._session.get(
            url = url,
            params=params,
            proxies=proxy,
            timeout=timeout)
        return response

