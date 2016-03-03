Fix Kali Live Build error
#########################

:title: Fix Kali Live Build error
:date: 2015-03-25T00
:modified: 2015-03-25 06
:tags:


I was trying out the Kali Linux live build, and ran into an an issue where
the :code:`lb build` command would throw an error: :code:`chroot: failed to run command '/usr/bin/env': No such file or directory`

Turns out this is a Debian bug that's been around since 2013. Luckily the fix
is straightforward. First follow the usual `live build instructions <http://docs.kali.org/development/live-build-a-custom-kali-iso>`_
and then make sure the `Kali repo sources are set <http://docs.kali.org/general-use/kali-linux-sources-list-repositories>`_.

Now in order to fix the issue we follow the instructions provided in 
`this bug report <https://bugs.kali.org/view.php?id=270>`_. I'll write it down here, 
in case I need to refer back to it later. I've also updated the version of
the :code:`libdebian-installer` package to the latest available at this time.

.. code:: console

	apt-get remove --purge libdebian-installer4
	wget http://ftp.debian.org/debian/pool/main/libd/libdebian-installer/libdebian-installer_0.99.tar.xz
	tar xvf libdebian-installer_0.99.tar.xz
	cd libdebian-installer-0.99
	grep -R parser_rfc822 src
	apt-get install automake libtool
	autoreconf -i -v
	./configure
	make
	make install
	git clone git://git.kali.org/live-build-config.git
	cd live-build-config/
	lb config
	lb build

After this the build ran fine.
