Shapely Window in PyQT
######################

:title: Shapely Window in PyQT
:date: 2011-05-27T15
:tags:


Recently I needed to make a PyQt app where the :code:`window` is the shape of an image and doesn’t 
have a border. I say needed, that’s not strictly true, more like wanted to because it’d be more 
interesting.

It wasn’t as straight forward as I had hoped but I managed to get it working in the end and 
here I am about to share it with the world. Here’s what we will need:

1. python, Qt, and PyQt installed	
2. The image you want to use as the background with transparency. PNG will do nicely	
3. A texteditor	
4. A cup of coffee

Set the coffee aside so you don’t knock it over, but keep it within reach. First we need to 
open up Designer.

Once open create a new Dialog or MainWindow. Open the resource browser and add your background 
image to the list of resources. Now right click on the :code:`window` and select 
:code:`Change styleSheet` (I am using Designer4 in case it looks different for you).
Enter the following in the popup, adjusting for names and path as appropriate.

.. code:: python

	#Dialog{
	    background-color: rgb(0, 0, 0);
	    background-image: url(:/img/windowshape.png);
	}

Adjusting the :code:``#Dialog`` to the :code:`window` name and the url path to your image.

You should now see the image in the :code:`window` with a black surround. At this point it’s also 
good to set the :code:`window` size to something suitable for your image.

As per usual you will need to compile your .ui and resource files with pyuic and pyrcc, but details on that are outside the scope of this post.
So in order to remove the border we call this in our :code:`__init__` function

.. code:: python

	self.win = QtGui.QMainWindow()
	self.win.setWindowFlags(self.win.windowFlags() |
	    QtCore.Qt.FramelessWindowHint |
	    QtCore.Qt.WindowSystemMenuHint)
    
It’s important to derive your class from :code:`QtGui.QMainWindow` otherwise this won’t work.

Don’t be surprised if under certain :code:`window` managers you still see a border, not all `window` 
managers will render windows without borders from :code:`Qt`. The settings are just a request rather than a demand. In Fluxbox for instance the border still shows. Gnome and KDE work fine.

Right, time for a sip of coffee. You earned it. But wait, what about the black colour? We want the :code:`window` in the shape of the image. Ah yes, we do that by adding this function

.. code:: python

	def resizeEvent(self, event):
	    pixmap = QtGui.QPixmap(":/img/windowshape.png")
	    region = QtGui.QRegion(pixmap.mask())
	    self.setMask(pixmap.mask());

This will tell :code:`Qt` to use the image as a mask for the `window` region, effectively hiding any parts where the image is transparent.
More coffee, we're almost there. Right now, as you're swallowing that last sip, you're wondering "How do I move or close the :code:`window` without a border?". Fear not fellow coder for there is a solution for each of these:

To close the :code:`window` we just need to add a context menu. Simply done by adding one more function to your class:

.. code:: python

	def contextMenuEvent(self, event):
	    menu = QtGui.QMenu(self)
	    quitAction = menu.addAction("Quit")
	    action = menu.exec_(self.mapToGlobal(event.pos()))
	    if action == quitAction:
	        self.close()

You can of course replace the :code:`self.close()` with a call to some confirmation dialog if you want, but that will now enable a right-click menu on your GUI with a quit option. Also you can add keyboard shortcuts to the application as well if you are so inclined.

Now for moving the thing. Here we need two extra functions, one for the mouse move and one for the mouse press:

.. code:: python

	def mouseMoveEvent(self, event):
	    if (event.buttons() == QtCore.Qt.LeftButton):
	        self.move(event.globalPos().x() - self.drag_position.x(),
	            event.globalPos().y() - self.drag_position.y());
	    event.accept();
	
	def mousePressEvent(self, event):
	    if (event.button() == QtCore.Qt.LeftButton):
	        self.drag_position* = event.globalPos() - self.pos();
	    event.accept();

We just get the click position when the mouse button is pressed, work out the offset from the 
top left corner of the :code:`window` (this is what the move function uses) and then when 
the mouse moves, we move the `window` with it.

That's it really. Pretty simple once you know how. Now go and enjoy the rest of that coffee.
