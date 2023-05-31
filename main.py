import os
import praw
import logging
from dotenv import load_dotenv
import signal
import sys
import contextlib

from config import get_configuration
from reddit_bot import RedditBot

load_dotenv()
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("reddit_bot")

def main() -> None:
    """
    Entry point of the script.
    """
    config = get_configuration()

    reddit = praw.Reddit(
        client_id=config.reddit_client_id,
        client_secret=config.reddit_client_secret,
        user_agent=config.reddit_user_agent,
    )
    subreddit = reddit.subreddit(config.subreddit)
    webhook_url = config.webhook_url
    sleep_time = config.sleep_time
    minimum_score = config.minimum_score

    bot = RedditBot(reddit, subreddit, webhook_url, sleep_time, minimum_score)
    bot.run()

@contextlib.contextmanager
def signal_handler(logger):
    def _signal_handler(sig, frame):
        if sig == signal.SIGINT:
            logger.info("Bot is shutting down due to user interruption")
            sys.exit(0)
        else:
            logger.info("Bot is shutting down due to termination signal")
            sys.exit(1)

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)
    try:
        yield
    finally:
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
    with signal_handler(logger):
        main()
