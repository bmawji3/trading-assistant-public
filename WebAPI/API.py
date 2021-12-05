from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from trading_assistant_app import app as ta
from flask_cors import CORS
import pandas as pd
import uuid
import json
import os

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

parser = reqparse.RequestParser()
parser.add_argument('date')


class Ticker(Resource):
     def get(self, ticker_id):
        ## Returns dictionary of stock data
        data = pd.read_csv(f'trading_assistant_app/data/{ticker_id}.csv')  # read CSV
        data = data.to_dict()  # convert dataframe to dictionary
        return {'data': data}, 200 


class DailyStocks(Resource):
     def get(self):
        args = parser.parse_args()
        date = args['date']
        buy_prediction = ta.read_predictions(date, minimum_count=0, buy=True)
        sell_prediction = ta.read_predictions(date, minimum_count=0, buy=False)
        return {'data': {
            'buy_prediction': buy_prediction,
            'sell_prediction': sell_prediction
        }}, 200


class Indicators(Resource):
     def get(self, ticker_id):
        args = parser.parse_args()
        date = args['date']
        technical_indicators = ta.get_technical_indicators_for_date(ticker_id, date)
        return {'data': technical_indicators}, 200


class RedditCount(Resource):
    def get(self, ticker_id):
        args = parser.parse_args()
        date = args['date']
        wsb_volume = ta.get_wsb_volume_for_date(ticker_id, date)
        return {'data': wsb_volume}, 200


class SessionLogger(Resource):
    def post(self):
        data = request.get_json()
        
        # Log session data into a JSON file
        fname = 'user_logs.json'
        if not os.path.isfile(fname):
            with open(fname, mode='w') as f:
                json.dump({str(uuid.uuid4()): data}, f, indent=4, sort_keys=True)
        else:
            with open(fname) as logsjson:
                logs = json.load(logsjson)

            with open(fname, mode='w') as f:
                logs[str(uuid.uuid4())] = data
                json.dump(logs, f, indent=4, sort_keys=True)
            
        return "OK", 200


class GetSessionLogs(Resource):
    def get(self):
        my_json = {}
        with open('user_logs.json', 'r') as fp:
            my_json = json.load(fp)
        return my_json


api.add_resource(Ticker, '/ticker/<string:ticker_id>') 
api.add_resource(DailyStocks, '/daily_stocks') 
api.add_resource(Indicators, '/indicators/<string:ticker_id>') 
api.add_resource(RedditCount, '/reddit_count/<string:ticker_id>')
api.add_resource(SessionLogger, '/session_log')
api.add_resource(GetSessionLogs, '/user_session_log')

if __name__ == '__main__':
    app.run()  # run Flask app
