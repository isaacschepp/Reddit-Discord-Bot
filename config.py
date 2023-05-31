import os
from dotenv import load_dotenv
from typing import NamedTuple

class Configuration(NamedTuple):
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str
    subreddit: str
    webhook_url: str
    sleep_time: int
    minimum_score: int

class EnvVar:
    REDDIT_CLIENT_ID = 'REDDIT_CLIENT_ID'
    REDDIT_CLIENT_SECRET = 'REDDIT_CLIENT_SECRET'
    REDDIT_USER_AGENT = 'REDDIT_USER_AGENT'
    SUBREDDIT = 'SUBREDDIT'
    WEBHOOK_URL = 'WEBHOOK_URL'
    SLEEP_TIME = 'SLEEP_TIME'
    MINIMUM_SCORE = 'MINIMUM_SCORE'

def get_configuration() -> Configuration:
    """Loads the configuration from environment variables."""
    load_dotenv()
    
    env_vars = [
        EnvVar.REDDIT_CLIENT_ID,
        EnvVar.REDDIT_CLIENT_SECRET,
        EnvVar.REDDIT_USER_AGENT,
        EnvVar.SUBREDDIT,
        EnvVar.WEBHOOK_URL,
        EnvVar.SLEEP_TIME,
        EnvVar.MINIMUM_SCORE
    ]

    for var in env_vars:
        if var not in os.environ:
            raise ValueError(f"Missing environment variable: {var}")

    config = Configuration(
        reddit_client_id=os.environ[EnvVar.REDDIT_CLIENT_ID],
        reddit_client_secret=os.environ[EnvVar.REDDIT_CLIENT_SECRET],
        reddit_user_agent=os.environ[EnvVar.REDDIT_USER_AGENT],
        subreddit=os.environ[EnvVar.SUBREDDIT],
        webhook_url=os.environ[EnvVar.WEBHOOK_URL],
        sleep_time=int(os.environ.get(EnvVar.SLEEP_TIME, 300)),
        minimum_score=int(os.environ.get(EnvVar.MINIMUM_SCORE, 1000))
    )

    return config
