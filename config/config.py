import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.av_api_key = os.environ.get("AV_API_KEY")
        self.red_client_id = os.environ.get("REDDIT_CLIENT_ID")
        self.red_client_secret = os.environ.get("REDDIT_CLIENT_SECRET")

    def to_dict(self):
        return {
            "av_api_key": self.av_api_key,
            "red_client_id": self.red_client_id,
            "red_client_secret": self.red_client_secret
        }