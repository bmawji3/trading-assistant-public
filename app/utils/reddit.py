import requests
import datetime
import pandas as pd

# CALL EXAMPLE
#test = PushShift(datetime.datetime(2021, 1, 1))
#tickers = test.text_with_ticker()
class PushShift:

    def __init__(self, query_date):
        # Local Calls
        self.query_date = query_date
        self.end_date = query_date + datetime.timedelta(days=1)
        self.year_before = self.end_date.year
        self.year_after = query_date.year
        self.month_before = self.end_date.month
        self.month_after = query_date.month
        self.day_before = self.end_date.day
        self.day_after = query_date.day

    def get_pushshift_data(self):
        """
        Gets data from the pushshift api.
        Read more: https://github.com/pushshift/api
        """
        # Calculate epoch from today and input date
        before = str((datetime.datetime.now() - datetime.datetime(
            self.year_before, self.month_before, self.day_before)).days) + "d"
        after = str((datetime.datetime.now() - datetime.datetime(
            self.year_after, self.month_after, self.day_after)).days) + "d"
        api_url = "https://api.pushshift.io/reddit/search/submission/?"
        api_url += f"before={before}&after={after}&"
        api_url += "size=500&sort_type=score&sort=desc&subreddit=wallstreetbets"
        api_url += "&q:not=[removed]&selftext:not=[deleted]"
        request = requests.get(api_url)
        api_result = request.json()
        return pd.DataFrame(api_result['data'])

    def filter_dataset(self):
        df = self.get_pushshift_data()
        df = df[df.link_flair_text != 'Shitpost']
        df = df[df.link_flair_text != 'Gain']
        df = df[df.link_flair_text != 'Loss']
        df = df[["title", "selftext"]]
        return df

    def search_sp500(self):
        """
        Current SP500 tickers added before query date

        Historical SP500 tickers taken into consideration
        """

        # Current SP500 Tickers in play
        current = pd.read_csv("sp_current.csv")
        current['Date'] = pd.to_datetime(current['Date'])
        current = current[current.Date <= self.query_date]
        current = current["Symbol"]

        # Possible SP500 Tickers in play
        history = pd.read_csv("sp_changes.tsv", sep="\t")
        history['Date'] = pd.to_datetime(history['Date'], format='%M%d%Y', errors='ignore')
        history = history[history.Date != '#VALUE!']
        history['Date'] = pd.to_datetime(history['Date'])
        history = history[history.Date <= self.query_date]

        # Aggregate most recent add and removal dates by symbol
        additions = history.groupby('Symbol').agg(last_add=pd.NamedAgg(column='Date', aggfunc=max))
        deletions = history.groupby('removed').agg(last_del=pd.NamedAgg(column='Date', aggfunc=max))

        # Join additions with deletions, early date if unavailable
        change = additions.merge(deletions, how='left', left_index=True, right_index=True)
        change = change.fillna(datetime.datetime(1800, 1, 1))
        change = change[change.last_add > change.last_del]

        # Merge old data on new data and clean up
        sp500_on_date = current.append(pd.Series(change.index), ignore_index=True)
        sp500_on_date = sp500_on_date.drop_duplicates()
        sp500_on_date = sp500_on_date.reset_index(drop=True)
        return pd.DataFrame(sp500_on_date)

    def text_with_ticker(self):
        redditor = self.filter_dataset()
        sp500_scope = self.search_sp500()
        # Count ticker mentions
        mentions = {}
        for ticker in sp500_scope['Symbol']:
            ticker_mentions = 0
            for row in redditor.values:
                if ' ' + ticker + '.' in row[0]\
                        or ' ' + ticker + '.' in row[1]\
                        or '$' + ticker + ' ' in row[0]\
                        or '$' + ticker + ' ' in row[1] \
                        or '$' + ticker + '.' in row[0] \
                        or '$' + ticker + '.' in row[1]\
                        or ' ' + ticker + ',' in row[0]\
                        or ' ' + ticker + ',' in row[1]:
                    ticker_mentions += 1
            mentions[ticker] = ticker_mentions
        # Sort for top return efficiency
        mentions = dict(sorted(mentions.items(), key=lambda item: item[1], reverse=True))
        popular = {}
        for k, v in mentions.items():
            if v > 0:
                popular[k] = v
            else:
                break
        return popular

