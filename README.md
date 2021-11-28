# trading-assistant
CSE6242 project

**Web App**

The folder is self contained and has all the necessary libraries. To run it locally simply start a server and open the index.html file in a browser.

e.g. use ```python3 -m http.server```

**Download CSV & Upload to S3**

1. Navigate to app/
2. Update data directory (if needed)
3. Run Script

e.g. ```cd app && python app.py```

**Reddit Stock Selector**

In: DateTime

Out: {Ticker: Mentions} in descending order, no tickers with 0 mentions presented.

e.g.
```
test = PushShift(datetime.datetime(2021, 1, 1))
tickers = test.text_with_ticker()
```
