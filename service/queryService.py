import numpy as np
import pandas as pd
from scipy.stats import zscore


class QueryService:

    NUM_DAYS = 7

    def __init__(self, db) -> None:
        self.db = db

    def get_top_tickers(self) -> pd.DataFrame:
        df = self.db.get_top_ticker_df(self.NUM_DAYS)
        if df is None:
            return None

        # Get latest entries with valid count (total_count > 0)
        latest_entries = df.sort_values("date", ascending=False).groupby("ticker").head(1)
        valid_latest = latest_entries[latest_entries["total_count"] > 0]["ticker"]

        # Clean df to include tickers only from valid_latest
        df = df[df["ticker"].isin(valid_latest)]

        # Compute sentiment ratio
        df["sentiment_ratio"] = df["positive_count"] / df["total_count"]
        df.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Compute z-scores (z_sentiment, z_count)
        clean_df = df.sort_values("date", ascending=False).groupby("ticker").head(1).copy()
        if len(clean_df) > 1:
            clean_df["z_sentiment"] = zscore(clean_df["sentiment_ratio"].fillna(0))
            clean_df["z_count"] = zscore(clean_df["total_count"].fillna(0))
        else:
            print("Not enough data to compute z-score... aborting\n")
            return None

        # Compute "score" (score = working equation...)
        # clean_df["score"] = clean_df["z_sentiment"] + (0.5 * clean_df["z_count"])
        clean_df["score"] = clean_df["z_count"] * clean_df["sentiment_ratio"]

        # Sort by score
        result = clean_df.sort_values("score", ascending=False).reset_index(drop=True).head(50)

        return result

