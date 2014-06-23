Overview
--------

With TKLDev, building an appliance from scratch is as easy as grabbing
the source and running make::

    root@tkldev ~$ cd core
    /turnkey/fab/products/turnkey/core
    root@tkldev turnkey/core$ make

If you can handle that you're ready to roll.

"Simple things should be simple. Hard things should be possible."

 -- Alan Kay

Developing new Linux distributions with TKLDev is easy. It has to be. We
use it to develop and maintain the 100+ ready-to-use apps in the TurnKey
library so we've gone to great lengths to make common tasks (e.g.,
installing packages, configuration files) as simple as possible.

The code footprint for most apps is very small. For example, our minimal
base appliance, TurnKey Core is just 4 lines of TKLDev "code"::

    root@tkldev ~$ cd /turnkey/fab/products
    /turnkey/fab/products

    root@tkldev fab/products$ git-clone https://github.com/turnkeylinux-apps/core
    Cloning into core...

    root@tkldev fab/products$ wc -l $(find core -type f|grep -v '\.git\|png\|jpg\|changelog\|README.rst\|txt$')
      1 core/plan/main
      3 core/Makefile
      4 total

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

The hard part usually isn't getting the integration details into TKLDev
but testing that they work properly.

Is TKLDev limited to building TurnKey related systems?
------------------------------------------------------

Nope. You can build any type of Debian based distribution you want. No
strings attached. If you don't want to, you don't have to include common
TurnKey functionality or any of the custom TurnKey components.

Sadly, we've gotten into the nasty habit of prepending TKL - the TurnKey
Linux initials - to all the TurnKey related stuff we develop but don't
let that fool you. Under the hood TKLDev is general purpose.

Of course we'll be delighted if you end up using TKLDev to help us
improve TurnKey but everyone is more than welcome to use it for other
things as well.

Getting started
---------------

Advanced Linux users can probably skip the documentation and just take a
look at a few examples from the TurnKey library source code:
https://github.com/turnkeylinux-apps

If you find yourself confused, take a step back and read through the
rest of the documentation first to get an overview of how things works,
learn more about development best practices, etc.

Hopefully, we've made this stuff easy enough to use so nearly anyone
with the inclination can jump in and make cool stuff happen. 

All the hard, really technical bits are automated so you don't need a
lot of Linux experience to work with TKLDev. The same amount of
experience you'd need to install and configure a regular Debian
installation will take you a long way. The difference is that with
TKLDev you can mass reproduce the results and collaborate with others on
the integration details in ways you couldn't do otherwise.

Documentation
-------------

* `Setup`_
* `Development`_

.. _Setup: setup.rst
.. _Development: development/README.rst

