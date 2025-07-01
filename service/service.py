import time

import pandas as pd
from typing import List

class Service:

    def __init__(self, tickerService, redditService, sentimentService): # todo: add DB
        self.subreddits = pd.read_csv("subreddits.csv")['subreddit'].tolist()
        
        tickerService.generate_tickers_csv()
        self.tickers = tickerService.get_ticker_set()

        self.reddit = redditService
        self.sentiment = sentimentService
        
    def run(self):
        time_now = time.time()
        since = time_now - (60 * 60 * 24)

        print(f"STARTING FETCH FOR {since}: {time_now}")

        n = len(self.subreddits)
        for idx, sub in enumerate(self.subreddits):
            print(f"FETCHING AND ANALYZING CONTENT FOR {sub}... {idx+1}/{n}", end="\r")
            subreddit_content = self.reddit.get_content_for_subreddit(since, sub)

        
        return

    def analyze_content(self, content: List[str], timestamp: float):
        pass
        # for post in content:
        #     ticker, has_match = self.has_match(post)
        #     if has_match:
        #         analyze sentiment
        #         create entry in db for ticker+timestamp or increment existing entry
        
        
        # return

    def has_match(self, content: str) -> tuple[bool, str]:

        for word in content.split(" "):
            if word in self.tickers:
                return True, word

        return False, ""


# start()
# for each subreddit, fetch data from reddit
# if ticker/common name in data
# analyze, and increment counter for that ticker+date
# if entry exists, update.... create if not
# ----> SQL or NoSQL?