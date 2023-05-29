# Reddit Discord Bot

This is a Reddit bot that posts content from a specified subreddit to Discord. It uses the PRAW library to interact with Reddit's API and the requests library to post content to Discord webhooks.

## Prerequisites
Before running the bot, make sure you have the following:

* Python 3.6 or above installed.
* PRAW library installed. You can install it using `pip install praw`.
* dotenv library installed. You can install it using `pip install python-dotenv`.

## Installation

1. Clone the repository or download the files to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Create a new file named `.env` in the project directory and add the following environment variables:

```
LOG_LEVEL=INFO
```

4. Create a `config.json` file in the project directory with the following structure:

{
  "REDDIT_CLIENT_ID": "YOUR_REDDIT_CLIENT_ID",
  "REDDIT_CLIENT_SECRET": "YOUR_REDDIT_CLIENT_SECRET",
  "REDDIT_USER_AGENT": "YOUR_REDDIT_USER_AGENT",
  "SUBREDDIT": "TARGET_SUBREDDIT",
  "WEBHOOK_URL": "YOUR_DISCORD_WEBHOOK_URL",
  "SLEEP_TIME": 300,
  "MINIMUM_SCORE": 1000
}

Make sure to replace the placeholder values with your actual Reddit client ID, client secret, user agent, target subreddit, Discord webhook URL, and other desired configurations.

## Usage

To start the bot, run the following command:
```
python main.py
```

The bot will continuously check for new posts on the specified subreddit. If a post meets the minimum score requirement and has not been posted to Discord before, it will be posted to the specified Discord channel using the provided webhook URL.

## Logging

The bot logs its activity to both a file (`bot.log`) and the console. The log level can be configured in the `.env` file using the `LOG_LEVEL` environment variable. By default, the log level is set to `INFO`.

## Handling Errors

The bot implements retry mechanisms for posting to Discord and checking Reddit posts to handle intermittent errors. It will retry up to 3 times with an exponential backoff delay before giving up. If an unexpected error occurs, the bot will wait for a longer period before retrying.

## Customization

You can customize the behavior of the bot by modifying the `config.json` file. The following options are available:

* `SLEEP_TIME` (optional): The time to wait between each check for new Reddit posts, in seconds. Default is 300 seconds (5 minutes).
* `MINIMUM_SCORE` (optional): The minimum score a Reddit post must have to be considered valid. Default is 1000.

Feel free to adjust these values according to your needs.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
