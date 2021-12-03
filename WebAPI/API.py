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
         #TODO: Should return list of stocks that represent a trading opportunity

        args = parser.parse_args()
        date = args['date']
        predicted_stocks = ta.read_predictions(date)
        return {'data': predicted_stocks}, 200

class Indicators(Resource):
     def get(self, ticker_id):
         #TODO: Should return techincal indicators and sentiment analysis for a given ticker and date
        
        args = parser.parse_args()
        date = args['date']
        technical_indicators = ta.get_technical_indicators_for_date(ticker_id, date)
        return {'data': technical_indicators}, 200

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


api.add_resource(Ticker, '/ticker/<string:ticker_id>') 
api.add_resource(DailyStocks, '/daily_stocks') 
api.add_resource(Indicators, '/indicators/<string:ticker_id>') 
api.add_resource(SessionLogger, '/session_log') 

if __name__ == '__main__':
    app.run()  # run Flask app
