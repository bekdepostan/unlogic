Extracting bup files in Linux
#############################

:title: Extracting bup files in Linux
:date: 2015-09-03T00
:modified: 2015-09-03 14
:tags:


I recently got hold of some malware that got snapped up by McAfee and stored in a bup file.
Keen to take a look at it, I researched how to 'unbup' files and found this page:

`http://blog.opensecurityresearch.com/2012/07/unbup-mcafee-bup-extractor-for-linux.html <http://blog.opensecurityresearch.com/2012/07/unbup-mcafee-bup-extractor-for-linux.html>`_

A slow bash script? A faster script in Perl? No, that won't do. Rather than search
for a Python implementation I decided to use this as an opportunity to write
something, and thus my `unbup.py` was born. You can get it from my `GitHub <https://github.com/Svenito/unbup>`_

It's about as simple as the bash script in terms of features, but it works, and
it is also fairly fast. I've only tested it with the one file I have, but if
you decide to use it, and it doesn't work, send me the bup file and I'll take a look
at fixing it. Otherwise feel free to fork it and make your own fixes.
