The joys of server ownership
############################

:title: The joys of server ownership
:date: 2015-05-08T00
:modified: 2015-05-08 13
:tags:


This post serves mostly as a "note to self".

I just ordered myself a super cheap VPS from `Ramnode <http://ramnode.com>`_ as I have
a little project I would like to setup and see if I can make it work.

But first I had to setup the server (Debian 7.0) and it's been a while since I've done that, so
some reading was in order to remind myself of all the joys. Thus I decided to note this
down for myself and anyone else who's interested. So it's not an in depth explanation
by any means.

Securing ##
-----------

I'm not looking for bullet proof as this won't be a production server and won't
hold any sensitive info, but I'd like to know that it's at least somewhat locked
down.

So first off install `Fail2ban <http://www.fail2ban.org/wiki/index.php/Main_Page>`_. This
will lock out users who fail to authenticate too often. Ramnode actually have a
`good video on this <https://www.youtube.com/watch?v=GmVoqFv_lGU>`_. As we'll
only allow key based authentication it's a bit redundant, but if you want to
go that way, there's the info.

Then turn off password authentication for SSH as I'll be using only keys to 
authenticate. Edit :code:`/etc/ssh/sshd_conf` and change the following lines to read:

.. code:: console

	ChallengeResponseAuthentication no
	PasswordAuthentication no
	UsePAM no

Make sure you have uploaded your `public key <https://help.ubuntu.com/community/SSH/OpenSSH/Keys>`_ to
:code:`~/.ssh/authorized_keys` and set the permissions on :code:`.ssh` and :code:`authorized_keys` on the
server to :code:`700` and :code:`600` respectively.

I also changed the default SSH port to something else, as that already keeps the number of automated 
bruteforcers down. Do this by changing the following line in :code:`/etc/ssh/sshd_config`

.. code:: console

	Port 22

Set it to anything that doesn't clash with other services. i.e. not 25 or 80 for example.

Once configured :code:`sudo service sshd reload` to pick up the changes.

So next up `iptables`. I followed `this guide <https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-using-ip-tables-on-ubuntu-12-04>`_
which gives you a good start. Be sure to run :code:`sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT` first.
Otherwise you'll end up blocking your current connection and... yeah, ok, I made that mistake.

Then allow what you need and default to dropping the rest. It's all in the URL above, but to re-iterate:

.. code:: console

	# Accept connections on port 22
	iptables -A INPUT -p tcp --syn --destination-port 22 -j ACCEPT
	
	# Deny all other input
	iptables -A INPUT -p tcp -syn -j DROP

You will need to run the first line for each port that needs to be able to accept
incoming connections. 

I additionally set up `knockd <http://www.zeroflux.org/projects/knock>`_ just to play around with it.

To do this edit :code:`/etc/knockd.conf` and set the port sequences. It should have a default
set for enabling and disabling the ssh port. Edit this to reflect any port changes. If you want to run miltiple commands
for a knock, simply concatenate the command with :code:`&&`. You can even make one command open
a port for a given time. As we have our *keep established connections* rule in :code:`iptables` we 
can do

.. code:: console

	[opencloseSSH]
	        sequence      = 2222:udp,3333:tcp,4444:udp
	        seq_timeout   = 15
	        tcpflags      = syn,ack
	        start_command = /usr/sbin/iptables -A INPUT -s %IP% -p tcp --syn --dport 22 -j ACCEPT
	        cmd_timeout   = 10
	        stop_command  = /usr/sbin/iptables -D INPUT -s %IP% -p tcp --syn --dport 22 -j ACCEPT

Lifted from the docs. This will allow and block only the IP from where the knock originated.

That's all for now. Postfix next time....
