# trading-assistant
CSE6242 project

**Web App**

The folder is self contained and has all the necessary libraries. To run it locally simply start a server and open the index.html file in a browser.

e.g. use ```python3 -m http.server```


**Web App**

Flask API to get stock data, techincal indicators and daily trading opportunities. 
The web app will use this API to display information and save user session data.

e.g. use ```cd WebAPI && python API.py```


**Download CSV & Upload to S3**

1. Navigate to app/
2. Update data directory (if needed)
3. Run Script

e.g. ```cd app && python app.py```

**Reddit Stock Selector**

Input a DateTime to output csv files containing date (day), ticker, and mention count in r\wallstreetbets top 500 scored submissions.

e.g.
```
test = PushShift(datetime.datetime(2021, 1, 1))
tickers = test.text_with_ticker()
```
Used to populate the reddit_data folder for the date range of r\wallstreetbets existence, 1-2 hours runtime on base model 2020 macbook air.

