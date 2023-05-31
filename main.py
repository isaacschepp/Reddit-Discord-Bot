import os
import praw
import requests
import time
import logging
from dotenv import load_dotenv
from typing import Set, List
from tenacity import retry, stop_after_attempt, wait_exponential
import json
import signal
import sys

from config import get_configuration

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

class RedditBot:
    """A Reddit bot that posts content to Discord."""

    POSTED_IDS_FILE = 'posted_ids.json'

    def __init__(self, reddit: praw.Reddit, subreddit: praw.models.Subreddit, webhook_url: str, sleep_time: int, minimum_score: int, logger: logging.Logger):
        self.reddit = reddit
        self.subreddit = subreddit
        self.webhook_url = webhook_url
        self.sleep_time = sleep_time
        self.minimum_score = minimum_score
        self.posted_reddit_ids = self.load_posted_ids()
        self.logger = logger

    def load_posted_ids(self) -> Set[str]:
        """Loads IDs of posts that have been posted to Discord."""
        if os.path.isfile(self.POSTED_IDS_FILE):
            with open(self.POSTED_IDS_FILE, 'r') as f:
                return set(json.load(f))
        else:
            self.logger.warning(f"{self.POSTED_IDS_FILE} not found. Creating a new set.")
            return set()

    def save_posted_id(self, id: str) -> None:
        """Saves ID of a post that has been posted to Discord."""
        self.posted_reddit_ids.add(id)
        with open(self.POSTED_IDS_FILE, 'w') as f:
            json.dump(list(self.posted_reddit_ids), f)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=60))
    def post_to_discord(self, content: str) -> None:
        """Posts content to Discord, retrying up to 3 times with exponential backoff."""
        self.logger.info("Attempting to post to Discord")
        response = requests.post(self.webhook_url, data={"content": content})
        if response.status_code != 200:
            if response.status_code == 403:
                raise requests.HTTPError("Forbidden: the request was valid, but the server is refusing action")
            elif response.status_code == 404:
                raise requests.HTTPError("Not Found: The requested resource could not be found on the server")
            # Add more specific error messages based on the status code
            else:
                response.raise_for_status()
        self.logger.info("Post to Discord successful")

    def is_valid_post(self, post: praw.models.Submission) -> bool:
        """Checks if the post is valid."""
        return post.score >= self.minimum_score and post.id not in self.posted_reddit_ids

    def process_post(self, post: praw.models.Submission) -> None:
        """Processes a single Reddit post."""
        content = f"**{post.title}**\n{post.url}"
        try:
            self.post_to_discord(content)
            self.save_posted_id(post.id)
            self.logger.info(f"Posted about {post.id} to Discord")
        except requests.HTTPError as e:
            self.logger.error(f"Error posting to Discord: {e}", exc_info=True)

    def get_new_posts(self) -> List[praw.models.Submission]:
        """Gets new posts from the subreddit."""
        return list(self.subreddit.new(limit=100))

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=60))
    def check_reddit_posts(self) -> None:
        """Checks for new Reddit posts and posts them to Discord, retrying up to 3 times with exponential backoff."""
        self.logger.info("Checking for new Reddit posts")
        try:
            new_posts = self.get_new_posts()
            for post in new_posts:
                if self.is_valid_post(post):
                    self.process_post(post)
        except praw.exceptions.PRAWException as e:
            self.logger.error(f"Error checking Reddit posts: {e}", exc_info=True)
        self.logger.info("Reddit posts check complete")

    def run(self) -> None:
        """Runs the bot."""
        while True:
            try:
                self.check_reddit_posts()
            except (SystemExit, KeyboardInterrupt):
                self.logger.info("Bot is shutting down due to SystemExit or KeyboardInterrupt")
                raise  # Reraise the exception
            except Exception as e:
                self.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            finally:
                time.sleep(self.sleep_time)

def main() -> None:
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

    bot = RedditBot(reddit, subreddit, webhook_url, sleep_time, minimum_score, logger)
    bot.run()


if __name__ == "__main__":
    # handle termination signals
    def signal_handler(sig, frame):
        logger.info("Bot is shutting down due to termination signal")
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    main()
