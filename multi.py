import pandas as pd
import multitasking as _multitasking
import re as _re

import shared


def download(tickers, start=None, end=None, threads=True, progress=True, period="max", interval="d",
            timeout=10):
    """
    Download EODHD tickers
    """
    # create ticker list
    tickers = tickers if isinstance(
        tickers, (list, set, tuple)) else tickers.replace(',', ' ').split()
    
    # initialize progress bar (later)
    
    # reset shared.DFS_
    shared._DFS = {}
    shared._ERRORS = {}
    shared._TRACEBACKS = {}
    
    # download using threads
    if threads:
        if threads:
            threads = min([len(tickers), _multitasking.cpu_count() * 2])
        _multitasking.set_max_threads(threads)
        for i, ticker in enumerate(ticker):
            _download_one_threaded(ticker, period=period, interval=interval,
                                   start=start, end=end , timeout=timeout)
            
def _download_one(ticker, start=None, end=end,
                  period="max", interval="d",
                  timeout=10):
    data = None
    try:
        data = Ticker(ticker).history(
                period=period, interval=interval,
                start=start, end=end, timeout=timeout
                )
    except Exception as e: