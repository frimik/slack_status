from flask import Flask, render_template
from slack_status import app
from slack_status.slack import client

import os


@app.route("/")
def index():
    return "Need a channel_id. Try again at URL: `/channel/ABC123`"


@app.route("/channel/<channel_id>")
def channel(channel_id):
    members = client.conversations_members(channel=channel_id)
    users = []
    for member in members.get("members"):
        user = client.users_info(user=member).get("user")
        if user.get("is_bot"):
            continue

        if not user.get("profile").get("status_emoji") and not user.get("profile").get(
            "status_text"
        ):
            continue

        users.append(user)
        app.logger.info(user)

    return render_template("channel.html", channel=channel_id, users=users)
