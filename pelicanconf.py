#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# nest, blueidea, clean-blog, pelican-cait
THEME = "../pelican-chunk"

AUTHOR = u'Sven Steinbauer'
SINGLE_AUTHOR = True

DISPLAY_CATEGORIES_ON_MENU = False

SITENAME = u'Unlogic'
SITESUBTITLE = u'I\'ve got a keyboard, a terminal, and a whole load of luck'
SITEURL = ''
DISPLAY_PAGES_ON_MENU = True

HEADER_COVER = 'images/keyboard-feature.jpg'

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

PYGMENTS_RST_OPTIONS = {'classprefix': 'hll'}

DISQUS_SITENAME = 'unlogic'
#GITHUB_HANDLE = 'svenito'
#TWITTER_HANDLE = 'binaryheadache'

COLOR_SCHEME_CSS = 'monokai.css'

PATH = 'content'
STATIC_PATHS = ['images']

FEED_ATOM = 'post/index.xml'
FEED_RSS = 'feed.xml'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()#('Pelican', 'http://getpelican.com/'),
         #('Python.org', 'http://python.org/'),
         #('Jinja2', 'http://jinja.pocoo.org/'),
         #('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Github', 'https://github.com/svenito'),
        ('Twitter', 'https://twitter.com/binaryheadache'),
        ('Rss', SITEURL + '/post/index.xml'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
