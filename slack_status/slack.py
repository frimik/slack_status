import os
import slack

slack_token = os.environ["SLACK_TOKEN"]
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
client = slack.WebClient(slack_bot_token)
