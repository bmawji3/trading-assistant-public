import yfinance as yf

def gather_data(symbols_array, spaces_array):
    for space, arr in zip(spaces_array, symbols_array):
        data = yf.download(space, period='ytd', group_by='ticker')
        for symbol in arr:
            data[symbol].to_csv(f'{symbol}.csv')

def main():
    download_new_data = False
    symbols_tech = ['FB', 'AAPL', 'AMZN', 'NFLX', 'GOOGL']
    symbols_meme = ['AMC', 'GME']
    symbols_misc = ['JPM', 'TSLA']
    symbols_etf = ['SPY', 'VOO']
    symbols_array = [symbols_tech, symbols_meme, symbols_misc, symbols_etf]
    flat_symbols = [item for sublist in symbols_array for item in sublist]

    if download_new_data:
        spaces_tech = " ".join(symbols_tech)
        spaces_meme = " ".join(symbols_meme)
        spaces_misc = " ".join(symbols_misc)
        spaces_etf = " ".join(symbols_etf)
        spaces_array = [spaces_tech, spaces_meme, spaces_misc, spaces_etf]
        gather_data(symbols_array, spaces_array)

