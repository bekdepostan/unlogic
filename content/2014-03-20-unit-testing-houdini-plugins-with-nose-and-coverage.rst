Unit testing Houdini Python plugins with nose and coverage
##########################################################

:title: Unit testing Houdini Python plugins with nose and coverage
:date: 2014-03-20T00
:modified: 2014-03-20 12
:tags:


We all know how important unit testing is, right? But often you wonder how can 
you test a not so straight forward tool. In this case we're talking about a
Python script intended to run inside `Houdini <http://sidefx.com>`_. In my specific
case the python script is launched from a script on a node when the user clicks
a button on the OTL. I want to run unit tests on this script, but the problem is
that the script parses a set of nodes and does various things according to the
types of nodes and layout of the nodes. It's clear that the HOM is required in the
unit tests. So I need to somehow run my unit tests inside houdini and have
some nodes available for my testing. Fortunately this isn't difficult to do, but
it does require a little setup and some fiddling in order to get it to work.

I'll be using `nose tests <https://nose.readthedocs.org>`_ as my test runner and
`coverage <http://nedbatchelder.com/code/coverage/>`_ for coverage testing.
Because I want to make sure I test as much code as possible. I created a hip file that
contains whatever nodes and connections I need to run most of the tests and saved
this to the same directory as my test script. 

Before we write some code you will need to install :code:`nose` and :code:`coverage` and make
sure they work.

Now that we have all our dependencies installed, we need to import all the 
modules we need and set some things up.

.. code-block:: python

	
	import nose
	import sys
	sys.path.insert(0, '../path_of_module')
	
	import os
	os.environ['NOSE_WITH_COVERAGE'] = '1'
	os.environ['NOSE_COVER_PACKAGE'] = 'module_to_test'
	
	import hou
	
	import module_to_test
	

We import the :code:`nose` module and then we need to tell nose to make use of the
coverage package. :code:`os.environ['NOSE_WITH_COVERAGE'] = '1'` does just that, and
:code:`os.environ['NOSE_COVER_PACKAGE'] = 'module_to_test'` restricts our test results to
the module(s) we want to test. If you want to specify multiple modules simply
separate them with commas: :code:`os.environ['NOSE_COVER_PACKAGE'] = 'module_to_test,another_module'`

Unfortunately for this to work properly you need to patch nose's cover plugin.
There's a small bug in older versions, so depending on your distro you may need to 
make the following change to 
:code:`nose/plugins/cover.py`

Change these lines
.. code-block:: python

	for pkgs in [tolist(x) for x in options.cover_packages]:
	    self.coverPackages.extends(pkgs)

to these lines
.. code-block:: python

	for pkgs in tolist(options.cover_packages):
	    self.coverPackages.append(pkgs)

Otherwise the :code:`NOSE_COVER_PACKAGE` variable won't work properly.

I also setup the :code:`sys.path` so that I load my local module rather 
than the globally installed one. Depending on how your directories are laid out
you might not need this.

After this we need to import the :code:`hou` module and finally the module(s) we want to test.

Then we write our main function which will load our hip file and start our tests

.. code-block:: python

	
	if __name__ == '__main__':
	    hou.hipFile.load('/path/to/test.hip')
	
	    nose.run(argv=[__file__], '--cover_html'])
	

As you can see, you can pass the commandline argments for nose into the run function.
With :code:`--cover_html` we automatically generate the html coverage information. You
could omit this and run :code:`coverage html` after the tests complete to generate the
html coverage pages instead. The output from the two methods is slightly different,
so pick the one that you prefer.

The next bits are up to you now, here you write your tests following a format like

.. code-block:: python

	
	def test_afunction():
	    node = hou.node('/obj/geo/box1')
	    result = module_to_test.do_stuff(node)
	    assert (result == 4)
	

You can access any and all :code:`hou.` calls from your tests, so do what you must.

Once you are happy with your tests, or you just want to go ahead and test a single
one, we need to run the tests through hython. Bear in mind that you'll consume a
batch license when you run these tests.

.. code-block:: bash

	
	hython ./test.py
	

where :code:`test.py` is the name of the file that contains the tests you wrote.
After a while you'll see your tests run and the coverage output. It should
look a little like this

.. code-block:: bash

	
	...
	Name          Stmts   Miss  Cover   Missing
	-------------------------------------------
	module_to_test  25     14    44%   1-2, 6, 9, 12-15, 21, 27-32
	another_module  314    173    45%   4-20, 24, 37-38, 46
	-------------------------------------------
	TOTAL           339    187    45%   
	----------------------------------------------------------------------
	Ran 3 tests in 0.053s
	
	OK
	

You'll also have a directory called :code:`cover` which will contain the html output,
assuming you have the :code:`--cover_html` flag on. If not, run :code:`coverage html` and 
after a short wait you will have a :code:`htmlcov` directory with the html coverage 
info.

I hope this helps you out if you ever wanted to unit test your Houdini Python
script. It's not as difficult as I thought, but it does take a little bit of setting
up to get everything to work right. There will still be some limitations as to what
you can test and get results for, but any testing is always better than none at
all I say.

And the :code:`test.py` file as a whole

.. code-block:: python

	import nose
	import sys
	sys.path.insert(0, '../path_of_module')
	
	import os
	os.environ['NOSE_WITH_COVERAGE'] = '1'
	os.environ['NOSE_COVER_PACKAGE'] = 'module_to_test'
	
	import hou
	
	import module_to_test
	
	
	def test_afunction():
	    node = hou.node('/obj/geo/box1')
	    result = module_to_test.do_stuff(node)
	    assert (result == 4)
	
	
	if __name__ == '__main__':
	    hou.hipFile.load('/path/to/test.hip')
	
	    nose.run(argv=[__file__], '--cover_html'])
