from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from trading_assistant_app import app as ta
from flask_cors import CORS
import pandas as pd
import uuid
import json
import os


def get(ticker_id):
    ## Returns dictionary of stock data
    data = pd.read_csv(f'trading_assistant_app/data/{ticker_id}.csv')  # read CSV
    reddit = pd.read_csv(f'trading_assistant_app/reddit_refined/{ticker_id}_rss_wc.csv')
    reddit = reddit[["Date", "wsb_volume"]]
    data = data.merge(reddit, how='left', on='Date')
    data['wsb_volume'] = data['wsb_volume'].fillna(0)
    data = data.to_dict()  # convert dataframe to dictionary

test = get("TSLA")

r = 1