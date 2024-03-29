"""
Copyright (c) 2013, 2014 Björn Andersson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import re
import struct
from sys import version_info
from flask import url_for
from slack_status import app
from slack_status.slack import client

try:
    from ._unicode_characters import UNICODE_ALIAS
except ImportError as exc:
    UNICODE_ALIAS = {}


from . import settings

__all__ = ("Emoji",)


UNICODE_WIDE = True
try:
    unichr(0x0001F48B)
except ValueError:  # pragma: no cover
    import unicodedata

    UNICODE_WIDE = False
    UNICODE_SURROGATE_MIN = 55296  # U+D800
    UNICODE_SURROGATE_MAX = 57343  # U+DFFF

    def convert_unicode_surrogates(surrogate_pair):
        return unicodedata.normalize("NFKD", surrogate_pair)


except NameError:
    unichr = chr  # Python3 doesn't have unichr

PYTHON3 = False
if version_info[0] == 3:
    PYTHON3 = True
else:
    from _python2 import hex_to_unicode


def get_static_folder(app_or_blueprint):
    """Return the static folder of the given Flask app
    instance, or module/blueprint.
    In newer Flask versions this can be customized, in older
    ones (<=0.6) the folder is fixed.
    """
    if not hasattr(app_or_blueprint, "static_folder"):
        # I believe this is for app objects in very old Flask
        # versions that did not support custom static folders.
        return os.path.join(app_or_blueprint.root_path, "static")

    if not app_or_blueprint.has_static_folder:
        # Use an exception type here that is not hidden by spit_prefix.
        raise TypeError(
            ("The referenced blueprint %s has no static " "folder.") % app_or_blueprint
        )
    return app_or_blueprint.static_folder


class SlackEmoji(object):
    """Test if an emoji exists in the library and returns the URL to it.
    Also can add emojis to a text if they match the pattern :emoticon:.

    Usage:
    >>> emoji = Emoji()
    >>> 'dog' in emoji
    True
    >>> 'doesntexistatall' in emoji
    False
    >>> emoji['dog']  # Uses staticfiles app internally
    '/static/emoji/img/dog.png'
    >>> emoji.replace("I am a :cat:.")
    'I am a <img src="/static/emoji/img/cat.png" alt="cat" class="emoji">.'

    This class is a singleton and if imported as following an instantiated
    version will be imported.
    >>> from emoji import Emoji
    >>> Emoji['dog']
    '/static/emoji/dog.png'

    """

    _static_path = "emoji/img"
    _image_path = os.path.join(get_static_folder(app), "emoji", "img")
    _instance = None
    _pattern = re.compile(r":([a-z0-9\+\-_]+):", re.I)
    _emojis = {}
    _unicode_characters = UNICODE_ALIAS

    # This character acts as a modifier, if it's ever seen then remove
    # it because the modification is done when converting to an image
    # anyway.
    _unicode_modifiers = (u"\ufe0e", u"\ufe0f")

    # HTML entities regexs
    _html_entities_integer_unicode_regex = re.compile(r"&#([0-9]+);")
    _html_entities_hex_unicode_regex = re.compile(r"&#x([0-9a-f]+);", re.I)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SlackEmoji, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.names()

    def __contains__(self, value):
        return value in self._emojis

    def keys(self):
        return self._emojis

    def __getitem__(self, item):
        if item in self._emojis:
            return self._emojis.get(item)

    def _image_string(self, emojiname, alt=None):
        title = " ".join(emojiname.split("_"))

        return settings.EMOJI_IMG_TAG.format(
            self._emojis.get(emojiname), alt or title, title
        )

    @classmethod
    def names(cls):
        """A list of all emoji names."""
        if not cls._emojis:
            _aliased_emojis = cls.fetch_emojis()
            _resolved_emojis = {}
            for emoji_name, emoji_url in _aliased_emojis.items():
                if emoji_url.startswith("alias:"):
                    _, target = emoji_url.split(":")
                    emoji_url = _aliased_emojis.get(target)

                # add resolved or already qualified emoji to _emojis dict
                _resolved_emojis[emoji_name] = emoji_url

            cls._emojis = cls.fetch_emojis()

        return cls._emojis

    @classmethod
    def replace(cls, replacement_string):
        """Add in valid emojis in a string where a valid emoji is between ::"""
        e = cls()

        def _replace_emoji(match):
            val = match.group(1)
            if val in e:
                return e._image_string(match.group(1))
            else:
                return match.group(0)

        return e._pattern.sub(_replace_emoji, replacement_string)

    @classmethod
    def fetch_emojis(cls):
        emoji_response = client.emoji_list()
        return emoji_response["emoji"]


class Emoji(object):
    """Test if an emoji exists in the library and returns the URL to it.
    Also can add emojis to a text if they match the pattern :emoticon:.

    Usage:
    >>> emoji = Emoji()
    >>> 'dog' in emoji
    True
    >>> 'doesntexistatall' in emoji
    False
    >>> emoji['dog']  # Uses staticfiles app internally
    '/static/emoji/img/dog.png'
    >>> emoji.replace("I am a :cat:.")
    'I am a <img src="/static/emoji/img/cat.png" alt="cat" class="emoji">.'

    This class is a singleton and if imported as following an instantiated
    version will be imported.
    >>> from emoji import Emoji
    >>> Emoji['dog']
    '/static/emoji/dog.png'

    """

    _static_path = "emoji/img"
    _image_path = os.path.join(get_static_folder(app), "emoji", "img")
    _instance = None
    _pattern = re.compile(r":([a-z0-9\+\-_]+):", re.I)
    _files = []
    _unicode_characters = UNICODE_ALIAS

    # This character acts as a modifier, if it's ever seen then remove
    # it because the modification is done when converting to an image
    # anyway.
    _unicode_modifiers = (u"\ufe0e", u"\ufe0f")

    # HTML entities regexs
    _html_entities_integer_unicode_regex = re.compile(r"&#([0-9]+);")
    _html_entities_hex_unicode_regex = re.compile(r"&#x([0-9a-f]+);", re.I)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Emoji, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.names()

    def __contains__(self, value):
        return value in self._files

    def keys(self):
        return self._files

    def __getitem__(self, item):
        if item in self._files:
            return self._static_url(item)

    def _static_url(self, name):
        return url_for("static", filename="{0}/{1}.png".format(self._static_path, name))

    def _image_string(self, filename, alt=None):
        title = " ".join(filename.split("_"))

        return settings.EMOJI_IMG_TAG.format(
            self._static_url(filename), alt or title, title
        )

    @classmethod
    def names(cls):
        """A list of all emoji names without file extension."""
        if not cls._files:
            for f in os.listdir(cls._image_path):
                if not f.startswith(".") and os.path.isfile(
                    os.path.join(cls._image_path, f)
                ):
                    cls._files.append(os.path.splitext(f)[0])

        return cls._files

    @classmethod
    def replace(cls, replacement_string):
        """Add in valid emojis in a string where a valid emoji is between ::"""
        e = cls()

        def _replace_emoji(match):
            val = match.group(1)
            if val in e:
                return e._image_string(match.group(1))
            else:
                return match.group(0)

        return e._pattern.sub(_replace_emoji, replacement_string)

    @classmethod
    def replace_unicode(cls, replacement_string):
        """This method will iterate over every character in
        ``replacement_string`` and see if it mathces any of the
        unicode codepoints that we recognize. If it does then it will
        replace that codepoint with an image just like ``replace``.

        NOTE: This will only work with Python versions built with wide
        unicode caracter support. Python 3 should always work but
        Python 2 will have to tested before deploy.

        """
        e = cls()
        output = []
        surrogate_character = None

        if settings.EMOJI_REPLACE_HTML_ENTITIES:
            replacement_string = cls.replace_html_entities(replacement_string)

        for i, character in enumerate(replacement_string):
            if character in cls._unicode_modifiers:
                continue

            # Check whether this is the first character in a Unicode
            # surrogate pair when Python doesn't have wide Unicode
            # support.
            #
            # Is there any reason to do this even if Python got wide
            # support enabled?
            if (
                not UNICODE_WIDE
                and not surrogate_character
                and ord(character) >= UNICODE_SURROGATE_MIN
                and ord(character) <= UNICODE_SURROGATE_MAX
            ):
                surrogate_character = character
                continue

            if surrogate_character:
                character = convert_unicode_surrogates(surrogate_character + character)
                surrogate_character = None

            name = e.name_for(character)
            if name:
                if settings.EMOJI_ALT_AS_UNICODE:
                    character = e._image_string(name, alt=character)
                else:
                    character = e._image_string(name)

            output.append(character)

        return "".join(output)

    @classmethod
    def name_for(cls, character):
        for modifier in cls._unicode_modifiers:
            character = character.replace(modifier, "")

        return cls._unicode_characters.get(character, False)

    @classmethod
    def replace_html_entities(cls, replacement_string):
        """Replaces HTML escaped unicode entities with their unicode
        equivalent. If the setting `EMOJI_REPLACE_HTML_ENTITIES` is
        `True` then this conversation will always be done in
        `replace_unicode` (default: True).

        """

        def _hex_to_unicode(hex_code):
            if PYTHON3:
                hex_code = "{0:0>8}".format(hex_code)
                as_int = struct.unpack(">i", bytes.fromhex(hex_code))[0]
                return "{0:c}".format(as_int)
            else:
                return hex_to_unicode(hex_code)

        def _replace_integer_entity(match):
            hex_val = hex(int(match.group(1)))

            return _hex_to_unicode(hex_val.replace("0x", ""))

        def _replace_hex_entity(match):
            return _hex_to_unicode(match.group(1))

        # replace integer code points, &#65;
        replacement_string = re.sub(
            cls._html_entities_integer_unicode_regex,
            _replace_integer_entity,
            replacement_string,
        )
        # replace hex code points, &#x41;
        replacement_string = re.sub(
            cls._html_entities_hex_unicode_regex,
            _replace_hex_entity,
            replacement_string,
        )

        return replacement_string
