from flask import Blueprint, Markup

blueprint = Blueprint("emojis", __name__)

from slack_status.emojis.models import Emoji, SlackEmoji


@blueprint.app_template_filter()
def emoji_replace(value):
    return Markup(Emoji.replace(value))


@blueprint.app_template_filter()
def slack_emoji_replace(value):
    return Markup(SlackEmoji.replace(value))


@blueprint.app_template_filter()
def emoji_replace_unicode(value):
    return Markup(Emoji.replace_unicode(value))


@blueprint.app_template_filter()
def emoji_replace_html_entities(value):
    return Markup(Emoji.replace_html_entities(value))
