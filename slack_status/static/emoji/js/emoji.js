/*
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
*/

(function (ns) {
  var EMOJIS = {},
    REGEXP = /:([a-z0-9\+\-_]+):/gi,
    DATA_URL = null,
    // Used for keeping track if we should re-load emojis from backend
    EMOJI_VERSION = '1';

  function _loadLocalStorage() {
    if (localStorage.getItem('emoji-version') == EMOJI_VERSION) {
      var data = localStorage.getItem('emojis');

      if (data) {
        return JSON.parse(data);
      }
    }

    return false;
  }

  function _setLocalStorage(data) {
    localStorage.setItem('emoji-version', EMOJI_VERSION);
    localStorage.setItem('emojis', JSON.stringify(data));
  }

  ns.Emoji = {
    dataUrl: function () {
      return DATA_URL;
    },
    setDataUrl: function (url) {
      if (url) DATA_URL = url;

      return this;
    },
    version: function (version) {
      if (version) EMOJI_VERSION = version;

      return EMOJI_VERSION;
    },
    load: function (data) {
      if (data) {
        EMOJIS = data;
        _setLocalStorage(data);
      } else {
        data = _loadLocalStorage();
        if (data) return this.load(data);

        if (DATA_URL) {
          $.get(DATA_URL, null, this.load);
        }
      }

      return this;
    },
    get: function (emoji) {
      if (emoji) return EMOJIS[emoji];

      var keys = [];
      for (var k in EMOJIS) keys.push(k);
      return keys;
    },
    replace: function (replacementString) {
      var that = this;

      return replacementString.replace(REGEXP, function (x, emoji) {
        var url = that.get(emoji);
        if (!url) return x;

        return '<img src="' + url + '" ' +
          'alt="' + emoji.split('_').join(' ') + '" ' +
          'class="emoji">';
      });
    },
    clear: function () {
      localStorage.removeItem('emojis');
      localStorage.removeItem('emoji-version');
      EMOJIS = {};
      DATA_URL = null;
    }
  };

})(window);
