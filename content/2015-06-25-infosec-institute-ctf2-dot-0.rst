Infosec Institute CTF2.0
########################

:title: Infosec Institute CTF2.0
:date: 2015-06-25T00
:modified: 2015-07-06 19
:tags:


The folks over at the `Infosec Institue <https://infosecinstitute.com>`_ have released
their `second CTF <http://ctf.infosecinstitute.com/ctf2/>`_. Here's how I got on...

Level 01 #
==========

In `level 01 <http://ctf.infosecinstitute.com/ctf2/exercises/ex1.php>`_ I am supposed
to use the provided form to perform a cross site scripting exploit. Here's what the form
looks like:

.. image:: "http://i.imgur.com/CJTNyK4.png"


At first I might as well test how the form works. Entering something like :code:`test` and
:code:`www.test.com` in the fields simply adds the supplied information to the column on the left.
So I try the usual XSS payload: :code:`<script>alert("Ex1");</script>` in the :code:`Site Name` field.

A popup tells me that I need to *match the requested format*. Probably some client side
checks, so I inspect the field with Firebug and notice this:

.. image:: "http://i.imgur.com/f5KzFDx.png"


The field has a regular expression premitting only upper or lowercase characters. I can either
delete this or just change it to :code:`.+` so it matches any character.

Now resubmitting the XSS payload works and the string is reflected on the page:

.. image:: "http://i.imgur.com/yvSc4To.png"


However, there's no pop up. So there must be something else validating input. Heading back to the
source I find some javscript in :code:`ex1.js` which contains the following code:

.. image:: http://i.imgur.com/VVe74tW.png
    :target: http://i.imgur.com/VVe74tW.png

The :code:`siteName` variable has all :code:`<` and :code:`>` characters replaced with their equivalent html codes.
By clicking on the gutter in the source code I set a breakpoint on the line that does this, and resubmit
my data. The Firebug debugger breaks on the line and I step over it. Sure enough :code:`siteName` is not
what I want it to be. Double clicking on the value in the right hand window allows me to edit it, and 
revert it back to what I want it to be. Then clicking continue I am rewarded with:

.. image:: "http://i.imgur.com/VEFDpio.png"


Level 02 #
==========

`Level 02 <http://ctf.infosecinstitute.com/ctf2/exercises/ex2.php>`_ is a simple web calculator:

.. image:: "http://i.imgur.com/asgTWCw.png"


I'm supposed to use the form to print :code:`phpinfo` or other data to the page. This is a PHP
script evaluating a simple expression. I am guessing that it's going to be calling :code:`eval`, as
that's a fairly common vulnerability, and fits to how the page works. After entering some numbers
and other characters into the two fields I quickly learn that the input for those fields is checked.
That means I can't enter anything but numbers into those fields. That leaves the operator as the only 
other thing under our control. 

I'm going to guess that code looks somewhat like this:

.. code-block:: php

	eval ("print $num1 $op $num2;");

So I need to change the operand to something that prints :code:`phpinfo` but leaves the rest of the statement
valid. With Firebug I can edit the value of the operand to the following:

.. image:: "http://i.imgur.com/8xnqMxv.png"


Hit submit and....

.. image:: "http://i.imgur.com/rUgaixe.png"


Level 03 #
==========

`Level 03 <http://ctf.infosecinstitute.com/ctf2/exercises/ex3.php>`_ provides me with a registration
form and a login form. The instructions indicate that the data is stored in a delimited file and I need
to sign up as a new user with admin rights.

.. image:: "http://i.imgur.com/f0g5TmV.png"


First things first, let's see if we can figure out the delimiter... Signing up and logging in
shows us our name and current role: :code:`role:normal`. This already tells me that the delimiter is not
:code:`:`. After fuzzing the input it turns out most characters are ok to use. So what's the delimeter?
I check the hints and it tells me that it's the newline character. Interesting, in my fuzzing I tried that,
but had no luck. Unless..

So let's not use :code:`\n` but a real new line. I can achieve this by editing the source with Firebug
once again, changing the :code:`lastname` field to a :code:`textarea` type:

`{{< figure src="http://i.imgur.com/QBVptMv.png" >}} <http://i.imgur.com/QBVptMv.png>`_

Now I can have multiple lines and enter a real carriage return into the field. My last
name will be

.. code-block:: console

	alpha7
	role:admin

And after a login with the new creds:

.. image:: "http://i.imgur.com/Akj9NL8.png"


Level 04 #
==========

`Level 04 <http://ctf.infosecinstitute.com/ctf2/exercises/ex4.php>`_ 

.. image:: http://i.imgur.com/nmRe8U2.png
    :target: http://i.imgur.com/nmRe8U2.png

Here we need to load a php file instead of the text files that load when you click
on the *Bio*, *Clients*, or *About* buttons. The instructions are very clear,
but it sounds like we need to load a phop file from the root of the domain. Let's
see what restrictions are in place.

