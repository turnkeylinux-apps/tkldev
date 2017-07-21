Building Packages from Source
=============================

As of v14.2, TKLDev includes all the components needed to build appliances
including packages built from souce code on the fly. This may be useful if you
wish to test a piece of software which is unpackaged, but you want it packaged.
It can also be useful if you wish to tweak an existing TurnKey package before
it is offically built.

Before you start
----------------

Before you can build any packages, you need to ensure that Chanko is fully
configured and has been pre-loaded with packages. If you haven't already done
that, please see docs/building-appliances-offline.rst

Build a buildroot
-----------------

Before you can build packages, you'll need a buildroot to build them in. We'll
probably provide one that can be downloaded, but until then you'll need to
build it yourself. Once you've configured Chanko, it's actually really easy!
You just need to do this:

.. code-block:: bash

    CODENAME=$(lsb_release -c | cut -f2)
    cd $FAB_PATH/products
    git clone https://github.com/turnkeylinux/buildroot.git
    cd buildroot
    export FAB_POOL=y
    export RELEASE=debian/$CODENAME
    make

Once that has finished, you just need to move your buildroot to where Pool is
expecting it to be:

.. code-block:: bash

    rsync --progress --delete -Hac build/root.patched/ /turnkey/fab/buildroots/jessie/

Build a package from source
---------------------------

Now it's time to build a package! For this test I'm going to build TurnKey's
ccurl package. So let's clone the source code first:

.. code-block:: bash

    mkdir /turnkey/public
    cd /turnkey/public
    git clone https://github.com/turnkeylinux/ccurl.git

Now we'll register this source code with pool and build the package:

.. code-block:: bash

    cd pools/jessie
    pool-register /turnkey/public/ccurl
    pool-get . ccurl

And after a few moments, you should find the ccurl Debian package ready for use:

.. code-block:: bash

    root@tkldev pools/jessie# ls
    ccurl_0+2015.2.13+13.16.45+1ec9bb04_amd64.deb

You can now move this .deb to where you wish to use it and install with dpkg. 
Alternatively, if you are building an appliance you can automatically include
this package by building with 'export FAB_POOL=y'. Note though, you will need
to ensure that Chanko has all the other required packages already cached.
See docs/building-appliances-offline.rst
