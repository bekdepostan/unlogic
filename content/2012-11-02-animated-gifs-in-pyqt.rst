Show animated gifs using PyQT
#############################

:title: Show animated gifs using PyQT
:date: 2012-11-02T00
:tags:


This is just a quick post to show you how to display animated gifs in PyQt. It's a straightforward process and by the end I will give you a class that wraps up the work for you.

The way we're going to approach this is by using a :code:``QLabel`:code:` to render a `:code:`QMovie`:code:`. Assuming we have our gif (`:code:`anim.gif`:code:`) we need to load it into a `:code:`QMovie`:code:` and set it on the `:code:`QLabel``. 

I'll give you the code now:

{% gist 4000025 %}

The code should be fairly easy to follow, so I won't spend much time here going over it. If you want to call this from a :code:``__main__`` function you simply do:

.. code:: python

	if __name__ == "__main__":
	    gif = "/path/to/image.gif"
	    app = QApplication(sys.argv)
	    player = ImagePlayer(gif)
	    player.show()
	    sys.exit(app.exec_())
