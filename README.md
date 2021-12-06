# trading-assistant
CSE6242 project

**Web API**

Flask API to get stock data, techincal indicators and daily trading opportunities. 
The web app will use this API to display information and save user session data.

e.g. use ```cd WebAPI && python API.py```

**Web App**

The folder is self contained and has all the necessary libraries. To run it locally simply start a server and open the index.html file in a browser.

e.g. use ```cd WebApp && python3 -m http.server```

While you can test locally, CORS issue have been apparent, please test with:
http://ec2-18-208-47-240.compute-1.amazonaws.com:6242/


Buy and sell integer values input into the text box of the days stock.

**Download CSV & Upload to S3**

1. Navigate to app/
2. Update data directory (if needed)
3. Run Script

e.g. ```cd app && python app.py```


