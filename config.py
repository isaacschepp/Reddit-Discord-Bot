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

ENV_VAR_TYPES = {
    EnvVar.REDDIT_CLIENT_ID: str,
    EnvVar.REDDIT_CLIENT_SECRET: str,
    EnvVar.REDDIT_USER_AGENT: str,
    EnvVar.SUBREDDIT: str,
    EnvVar.WEBHOOK_URL: str,
    EnvVar.SLEEP_TIME: int,
    EnvVar.MINIMUM_SCORE: int
}

def get_configuration() -> Configuration:
    """Loads the configuration from environment variables."""
    load_dotenv()

    config_values = {}
    for var in ENV_VAR_TYPES:
        value = os.getenv(var)
        if value is None:
            raise ValueError(f"Missing environment variable: {var}")
        key = var.lower()  # Convert to lowercase
        if key in ["sleep_time", "minimum_score"]:
            config_values[key] = int(value)  # Cast to int for these keys
        else:
            config_values[key] = value  # Use as is for other keys

    config = Configuration(**config_values)

    return config
