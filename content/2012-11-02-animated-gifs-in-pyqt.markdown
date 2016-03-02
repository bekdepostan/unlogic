---
layout: post
title: Show animated gifs using PyQT
date: 2012-11-02 10:18
comments: true
published: true
tags: [PyQt, programming]
---

This is just a quick post to show you how to display animated gifs in PyQt. It's a straightforward process and by the end I will give you a class that wraps up the work for you.

The way we're going to approach this is by using a ``QLabel`` to render a ``QMovie``. Assuming we have our gif (``anim.gif``) we need to load it into a ``QMovie`` and set it on the ``QLabel``. 

I'll give you the code now:

{% gist 4000025 %}

The code should be fairly easy to follow, so I won't spend much time here going over it. If you want to call this from a ``__main__`` function you simply do:

{% highlight python %}
if __name__ == "__main__":
    gif = "/path/to/image.gif"
    app = QApplication(sys.argv)
    player = ImagePlayer(gif)
    player.show()
    sys.exit(app.exec_())
{% endhighlight %}
