DESCRIPTION
The package, trading-assistant, contains code for front end and back end applications as well as environment and
dependencies files that can be used to import the same tools we used to develop the applications.

Inside WebApp, we have our code for the front end application. This is created from an index.html file as well as
JavaScript functions used to create and render graphs and allow for user interactivity throughout the app.

Inside WebAPI we have our code for the back end application. The API.py file communicates with the WebApp and uses the
logic written inside trading_assistant_app to send responses for the front end to display. Inside trading_assistant_app
is where the data gathering, data preparation, and model training occurs. The file, app.py, is the main driver code,
while utils are used to help gather and construct data correctly.

In order to gather data, we use the utils/reddit.py file to gather mention counts for stocks in the S&P 500 on
the subreddit r/wallstreetbets. This data is stored in reddit_data. The yfinance API in the file ImportSecurities.py
gathers open, high, low, close, and volume financial data for the previous 10 years for the same stocks. Next, using the
financial data, 13 technical indicators are calculated and merged with the mention counts to create 14 different features
on which a machine learning model can be trained on. Additionally, labels are created for each record in the merged
dataframe. From 10 years of data with 252 trading days for about 500 different stocks, this is about 1,260,000 records of
data. Next, this 60% of the data is trained with a RandomForestClassifier. Due to the nature of the data being time-series,
we cannot randomize which data that gets trained and instead have to do a direct split. After training, we find the list
of stocks that are good buys and good sells and display this to the user. Additionally, we also filter the stocks
predicted to those seen or mentioned in r/wallstreetbets. Any user of this application can truly experience the
sensation of being a part of the subreddit.


INSTALLATION
This project is based in python3. You will need this at a minimum to install dependencies and run the project on your local environment.
There are 2 different files provided for installing dependencies:
    1. requirements.txt
    2. environment.yml

With python3, have a dependency manager like Anaconda or pip to install packages for you.
For example, you can get pip via shell command `curl -O https://bootstrap.pypa.io/get-pip.py`,
and run `python3 get-pip.py --user`. Optionally, download Anaconda from https://www.anaconda.com/products/individual

Download dependencies via command `pip install -r requirements.txt`
or by importing conda environment via command `conda env create -f environment.yml`. Also activate the environment
with command `conda activate TradingAssistantApp`.


EXECUTION
The data gathering, preparation, and model training is done in advance to provide the user a seamless experience and
avoid having to take extra time away from the application experience.
Consequently, path variables in WebAPI/trading_assistant_app/app.py are configured to be run with the WebAPI/API.py.

Open up your first terminal shell, and use an environment with the correct python version and dependencies specified above.
This first step will run the backend for the application.
`cd trading-assistant/WebAPI`
`python API.py`

In your second terminal shell, run the following command:
`cd trading-assistant/WebApp`
`python -m http.server`

In your browser, navigate to http://localhost:8000/ to see the WebApp running.
Additionally, this WebApp is running on an EC2 instance http://ec2-18-208-47-240.compute-1.amazonaws.com:6242/

For setting up on EC2, changes needed to be made to the index to read from correct hosts/ports.
Additionally, there needs to be processes set up and running.
On the EC2 instance, Apache HTTP is serving the WebApp and Gunicorn is serving the WebAPI.
