Hello Hugo, goodbye Jekyll
##########################

:date: 2016-02-09 11:06:24
:tags: hugo, jekyll, blog
:share: true

It's time to move on from Jekyll and welcome the dawn of `Hugo <http://gohugo.io>`_.
I've now *successfully* migrated the blog over from Jekyll. There were a few hiccups
along the way, but that's to be expected with anything new and shiny.

The reasons I moved generators are:

* Jekyll was taking a long time to generate the blog. Hugo takes around 900ms
* The amount of setup needed to get Jekyll working on a new system was painful. Ruby
    versions, bundles, etc. It just got too much. Hugo is a single binary.
* I fancied something new :)

Still hosted on Github pages of course, so no difference there. There's probably
a few things that need tobe tweaked here and there to get the transition working
(like gist tags and such), but overall all it took was the built in importer
and some runs of :code:`sed`.

