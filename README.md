# Reddit-to-Discord Bot

This project is a Reddit-to-Discord bot that fetches new posts from a specified subreddit and posts them to a Discord channel using a webhook. The bot is built using Python and utilizes the `praw` library for interacting with the Reddit API, `requests` for making HTTP requests to the Discord webhook, and `tenacity` for implementing retry logic. The configuration is loaded from environment variables using `python-dotenv`.

## Prerequisites

* Python 3.7 or above
* Reddit API credentials (client ID, client secret, and user agent)
* Discord webhook URL

## Installation

1. Clone the repository: `git clone https://github.com/isaacschepp/Reddit-Discord-Bot.git`
2. Change into the project directory: `cd Reddit-Discord-Bot`
3. Create a new virtual environment:
   - **Windows**:
     ```
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **macOS and Linux**:
     ```
     python3 -m venv .venv
     source .venv/bin/activate
     ```
4. Install the required dependencies: `pip install -r requirements.txt`

## Configuration:
The bot requires the following environment variables to be set:

* `REDDIT_CLIENT_ID`: The client ID of your Reddit application.
* `REDDIT_CLIENT_SECRET`: The client secret of your Reddit application.
* `REDDIT_USER_AGENT`: The user agent for your Reddit application.
* `SUBREDDIT`: The name of the subreddit from which to fetch new posts.
* `WEBHOOK_URL`: The URL of the Discord webhook to post the content.
* `SLEEP_TIME` (optional): The time to sleep between checking for new posts (default: 300 seconds).
* `MINIMUM_SCORE` (optional): The minimum score a post must have to be considered (default: 1000).

Create a `.env` file in the project directory and add the above environment variables with their corresponding values.

## Usage

Run the bot by executing the `main.py` script:

```bash
python main.py
```

The bot will continuously check for new posts on the specified subreddit and post them to the configured Discord channel using the webhook.

To stop the bot, press `Ctrl + C` or send a termination signal.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Additional Files

* `.gitignore`: Specifies which files and directories should be ignored by Git.
* `bot.log`: Log file where the bot logs its activities.
* `config.json`: Configuration file for the bot (not used in this project).
* `posted_ids.json`: JSON file to store the IDs of posts that have been posted to Discord.
* `__pycache__/`: Directory containing Python bytecode files (automatically generated).
* `requirements.txt`: File listing the required Python packages and their versions.

## Credits
This project was created by Isaac Schepp and is based on the [Reddit API](https://www.reddit.com/dev/api/) and [Discord Webhooks](https://discord.com/developers/docs/resources/webhook).