Fuzzing the file parameter I notice that it seems to test for :code:`fileNiXtxt` where *N* is
any number and :code:`X` is any other character. Anything other than that pattern will print :code:`Invalid file selected.`.

Entering :code:`index.php;file1.txt` for example gives a different error: :code:`There is something else that you must do.`.
Interesting. So I guess it just needs to be somewhere in that argument for the filter to accept it. But
how can we accomplish this with a valid payload?

One thing I tried was :code:`/file1/txt/../../file.php` which wasn't right either. Here we make use
of relative paths where when PHP opens the file, it will ignore the fact that the path
:code:`/file1/txt` doesn't exist and treat this as if :code:`file.php` as at :code:`/`. 

UPDATE: Solved

So the key bit I was missing was that it wanted a remote, even if that remote is the
same domain as the current page. So I added :code:`http://infosecinstitute.com/file3.php` as
the argument to get a new error: *You are trying to add a remote URL.* Ok, now we are getting somewhere.
As one of the hints is that the regex might be case sensitive, let's capitalise the :code:`h` in :code:`http`.
This time we get an *invalid file* message, so that bypass worked. Now we need to satisfy the
:code:`file3.txt` requirement and using :code:`Http://infosecinstitute.com/file3.txt.php` I get the flag

.. image:: http://i.imgur.com/WTFYtJi.png
    :target: http://i.imgur.com/WTFYtJi.png


Level 05 #
==========

`Level 05 <http://ctf.infosecinstitute.com/ctf2/exercises/ex5.php>`_ starts by telling
me that I am not logged in. 

.. image:: "http://i.imgur.com/BOBdkHX.png"


Well, I don't remember logging in, so that's not unusual. What is unusual is
that the :code:`login` button doesn't work. I'll quickly check the source code and notice
that it's disabled, but also that it points to :code:`login.html`. Enabling and clicking it
takes me to a 404, so no go. The vulnerability here is *Missing Function Level Access Control*
so perhaps this page assumes we're logged in if we are coming from the login page. Let's 
assume that if the user is successful on :code:`login.html`, that page will redirect here, and then 
this page will just assume that the user is allowed to be here.

Using an intercepting proxy I'll edit the :code:`Referer` field in the original request, so that
it appears to be coming from the login page:

.. image:: "http://i.imgur.com/EK9u7Ir.png"


Forward the request and

.. image:: "http://i.imgur.com/QCisDvN.png"


Level 06 #
==========

`Level 06 <http://ctf.infosecinstitute.com/ctf2/exercises/ex6.php>`_ shows a nice
big text area with allowable HTML tags.

.. image:: "http://i.imgur.com/Waq1AVN.png"


This time I need to perform a cross site request forgery. This can be accomlished by an :code:`href`
tag, but trying this tells me that they are expecting something that will perform the request
without the need for user interaction. Ok, fine, let's revisit the allowed tags. :code:`img` looks useful, right?

Let's try the following

.. image:: "http://i.imgur.com/qCd5NUP.png"


Yep, that's what we needed. 

Level 07 #
==========

`Level 07 <http://ctf.infosecinstitute.com/ctf2/exercises/ex7.php>`_ is a login form on which
we need to perform another XSS attack. 

.. image:: "http://i.imgur.com/WO8dRpe.png"


Well, lucky for me I perform these challenges through a proxy which unhides hidden fields like
the one you see there. Some investigation shows that the value of the hidden field comes from
a php_self value. That is it uses whatever the URL part is to populate the field, so that form
is submitted back to itself.

Using this we can inject something into the field to hopefully reflect our data on the page.
By employing the :code:`arg` paramater we can close the :code:`input` tag, and the inject our :code:`h1` tags:

.. code-block:: console

	http://ctf.infosecinstitute.com/ctf2/exercises/ex7.php?arg='><h1>username</h1>

Submitting that puts :code:`username` on the page surrounded by :code:`h1` tags and nabs the flag

Level 08 #
==========

`Level 08 <http://ctf.infosecinstitute.com/ctf2/exercises/ex8.php>`_

.. image:: "http://i.imgur.com/610ZNNq.png"


Here we need to upload an image that will produce a javscript alert. First things first with these
things I upload an image to see how it behaves. Once uploaded I click on the example links and notice that
images are fetched via an id. The URL is 

.. code-block:: console

	http://ctf.infosecinstitute.com/ctf2/exercises/ex8.php?attachment_id=1

So let me see if I can access an image via another ID, for example :code:`id=4`.
I get the message:

.. code-block:: console

	This attachment is currently under review by our editors. 

So no. Checking out the image URL for one of the chess images shows me that the images
are stored at :code:`http://ctf.infosecinstitute.com/ctf2/ex8_assets/img/chess1.png` for example.

I make a note of this.

Now can I just upload an html file? That gives me an error of an invalid file type. So let me chack
if it's just checking the extension or if there's something more happening. Intercepting the upload
request with Burp proxy I can change the extension to :code:`jpg` and sucessfully upload the html file.

