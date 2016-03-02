Honeypotting with Dionaea and Raspi
###################################

:title: Honeypotting with Dionaea and Raspi
:date: 2015-07-16T00
:modified: 2015-07-16 12
:tags:


I recently setup a `dionaea <http://dionaea.carnivore.it/>`_ honeypot on my Raspberry Pi
and after tweaking and configuring it for a few days have now got a working setup.
It's a low interaction honeypot aimed to capture malware rather than ssh bruteforce 
attacks. 

I plan to leave it online for a week or a month, and the analyse the stats and see
what it managed to collect. So far it's mostly conficker variants, but there's a
suprising (to me) large number of infected machines out there. In one 8 hour period 
during testing, it managed to collect 8 unique samples from 154 connections.

Here's the stats from that period:

.. image:: "http://i.imgur.com/j828Fpw.png"


It should be fairly interesting to see if anything else comes along during its 
uptime.

