import os
from flask import Flask, render_template
from slack_status import app
from slack_status.slack import client

fake = False
if os.getenv("FAKER"):
    from faker import Faker

    fake = Faker()


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

        # Special fake demo conditions ...
        if fake:
            user["real_name"] = fake.name()
            user["profile"]["image_48"] = "http://lorempixel.com/48/48/?user=%s" % (
                user["name"]
            )

        users.append(user)
        app.logger.info(user)

    return render_template("channel.html", channel=channel_id, users=users)
