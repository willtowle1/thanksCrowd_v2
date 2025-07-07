import requests
import pandas as pd
from io import StringIO

class Tickers:

    TICKER_EXCLUSIONS = ["YOU", "FOR", "ALL", "GOOD", "ANY", "ARE", 
                         "CAN", "NOW", "GET", "WELL", "NICE", "HAS", 
                         "SEE", "PAY", "LOW", "HOPE", "WOW"]
    def __init__(self, api_key, filename) -> None:
        self.url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}'
        self.filename = filename

    def generate_tickers_csv(self) -> None:
        try:
            response = requests.get(self.url)
            csv_data = response.text
            df = pd.read_csv(StringIO(csv_data))

            # Clean up            
            df = df[df['assetType'] == 'Stock']
            df = df[df['symbol'].str.len() >= 3]
            df = df[~df['symbol'].str.contains('-')]
            df = df[~df['symbol'].isin(self.TICKER_EXCLUSIONS)]
                        
            # Add TICKER -> Ticker copy
            df_upper = df.copy()
            df_upper['symbol'] = df_upper['symbol'].apply(lambda x: x[0].upper() + x[1:].lower())
            df = pd.concat([df, df_upper])

            df['symbol'].to_csv(self.filename, index=False)
        except Exception as e:
            print(f"failed to generate tickers.csv: {e}")
            return 
        
        print("tickers.csv generated successfully...\n")


    def get_ticker_set(self) -> set:
        return set(pd.read_csv(self.filename)['symbol'].tolist())