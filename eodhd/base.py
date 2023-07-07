from datetime import date
from datetime import datetime as _datetime
import requests

import time as _time

import pandas as pd
import numpy as np

from data import TickerData
from . import utils
from . import shared

import config as cfg

_BASE_URL_ = 'https://query2.eodhistoricaldata.com'
_ROOT_URL_ = 'https://eodhistoricaldata.com'


class TickerBase:
    def __init__(self, ticker, session=None):
        self.ticker = ticker.upper()
        self.session = session
        self._history = None
        self._history_metadata = None
        self._history_metadata_formatted = False
        self._base_url = _BASE_URL_
        self._root_url = _ROOT_URL_
        self._tz = None

        self._isin = None
        self._news = []
        self._shares = None

        self._earnings_dates = {}

        self._earnings = None
        self._financials = None

        self._data: TickerData = TickerData(self.ticker, session=session)

    def history(self, period="m", interval="1d",
                start=None, end=None, prepost=False,
                keepna=False, rounding=False, timeout=10) -> pd.DataFrame:
        """
        Parameters
        ----------
        period : str
            Use 'd' for daily, 'w' for weekly, 'm' for monthly prices.
            By default, daily prices will be shown.
            Either Use period parameter or use start and end
        interval : str
        start : str
            Download start date string (YYYY-MM-DD), inclusive.
            Default is 1900-01-01
        end : str
            Download end date string (YYYY-MM-DD), exclusive.
            Default is now.
        """

        if (start is None or period is None) or period.lower() == "max":
            if end is None:
                end = int(_time.time())
                end = _datetime.fromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S').split(" ")[0]
            else:
                end = end
            if start is None:
                _UNIX_TIMESTAMP_1900 = "1900-01-01"  # 1900-01-01
                start = _UNIX_TIMESTAMP_1900
            params = {"period1": start, "period2": end}
        else:
            period = period.lower()
            params = {"range": period}

        params["interval"] = interval.lower()
        params["includePrePost"] = prepost

        # Getting data from json
        url = "{}/api/eod/{}?from={}&to={}&period=d&fmt=json&api_token={}".format(
            self._root_url, self.ticker, start, end, cfg.api_key)

        data = None

        try:
            get_fn = self._data.get

            data = get_fn(
                url=url,
                params=params,
                timeout=timeout
            )

            # data = pd.DataFrame(data)
            # data.set_index(['date'], inplace=True)

            data = data.json()  # returns a list
            return data
        except Exception:
            print(f"{self.ticker} not found!!!")
            pass

        err_msg = "No data found for this date range, symbol may be delisted"
        fail = False

        # return data

        # Store the meta data thet gets retrieved
        try:
            self._history_metadata = data
        except Exception:
            self._history_metadata = {}
        self._history_metadata = utils.format_history_data(data)

        fail = False
        if data is None or not type(data) is list:
            fail = True

        if fail:
            # hace algo cuando aparece un error
            shared._DFS[self.ticker] = utils.empty_df()
            shared._ERRORS[self.ticker] = err_msg
            return utils.empty_df()
