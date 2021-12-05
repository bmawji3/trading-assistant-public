import requests
import datetime
import pandas as pd
import time


class PushShift:

    def __init__(self, query_date):
        self.query_date = query_date
        self.end_date = query_date + datetime.timedelta(days=1)
        self.year_before = self.end_date.year
        self.year_after = query_date.year
        self.month_before = self.end_date.month
        self.month_after = query_date.month
        self.day_before = self.end_date.day
        self.day_after = query_date.day

    def get_pushshift_data_submissions(self):
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
        time.sleep(1)
        if str(request) != '<Response [200]>':
            print(request)
            time.sleep(10)
            request = requests.get(api_url)
            time.sleep(1)
        api_result = request.json()
        return pd.DataFrame(api_result['data'])

    def get_pushshift_data_comments(self):
        """
        Gets data from the pushshift api.
        Read more: https://github.com/pushshift/api
        """
        # Calculate epoch from today and input date
        before = str((datetime.datetime.now() - datetime.datetime(
            self.year_before, self.month_before, self.day_before)).days) + "d"
        after = str((datetime.datetime.now() - datetime.datetime(
            self.year_after, self.month_after, self.day_after)).days) + "d"
        api_url = "https://api.pushshift.io/reddit/search/comment/?"
        api_url += f"before={before}&after={after}&"
        api_url += "size=500&sort_type=score&sort=desc&subreddit=wallstreetbets"
        api_url += "&q:not=[removed]&selftext:not=[deleted]"
        request = requests.get(api_url)
        if str(request) != '<Response [200]>':
            print(request)
            time.sleep(10)
            request = requests.get(api_url)
            time.sleep(1)
        api_result = request.json()
        df = pd.DataFrame(api_result['data'])
        df.rename(columns={"body": "title"}, inplace=True)
        return df

    def filter_dataset(self):
        df = self.get_pushshift_data_submissions()
        if df.shape[0] < 1:
            return None
        if 'link_flair_text' in df.columns \
                and 'title' in df.columns \
                and 'selftext' in df.columns:
            df = df[df.link_flair_text != 'Shitpost']
            df = df[df.link_flair_text != 'Gain']
            df = df[df.link_flair_text != 'Loss']
            df = df[["title", "selftext"]]
        else:
            return None
        return df

    def text_with_ticker(self):
        submittor = self.filter_dataset()
        commentor = self.get_pushshift_data_comments()
        commentor = commentor[["title", "associated_award"]]
        if submittor is None and commentor is None:
            return None
        elif submittor is None:
            redditor = commentor
        elif commentor is None:
            redditor = submittor
        else:
            redditor = pd.concat([submittor, commentor])
        sp500_scope = pd.read_csv("sp_current.csv")
        # Count ticker mentions
        mentions = {}
        for ticker, name in zip(sp500_scope['Symbol'], sp500_scope['Security']):
            ticker_mentions = 0
            for row in redditor.values:
                if type(row[1]) == str:
                    if ' ' + ticker + '.' in row[0] \
                            or ' ' + ticker + '.' in row[1] \
                            or '$' + ticker + ' ' in row[0] \
                            or '$' + ticker + ' ' in row[1] \
                            or '$' + ticker + '.' in row[0] \
                            or '$' + ticker + '.' in row[1] \
                            or ' ' + ticker + ',' in row[0] \
                            or ' ' + ticker + ',' in row[1]\
                            or name in row[0] or name in row[1]:
                        ticker_mentions += 1
                else:
                    if ' ' + ticker + '.' in row[0] \
                            or '$' + ticker + ' ' in row[0] \
                            or '$' + ticker + '.' in row[0] \
                            or ' ' + ticker + ',' in row[0] \
                            or name in row[0]:
                        ticker_mentions += 1

            mentions[ticker] = ticker_mentions
        # Sort for top return efficiency
        mentions = dict(sorted(mentions.items(), key=lambda item: item[1], reverse=True))
        df = pd.DataFrame(columns=['Date', 'Ticker', 'wsb_volume'])
        for k, v in mentions.items():
            if v > 0:
                df2 = pd.DataFrame([[self.query_date, k, v]], columns=['Date', 'Ticker', 'wsb_volume'])
                df = pd.concat([df, df2])
        if df.size == 0:
            return None
        return df


start_date = datetime.datetime(2021, 11, 1)
end_date = datetime.datetime(2021, 12, 3)
delta = datetime.timedelta(days=1)
i = 0
results = pd.DataFrame(columns=['Date', 'Ticker', 'wsb_volume'])
while start_date <= end_date:
    test = PushShift(start_date)
    tickers = test.text_with_ticker()
    if tickers is not None:
        results = pd.concat([results, tickers])
    else:
        time.sleep(0.5)
    i += 1
    print(start_date)
    start_date += delta
    time.sleep(0.5)

unique_tickers = set(results['Ticker'].values.tolist())

for ticker in unique_tickers:
    is_ticker = results['Ticker'] == ticker
    to_file = results[is_ticker]
    to_file.to_csv('reddit_refined2/' + ticker + '_rss_wc.csv', index=False)

r = 1

# Thought we would have more time for adjusting for old
# SP500 changes, sadly this will not be used in this iteration
# def search_sp500(self):
#     """
#     Current SP500 tickers added before query date
#
#     Historical SP500 tickers taken into consideration
#     """
#
#     # Current SP500 Tickers in play
#     current = pd.read_csv("sp_current.csv")
#     current['Date'] = pd.to_datetime(current['Date'])
#     current = current[current.Date <= self.query_date]
#     current = current["Symbol"]
#
#     # Possible SP500 Tickers in play
#     history = pd.read_csv("sp_changes.tsv", sep="\t")
#     history['Date'] = pd.to_datetime(history['Date'], format='%M%d%Y', errors='ignore')
#     history = history[history.Date != '#VALUE!']
#     history['Date'] = pd.to_datetime(history['Date'], errors='ignore')
#     history = history[history.Date <= self.query_date]
#
#     # Aggregate most recent add and removal dates by symbol
#     additions = history.groupby('Symbol').agg(last_add=pd.NamedAgg(column='Date', aggfunc=max))
#     deletions = history.groupby('removed').agg(last_del=pd.NamedAgg(column='Date', aggfunc=max))
#
#     # Join additions with deletions, early date if unavailable
#     change = additions.merge(deletions, how='left', left_index=True, right_index=True)
#     change = change.fillna(datetime.datetime(1800, 1, 1))
#     change = change[change.last_add > change.last_del]
#
#     # Merge old data on new data and clean up
#     sp500_on_date = current.append(pd.Series(change.index), ignore_index=True)
#     sp500_on_date = sp500_on_date.drop_duplicates()
#     sp500_on_date = sp500_on_date.reset_index(drop=True)
#     return pd.DataFrame(sp500_on_date)
