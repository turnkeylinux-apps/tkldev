Overview
--------

With TKLDev, building a TurnKey image from scratch is as easy as
grabbing the source and running make::

    root@tkldev ~$ cd core
    /turnkey/fab/products/turnkey/core
    root@tkldev turnkey/core$ make

If you can handle that you're ready to roll.

How hard is this?
-----------------

 "Simple things should be simple. Hard things should be possible."

 -- Alan Kay

If you have the skills to setup a Debian/Ubuntu system to do what you
want you are already 95% of the way to using TKLDev to create a
"productized" version of that. The learning curve isn't steep. What
TKLDev does is provide a convenient framework that supports a rapid
development cycle and automates away most of the drudge work.

The source code to the existing library of 100+ TurnKey images provides
a rich source of working examples you can borrow from.

TKLDev isn't TurnKey specific. You can build any Debian based Linux
distribution with it. We do use it a lot for TurnKey though so we've
been continually refining it to scratch our own itches and make common
tasks (e.g., installing packages, configuration files) as simple and
easy as possible.

The code footprint for most integrations is small, because most of the
basic functionality is inherited from the `common`_ repository. For
example, TurnKey Core is just 6 lines of TKLDev "code"::

    root@tkldev ~$ cd /turnkey/fab/products
    /turnkey/fab/products

    root@tkldev fab/products$ git-clone https://github.com/turnkeylinux-apps/core
    Cloning into core...

    root@tkldev fab/products# wc -l $(find core -type f|grep -v '\.git\|png\|jpg\|changelog\|README.rst\|txt$')
      3 core/Makefile
      1 core/plan/main
      2 core/conf.d/main
      6 total

The code for Core doesn't do much beyond inheriting from the common base::

    root@tkldev fab/products# cat core/Makefile 
    WEBMIN_FW_TCP_INCOMING = 22 12320 12321

    include $(FAB_PATH)/common/mk/turnkey.mk

    root@tkldev fab/products# cat core/plan/main 
    #include <turnkey/base>

    root@tkldev fab/products# cat core/conf.d/main 
    #!/bin/sh -ex
    echo "do nothing - core requires no post-package configuration commands"

TurnKey LAMP stack, which is slightly more complicated is still just 147
lines of "code"::

    root@tkldev fab/products$ git-clone https://github.com/turnkeylinux-apps/lamp
    Cloning into lamp...

    root@tkldev fab/products$ wc -l $(find lamp -type f|grep -v '\.git\|png\|jpg\|changelog\|README.rst\|txt$')
      11 lamp/plan/main
       1 lamp/overlay/etc/skel/.bashrc.d/php-xdebug
      17 lamp/overlay/etc/apache2/mods-available/status.conf
      23 lamp/overlay/etc/apache2/sites-available/default
      10 lamp/overlay/var/www/cgi-bin/test.cgi
      73 lamp/overlay/var/www/index.php
       1 lamp/overlay/var/www/phpinfo.php
       5 lamp/conf.d/main
       1 lamp/removelist
       5 lamp/Makefile
     147 total

The hard part usually isn't using TKLDev but getting the integration
details right (e.g., combining packages and configurations). 

If you're going to integrate a Linux system you're going to have to do
that anyway and test it, so why not to do it in a way that is well
documented and repeatable as opposed to an error prone manual process.
Your future self will appreciate it and so will everyone else that wants
to benefit from and build on your work.

Is TKLDev limited to building TurnKey related systems?
------------------------------------------------------

No! You can build any type of Debian based distribution you want.
Desktops, servers, embedded systems. 

There are no strings attached. If you don't want to, you don't have to
include common TurnKey functionality or any of the custom TurnKey
components.

Sadly, we've gotten into the nasty habit of prepending TKL - the TurnKey
Linux initials - to all things TurnKey but don't let that fool you.
Under the hood TKLDev is 100% general purpose.

Of course we'll be delighted if you end up using TKLDev to help us
improve TurnKey but everyone is more than welcome to use it for other
things as well.

Getting started
---------------

It's recommended to read through documentation in the following order:

1) `Setup`_: build your first image.
2) `Hello world`_: say hello by making your first change.
3) `Development`_: understand how stuff works in greater detail.
4) `Tips and tricks`_: reference collection of tips and tricks.

More advanced Linux users may be able to fast forward through most of it
and learn the most by examining a few real-life examples from the
TurnKey library: https://github.com/turnkeylinux-apps

If you find yourself confused, take a step back and read through the
rest of the documentation first to get an overview of how things works,
learn more about development best practices, etc. We've made this easy
enough so anyone that wants to can jump in and make cool stuff happen. 

.. _common: https://github.com/turnkeylinux/common
.. _Setup: ./getting-started/setup.rst
.. _Hello world: ./getting-started/helloworld.rst
.. _Tips and tricks: ./getting-started/tips.rst
.. _Development: ./development/README.rst

