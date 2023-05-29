import os
import praw
import requests
import time
import logging
from dotenv import load_dotenv
from typing import Set
from tenacity import retry, stop_after_attempt, wait_exponential
from pathlib import Path
import json


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

    def __init__(self, reddit: praw.Reddit, subreddit: praw.models.Subreddit, webhook_url: str, sleep_time: int, minimum_score: int):
        self.reddit = reddit
        self.subreddit = subreddit
        self.webhook_url = webhook_url
        self.sleep_time = sleep_time
        self.minimum_score = minimum_score
        self.posted_reddit_ids = self.load_posted_ids()

    @staticmethod
    def load_posted_ids() -> Set[str]:
        """Loads IDs of posts that have been posted to Discord."""
        file_path = Path(RedditBot.POSTED_IDS_FILE)
        if file_path.is_file():
            with file_path.open('r') as f:
                return set(json.load(f))
        else:
            logger.warning(f"{RedditBot.POSTED_IDS_FILE} not found. Creating a new set.")
            return set()

    def save_posted_id(self, id: str) -> None:
        """Saves ID of a post that has been posted to Discord."""
        self.posted_reddit_ids.add(id)
        with open(RedditBot.POSTED_IDS_FILE, 'w') as f:
            json.dump(list(self.posted_reddit_ids), f)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=60))
    def post_to_discord(self, content: str) -> None:
        """Posts content to Discord, retrying up to 3 times with exponential backoff."""
        logger.info("Attempting to post to Discord")
        response = requests.post(self.webhook_url, data={"content": content})
        response.raise_for_status()
        logger.info("Post to Discord successful")

    def is_valid_post(self, post: praw.models.Submission) -> bool:
        """Checks if the post is valid."""
        return post.score >= self.minimum_score and post.id not in self.posted_reddit_ids

    def process_post(self, post: praw.models.Submission) -> None:
        """Processes a single Reddit post."""
        content = f"{post.title}\n{post.url}"
        try:
            self.post_to_discord(content)
            self.save_posted_id(post.id)
            logger.info(f"Posted about {post.id} to Discord")
        except requests.HTTPError as e:
            logger.error(f"Error posting to Discord: {e.response.content}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=60))
    def check_reddit_posts(self) -> None:
        """Checks for new Reddit posts and posts them to Discord, retrying up to 3 times with exponential backoff."""
        logger.info("Checking for new Reddit posts")
        try:
            for post in self.subreddit.new(limit=100):
                if self.is_valid_post(post):
                    self.process_post(post)
        except Exception as e:
            logger.error(f"Error checking Reddit posts: {e}")
            time.sleep(self.sleep_time)  # wait before retrying
        logger.info("Reddit posts check complete")

    def run(self) -> None:
        """Runs the bot."""
        while True:
            try:
                self.check_reddit_posts()
            except (SystemExit, KeyboardInterrupt):
                logger.info("Bot is shutting down due to SystemExit or KeyboardInterrupt")
                raise  # Re-raise the exception to stop the application
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                time.sleep(self.sleep_time * 2)  # Wait a bit longer before trying again in case of an unexpected error

            time.sleep(self.sleep_time)

def get_configuration() -> dict:
    """Loads the configuration from a file."""
    with open('config.json') as config_file:
        return json.load(config_file)

def main() -> None:
    try:
        config = get_configuration()

        reddit = praw.Reddit(
            client_id=config["REDDIT_CLIENT_ID"],
            client_secret=config["REDDIT_CLIENT_SECRET"],
            user_agent=config["REDDIT_USER_AGENT"],
        )
        subreddit = reddit.subreddit(config["SUBREDDIT"])
        webhook_url = config["WEBHOOK_URL"]
        sleep_time = config.get("SLEEP_TIME", 300)
        minimum_score = config.get("MINIMUM_SCORE", 1000)

        bot = RedditBot(reddit, subreddit, webhook_url, sleep_time, minimum_score)
        bot.run()
    except Exception as e:
        logger.error(f"An error occurred while setting up the bot: {e}")

if __name__ == "__main__":
    main()
