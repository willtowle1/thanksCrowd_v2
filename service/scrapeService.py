import time
import datetime

from typing import List

class ScrapeService:

    def __init__(self, tickerService, redditService, sentimentService, db) -> None:

        tickerService.generate_tickers_csv()
        self.tickers = tickerService.get_ticker_set()

        self.reddit = redditService
        self.subreddits = redditService.get_subreddits()
        self.sentiment = sentimentService
        self.db = db
        
    def run(self) -> None:
        end = time.time()
        start = end - (60 * 60 * 24)

        self._scrape(start, end)
        return

    def seed(self) -> None:

        end = time.time() - (60 * 60 * 24)
        start = end - ((60 * 60 * 24) * 5)

        self._scrape(start, end)

        return
    
    # Scrape from start (inclusive) to end (exclusive)
    def _scrape(self, start: float, end: float) -> None:
        func_start = time.time()

        print(f"STARTING SCRAPE FOR {self._pretty_time(start)}: {self._pretty_time(end)}...\n")

        n = len(self.subreddits)
        total, num_positive = 0, 0

        for idx, sub in enumerate(self.subreddits):
            print(f"Results for /{sub}... ({idx+1}/{n})")
            
            subreddit_content = self.reddit.get_content_for_subreddit(start, end, sub)
            sub_total, sub_num_positive = self._analyze_content(subreddit_content, end)

            total += sub_total
            num_positive += sub_num_positive

            print(f"Posts: {len(subreddit_content)}")
            print(f"Ticker mentions: {sub_total}")
            print(f"Positive ticker mentions: {sub_num_positive}\n")

        print(f"COMPLETED SCRAPE IN {round(time.time() - func_start, 2)} SECONDS\n")

        print(f"Total results:")
        print(f"Total mention of tickers: {total}")
        print(f"Total positive mentions of ticker: {num_positive}\n")

        return

    def _analyze_content(self, content: List[str], timestamp: float) -> tuple[int, int]: # total, num_positive
        total, num_positive = 0, 0
        for post in content:
            tickers = self._get_tickers(post)
            if len(tickers) > 0:
                isPositive = self.sentiment.analyze(post)
                for ticker in tickers:
                    self.db.increment(ticker.upper(), timestamp, isPositive)
                
                total += len(tickers)
                num_positive += len(tickers) if isPositive else 0

        
        return total, num_positive

    def _get_tickers(self, content: str) -> List:
        tickers = []
        for word in content.split(" "):
            if word in self.tickers:
                tickers.append(word)
        return tickers

    def _pretty_time(self, timestamp: float) -> str:
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')