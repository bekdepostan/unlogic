Don't be a dict
###############

:date: 2016-04-05
:tag: python, dict
:category: programming

You're probably familiar with the :code:`__dict__` attribute of Python 
classes. If not, it basically lists that object's attributes.

.. code:: python

    >>> class A():
    ...     var = 0
    ...     def test(self):
    ...             pass
    ... 
    >>> A.__dict__
    {'test': <function test at 0x7f498ab085f0>, 'var': 0, '__module__': '__main__', '__doc__': None}
        
So why is this useful? Well I recently used this to allow users
to leverage a member variable to define an element in a path. The class
computes a path and the user can use it like this

.. code:: python

    the_class.path = {'new_path': '{computed_path}/myfolder'}

and in the code it would do

.. code:: python

    user_path = new_path.format(**self.__dict__)

This will replace the :code:`{computed_path}` in the string (new_path)
with the value from :code:`self.computed_path`, or specifically,
:code:`self.__dict__['computed_path']`

Of course :code:`self` has a :code:`computed_path` member variable.

All good so far? Right, so where am I going with this? Well the problems
roll in when you want to do things a bit different and use properties to
access your variables. Because properties don't show up in :code:`__dict__`.

Usually you will have a :code:`_var` as a member, and a :code:`var` that
is your getter/setter. Only the :code:`_var` shows up however. So the above
code will not work, unless your users use the underscore variable, which
isn't very friendly. 

So if you are relying on :code:`__dict__` somewhere in your code, make sure
you bear this in mind when you are considering using properties instead of 
accessing the variables directly.