Now browsing to the image url I am told it cannot display the image due to errors. Well, the browser
is trying to interpret the file as an image, which it clearly isn't. There's got to be another way
to get at my image. How about the object reference in the URL :code:`http://ctf.infosecinstitute.com/ctf2/exercises/ex8.php?attachment_id=1`
for example? Maybe if I just reference the filename directly?

.. code-block:: console

	http://ctf.infosecinstitute.com/ctf2/exercises/ex8.php?file=index.jpg

Success

`{ %img http://i.imgur.com/RVoJGMr.png %} <http://i.imgur.com/RVoJGMr.png>`_

Level 09 #
==========

`Level 09 <http://ctf.infosecinstitute.com/ctf2/exercises/ex9.php>`_ starts off by showing me the 
details of one John Doe.

.. image:: "http://i.imgur.com/8NESmpB.png"


I need to change something to make it show the details for Mary Jane. There's no URL parms,
no login, so how can the page know who to show? There's one place left: the cookie jar.

Using Firebug once again I inspect the cookies and sure enough

.. image:: "http://i.imgur.com/xGdtDa7.png"


This is "JOHN+DOE" encoded as base64 as it turns out. One thing to note is when you

.. code-block:: console

	echo Sk9ITitET0u= | base64 -d

there is no newline at end of the name. So to encode :code:`MARY+JANE` correctly I need to 
use echo with the :code:`-n` flag:

.. code-block:: console

	$> echo -n MARY+JANE | base64
	TUFSWStKQU5F

Editing the cookie and inserting that base64 string will show us Mary Jane's details.

Level 10 #
==========

`Level 10 <http://ctf.infosecinstitute.com/ctf2/exercises/ex10.php>`_ is a game and we need to
edit its source so we look like we're really good at it.

.. image:: "http://i.imgur.com/g03njlQ.png"


Entering anything in the name I field I have a poke around to see how the whole thing
works. We're shown some coloured squares and then they are turn over. We need to then 
remember which colour each square had. Except we need to do it at least 9999 times and
at the extreme level, which only shows us the squares for a second.

Finding the square colours isn't hard. With Firebug we can see:

.. image:: "http://i.imgur.com/isDO7LM.png"


and those numbers are 0 indexed into the list of numbers from the selction popup. So playing
along I can win one game. So let's find out where my current win/loss count is stored.

In the Javscript I find a structure that does this:

.. image:: "http://i.imgur.com/gZghIIn.png"


but all this does is increment and decrement the values. Clearly that data is stored somewhere. 
Turns out that this :code:`localstorage` is in the DOM. Using the *DOM* tab in Firebug I can find
the structure and its data:

.. image:: "http://i.imgur.com/xGIZXpb.png"


Now I can edit the number of wins and then, all I need to do is play one more game to take the flag.

Level 11 #
==========

`Level 11 <http://ctf.infosecinstitute.com/ctf2/exercises/ex11.php>`_ blacklists me

.. image:: "http://i.imgur.com/RaGy98O.png"


Awwwww I was having such fun. But how? Not from my IP, as that's going to change. First thing
to check: cookie jar. Yay!

.. image:: "http://i.imgur.com/QgGrvwE.png"


There it is, a big :code:`no`. I'll change that to a :code:`yes`, reload and take the flag, thanks very much.

Level 12 #
==========

`Level 12 <http://ctf.infosecinstitute.com/ctf2/exercises/ex12.php>`_ is a bruteforce challange. No 
login attempt limits, no rate limits, so it's ripe for the picking.

.. image:: "http://i.imgur.com/LMUBNoq.png"


After searching for the suggested password list, the first hit is the Openwall password list for
john the ripper. So why not download it and give it a try?

I fire up :code:`wfuzz` with the following commandline

.. code-block:: console

	$> wfuzz -c -z file,/usr/share/wordlists/password-2011.lst --hw Incorrect -d "username=admin&password=FUZZ&logIn=Login" "http://ctf.infosecinstitute.com/ctf2/exercises/ex12.php"

Within a few seconds I get a hit with :code:`princess`. Enter that with the username :code:`admin` and onto the next level

Level 13 #
==========

`Level 13 <http://ctf.infosecinstitute.com/ctf2/exercises/ex13.php?redirect=ex13-task.php>`_ is actually
redirect to :code:`ex13-task.php`. I need to make the redirect point to an external page so that to another user
it looks like they are visiting :code:`ctf.infosecinstitute.com` but are infact taken to another site

.. image:: "http://i.imgur.com/jNgQ4Ww.png"


Well the obvious thing is just to try and type in another URL :code:`http://ctf.infosecinstitute.com/ctf2/exercises/ex13.php?redirect=http://unlogic.co.uk`
but that gives me an error. Hrmm... trying a few other redirect options tells me that the redirect is URL 
relative, which means if I strip off the protocol off the URL, I should be able to make this work:

.. image:: http://i.imgur.com/QM7V8Dk.png
    :target: http://i.imgur.com/QM7V8Dk.png

Sure enough, that worked. That's it, the final flag.

Thanks to the Infosec Institute for another great CTF!
