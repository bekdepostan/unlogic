#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# nest, blueidea, clean-blog, pelican-cait
THEME = "/mill3d/users/sven/work/sandbox/pelican-clean-blog"

AUTHOR = u'Sven Steinbauer'
SITENAME = u'Unlogic'
SITESUBTITLE = u'I\'ve got a keyboard, a terminal, and a whole load of luck'
SITEURL = ''
DISPLAY_PAGES_ON_MENU = True

HEADER_COVER = 'images/keyboard-feature.jpg'

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

DISQUS_SITENAME = 'unlogic'
GITHUB_URL = 'http://github.com/myprofile'
TWITTER_URL = 'http://twitter.com/myprofile'

COLOR_SCHEME_CSS = 'monokai.css'

PATH = 'content'
STATIC_PATHS = ['images']

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

 #DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
