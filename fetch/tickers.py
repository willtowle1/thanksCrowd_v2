import requests
import pandas as pd
from io import StringIO

class Tickers:
    def __init__(self, api_key, filename):
        self.url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}'
        self.filename = filename

    def generate_tickers_csv(self):
        try:
            response = requests.get(self.url)
            csv_data = response.text
            df = pd.read_csv(StringIO(csv_data))
            
            df = df[df['assetType'] == 'Stock']
            df = df[df['symbol'].str.len() >= 3]
            df = df[~df['symbol'].str.contains('-')]
            
            df['symbol'].to_csv(self.filename, index=False)
        except Exception as e:
            print(f"failed to generate tickers.csv: {e}")
            return 
        
        print("tickers.csv generated successfully")


    def get_ticker_set(self):
        return set(pd.read_csv(self.filename)['symbol'].tolist())