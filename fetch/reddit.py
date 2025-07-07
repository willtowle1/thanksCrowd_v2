import praw
import pandas as pd
from typing import List

class Reddit:

    MAX_FETCH = 1000

    def __init__(self, id, secret, user_agent) -> None:
        self.reddit = praw.Reddit(client_id=id, client_secret=secret, user_agent=user_agent)
    
    def _query_submissions(self, start: float, end: float, sub: str) -> List:
        subreddit = self.reddit.subreddit(sub)
        res = []
        try:
            for post in subreddit.new(limit=self.MAX_FETCH):
                if start <= post.created_utc < end:
                    res.append(post.title.replace("$", "") + ": " + post.selftext.replace("$", ""))
                elif post.created_utc < start:
                    break
        except Exception as e:
            print(f"an error occurred while getting submissions for subreddit {sub}: {e}")

        return res

    def _query_comments(self, start: float, end: float, sub: str) -> List:
        subreddit = self.reddit.subreddit(sub)
        res = []
        try:
            for comment in subreddit.comments(limit=self.MAX_FETCH):
                if start <= comment.created_utc < end:
                    res.append(comment.body.replace("$", ""))
                elif comment.created_utc < start:
                    break
        except Exception as e:
            print(f"an error occurred while getting comments for subreddit {sub}: {e}")

        return res

    def get_content_for_subreddit(self, start: float, end: float, sub: str) -> List:
        comments = self._query_comments(start, end, sub)
        submissions = self._query_submissions(start, end, sub)
        return comments + submissions
        
    def get_subreddits(self) -> List[str]:
        return pd.read_csv("subreddits.csv")['subreddit'].tolist()
    