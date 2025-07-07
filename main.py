import sys
import pandas as pd

from config.config import Config
from dal.dal import Database
from fetch.reddit import Reddit
from fetch.tickers import Tickers
from sentiment.bert import SentimentAnalyzer
from service.scrapeService import ScrapeService
from service.queryService import QueryService

def main():
    print("Starting thanksCrowd...\n")

    args = sys.argv[1:]
    if len(args) > 0:
        if args[0] == "seed":
            seed()
        elif args[0] == "scrape":
            scrape()
        elif args[0] == "query":
            query()
        elif args[0] == "display":
            if len(args) >= 2:
                display_results(args[1])
            else:
                display_results()
        else:
            print("Invalid argument [scrape | query | display]")
            return
    else:
        print("Must provide argument [scrape | query | d]")

def seed():
    config = Config()
    config = config.to_dict()
    print("Config loaded...\n")

    tickerService = Tickers(config["av_api_key"], "tickers.csv")
    redditService = Reddit(config["red_client_id"], config["red_client_secret"], "thanksCrowd")
    sentimentService = SentimentAnalyzer()
    db = Database()
    scrapeService = ScrapeService(tickerService, redditService, sentimentService, db)
    print("Services loaded...\n")

    print("Starting seed...\n")
    scrapeService.seed()
    print("Seed completed...\n")

def scrape():
    config = Config()
    config = config.to_dict()
    print("Config loaded...\n")

    tickerService = Tickers(config["av_api_key"], "tickers.csv")
    redditService = Reddit(config["red_client_id"], config["red_client_secret"], "thanksCrowd")
    sentimentService = SentimentAnalyzer()
    db = Database()
    scrapeService = ScrapeService(tickerService, redditService, sentimentService, db)
    print("Services loaded...\n")

    print("Starting scrape...\n")
    scrapeService.run()
    print("Scrape completed...\n")

def query():
    db = Database()
    queryService = QueryService(db)

    print("Starting query...\n")
    result = queryService.get_top_tickers()
    if result is None:
        print("Result not generated due to insufficient data...\n")
        return
    
    result.to_csv("results.csv", index=False)
    print("Results saved...\n")

def display_results(ticker: str = None):
    df = pd.read_csv("results.csv")
    if ticker is not None:
        print(df[df['ticker'] == ticker])
    else:
        print(df)


if __name__ == "__main__":
    main()
