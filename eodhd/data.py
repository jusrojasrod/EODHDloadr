from functools import lru_cache

import requests
import time
import random


cache_maxsize = 64


class TickerData:
    """

    """
    def __init__(self, ticker: str, session=None):
        self.ticker = ticker
        self._session = session or requests

    def get(self, url, user_agent_headers=None, params=None, proxy=None,
            timeout=20):

        response = self._session.get(
            url=url,
            params=params,
            proxies=proxy,
            timeout=timeout)
        return response

    @lru_cache(maxsize=cache_maxsize)
    def cache_get(self, url, user_agent_headers=None, params=None, proxy=None,
                  timeout=20):
        return self.get(url, user_agent_headers, params, proxy, timeout)
