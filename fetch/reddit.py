import praw
from typing import List
class Reddit:

    MAX_FETCH = 1000

    def __init__(self, id, secret, user_agent):
        self.reddit = praw.Reddit(client_id=id, client_secret=secret, user_agent=user_agent)
    
    def _query_submissions(self, since: float, sub: str) -> List:
        subreddit = self.reddit.subreddit(sub)
        res = []
        try:
            for post in subreddit.new(limit=self.MAX_FETCH):
                if post.created_utc >= since:
                    res.append(post.title + ": " + post.selftext)
                else:
                    break
        except Exception as e:
            print(f"an error occurred while getting submissions for subreddit {sub}: {e}")

        return res

    def _query_comments(self, since: float, sub: str) -> List:
        subreddit = self.reddit.subreddit(sub)
        res = []
        try:
            for comment in subreddit.comments(limit=self.MAX_FETCH):
                if comment.created_utc >= since:
                    res.append(comment.body)
                else:
                    break
        except Exception as e:
            print(f"an error occurred while getting comments for subreddit {sub}: {e}")

        return res

    def get_content_for_subreddit(self, since: float, sub: str) -> List:
        comments = self._query_comments(since, sub)
        submissions = self._query_submissions(since, sub)

        return comments + submissions
        
    

    # def get_subreddit(self, subs):
    #     res = []
    #     for sub in subs:
    #         try:
    #             subreddit = self.reddit.subreddit(sub)
    #             if subreddit.subscribers >= 1000:
    #                 res.append(sub)

    #         except Exception as e:
    #             print(f"an error occurred while getting subreddit {sub}: {e}")

    #     return res
        