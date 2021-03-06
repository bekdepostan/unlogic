Dominos CLI Update
##################

:title: Dominos CLI Update
:date: 2015-03-15T00
:modified: 2015-03-15 06
:tags: []


Small update on some progress and changes. Setting the store is now done by
enetering your postcode and the nearest delivery store to that postcode is 
automatically selected. Setting the address also works and isn't just a stub,
and finally it is also able to determine if cash on delivery is available to you,
albeit at the end of the process, but that's how they do it.

.. raw:: html

    <script type="text/javascript" src="https://asciinema.org/a/17706.js" id="asciicast-17706" async></script>

So the API is coming along and the CLI interface (which is mostly just a proof
of concept for the API) is also shaping up. Once cash on delivery orders are working
I reckon it's time to release it. Then work on investigating how credit card orders
are handled will start.

It's a fun, fairly pointless, and interesting ride :)

`Now on Github <https://github.com/Svenito/dominos>`_
