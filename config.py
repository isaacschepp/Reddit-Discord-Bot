import os
from typing import NamedTuple

class Configuration(NamedTuple):
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str
    subreddit: str
    webhook_url: str
    sleep_time: int
    minimum_score: int

def get_configuration() -> Configuration:
    """Loads the configuration from environment variables."""
    env_vars = [
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET',
        'REDDIT_USER_AGENT',
        'SUBREDDIT',
        'WEBHOOK_URL',
        'SLEEP_TIME',
        'MINIMUM_SCORE'
    ]

    for var in env_vars:
        if var not in os.environ:
            raise ValueError(f"Missing environment variable: {var}")

    config = Configuration(
        reddit_client_id=os.environ['REDDIT_CLIENT_ID'],
        reddit_client_secret=os.environ['REDDIT_CLIENT_SECRET'],
        reddit_user_agent=os.environ['REDDIT_USER_AGENT'],
        subreddit=os.environ['SUBREDDIT'],
        webhook_url=os.environ['WEBHOOK_URL'],
        sleep_time=int(os.environ.get('SLEEP_TIME', 300)),
        minimum_score=int(os.environ.get('MINIMUM_SCORE', 1000))
    )

    return config
