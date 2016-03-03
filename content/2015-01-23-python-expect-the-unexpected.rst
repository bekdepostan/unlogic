Python
#######

:title: 'Python
:date: 2015-01-23T00
:modified: 2015-01-23 09
:tags:


I've not really had much of a play with Python 3, but I'm aware of some of its
differences. Yesterday I found out about a difference that took me by surprise.
Enough of a surprise that I felt the urge to write this post. 

Opinion Divided
===============

What surprised me was how :code:`/` has changed in Python 3. In Python 2.7 it returns
the result of the division of two numbers.

.. code:: python

	>>> 8/2
	4
	>>> 10/3
	3

Checks out to me. :code:`10 / 3` is 3.3333, and because we are using integers in
the expression, we expect an integer as the result.
Change the input to floats (or at least one of the inputs)

.. code:: python

	>>> 10/3.0
	3.3333333333333335

and we get a float. Right, nothing weird there. Where it starts getting odd is 
that in Python 3 you **always** get a float back, unless you use the :code:`//` operator.
Apparently that is because too many people expected integer division to return a float.
Maybe it's just me and my fellow oldies who think that the original behaviour is
correct and integer division should yield an integer, not a float. Pretty much all
main stream languages behave like this. In C/C++ you need to cast one of the arguments
to a float to get a float back.

.. code:: cpp

	#include <iostream>
	
	int main () {
	    std::cout << 10 / 3 << std::endl;
	    std::cout << (float)10 / 3 << std::endl;
	
	    return 0;
	}

.. code:: console

	$] ./a.out 
	3
	3.33333
 
I understand that if you are dividing numbers you will want to have 
the accuracy of the float type, but I find this a bit of an odd choice 
for the Python devs to make. But perhaps this is the future, and I'm
just too old to accept what you whippersnappers are up to with your
fancy `languages and tools <http://i.imgur.com/GUum4gy.gif>`_.

Ultimately, does it really matter? Well yes and no. No, because Python is
dynamically typed, so it doesn't really matter what type the result is, whatever
it gets assigned too will become what it needs to. Yes, because there may be
times when getting a float might cause unexpected behaviour. 

It's not the end of the world as such, because the *no* above greatly 
outweighs the *yes*, but I'm still a little surprised at this change. I would 
perhaps have kept :code:`/` as it is and made :code:`//` the one that always returns a float.

And just to finish:

.. code:: python

	Python 3.4.0
	>>> 10//3
	3
	>>> 10//3.0
	3.0

`Yeah, sure, why not? <http://i.imgur.com/WEllYN3.gif>`_

