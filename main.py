import time

import pandas as pd
from config.config import Config
from fetch.reddit import Reddit
from fetch.tickers import Tickers

def main():

    config = Config()
    config = config.to_dict()

    # tickerService = Tickers(config["av_api_key"], "tickers.csv")
    # tickerService.generate_tickers_csv()
    # ticker_set = tickerService.get_ticker_set()
    # print(ticker_set)

    # ticker_set = set(pd.read_csv("tickers.csv")['symbol'].tolist())
    ticker_set = pd.read_csv("subreddits.csv")['subreddit'].tolist()

    # print(len(ticker_set))
    print(ticker_set)

    # since = time.time() - (60 * 60 * 24)

    # reddit = Reddit(config["red_client_id"], config["red_client_secret"], "thanksCrowd")
    # submissions = reddit.get_content("submissions", since, "WallStreetBets")
    # print(len(submissions))

    # comments = reddit.get_content("comments", since, "WallStreetBets")
    # print(len(comments))

    # subreddits = pd.read_csv("subreddits.csv", header=None)[0].tolist()[1:]


    



if __name__ == "__main__":
    main()
