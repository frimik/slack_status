# slack_status
Slack channel member status dashboard. Shows status text and emojis from members of a chosen channel.

![Screenshot](/slack_status/static/screenshot.png?raw=true "Screenshot")

# Usage

```sh

# example .envrc (if using direnv)
SLACK_TOKEN="xoxp-234335552523-abc123-xyz"
SLACK_BOT_NAME="Archer"
SLACK_BOT_ICON=":archer:"
FLASK_APP=main.py
FLASK_DEBUG=1
export SLACK_TOKEN SLACK_CHANNEL SLACK_BOT_NAME SLACK_BOT_ICON FLASK_APP FLASK_DEBUG

pip3 install -r requirements.txt
flask run
```

Now visit http://localhost:5000/channel/ABCD1234

You can get the channel ID from the web URL of a channel or a message by right-clicking any message in Slack and copying the link to it.

# See also

- [django-emoji](https://github.com/gaqzi/django-emoji) - A simple django app to use emojis on your website ⛺
