YouCompleteMe
#############

:title: YouCompleteMe
:date: 2013-11-07T12
:tags:


If you haven't heard of the YouCompleteMe plugin for Vim, headover to 
`http://valloric.github.io/YouCompleteMe/ <http://valloric.github.io/YouCompleteMe/>`_ and take a look.
It's a very competent auto completer for a variety of languages. But as always the C style completer takes
a little bit of work to get going. So just for you, I've written up how I managed to get it to work
on 64bit Centos 6.2.

<!--more-->

So using `Vundle <https://github.com/gmarik/vundle) install YouCompleteMe (referred to as YCM from now on>`_.
Now we need to build clang. I managed to get this done by following `these steps <http://clang.llvm.org/get_started.html>`_.
Use :code:``CC="/usr/bin/gcc" CXX="/usr/bin/g++" ../llvm/configure`` to configure it.

You will end up with a directory called :code:``build`` that contains almost everything. All you have to do is copy the 
:code:``llvm/tools/clang/include/clang-c`` folder from the original checkout (step 2 if you follow the clang guide) to 
:code:``build/include``.

Now we need to build the YCM tools according to the docs. Here's the command I used:

.. code-block:: bash

	cmake -G "Unix Makefiles" -DPATH_TO_LLVM_ROOT=/tmp/build -DEXTERNAL_LIBCLANG_PATH=/tmp/build/Release+Asserts/lib/libclang.so . ~/.vim/bundle/YouCompleteMe/cpp

adjust the paths as necessary. After the configure stage run

.. code-block:: bash

	make ycm_support_libs

And with some patience you are done.

Now you need to add a :code:``.ycm_extra_conf.py`` to your project and you should start seeing autocompletion.
    
