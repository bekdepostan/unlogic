#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# nest, blueidea, clean-blog, pelican-cait
THEME = "theme/pelican-chunk"
CSS_FILE = 'style.css'

AUTHOR = u'Sven Steinbauer'
SINGLE_AUTHOR = True

FOOTER_TEXT = '<p>Powered by <a href="http://getpelican.com">Pelican</a>'

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
GITHUB_HANDLE = 'svenito'
TWITTER_HANDLE = 'binaryheadache'
KEYBASE_HANDLE = 'unlogic'

COLOR_SCHEME_CSS = 'monokai.css'

PATH = 'content'
STATIC_PATHS = ['images', 'extra/CNAME', 'extra/favicon.ico', 'extra/keybase.txt',
                'extra/sven_unlogic.asc',
                'extra/.well-known/acme-challenge/KBwpWJ61Qfln1wLxSFKelofWbktKhkJ7I5EqXbPnXm4',
                'extra/.well-known/acme-challenge/VZHdit6jlJu5mme1KCc0jeDmdfLofeDjfvu9wUrmy1k']


EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},
                       'extra/favicon.ico': {'path': 'favicon.ico'},
                       'extra/keybase.txt': {'path': 'keybase.txt'},
                       'extra/sven_unlogic.asc': {'path': 'sven_unlogic.asc'},
                       'extra/.well-known/acme-challenge/KBwpWJ61Qfln1wLxSFKelofWbktKhkJ7I5EqXbPnXm4': {'path': '.well-known/acme-challenge/KBwpWJ61Qfln1wLxSFKelofWbktKhkJ7I5EqXbPnXm4'},
                       'extra/.well-known/acme-challenge/VZHdit6jlJu5mme1KCc0jeDmdfLofeDjfvu9wUrmy1k': {'path': '.well-known/acme-challenge/VZHdit6jlJu5mme1KCc0jeDmdfLofeDjfvu9wUrmy1k'},
                       }

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

        #('Pelican', 'http://getpelican.com/'),
         #('Python.org', 'http://python.org/'),
         #('Jinja2', 'http://jinja.pocoo.org/'),
         #('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Github', 'https://github.com/svenito'),
        ('Twitter', 'https://twitter.com/binaryheadache'),
        ('Rss', SITEURL + '/post/index.xml'),)

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ['plugins']
PLUGINS = ['pelicanfly',
           'pelican_gist' ]
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
