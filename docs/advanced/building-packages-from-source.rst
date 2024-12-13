Building Packages from Source
=============================

TKLDev includes most of the components needed to build Debian packages from
souce code OOTB. This can be useful if you want to test changes you've made
to an existing package or create a new package - of your code or someone
else's.

Environment variables
---------------------

.. code-block:: bash

    # assuming building for the current TurnKey/Debian version
    CODENAME=$(lsb_release -sc)

Buildroot
---------

A buildroot is a minimalist Debian chroot_ specifically for building packages
in.

TurnKey uses our bootstrap_ as a base, then adds some extra build related
tools/packages. To generate one yourself, see the buildroot_ repo.


Pool configuration
------------------

Pool_ is the custom TurnKey tool for building packages. With the exception
of a buildroot, TKLDev should have pool configured out of the box. So once
you have built your buildroot you should be good to go.

Build a package with pool
-------------------------

I'll use TurnKey's "inithooks" package as an example:

Clone or copy your source code to an appropriate location:

.. code-block:: bash

    mkdir /turnkey/public
    cd /turnkey/public
    git clone https://github.com/turnkeylinux/inithooks.git

Then register the source code with Pool and build the package:

.. code-block:: bash

    cd pools/${CODENAME}

    pool-register /turnkey/public/inithooks
    pool-get . inithooks

Assuming that the build process completes successfully, you will find the new
Debian package in the pool directory:

.. code-block:: bash

    root@tkldev pools/bookworm# ls
    inithooks_2.2.1_all.deb

If you wish, the package can be installed on the local system using apt:

.. code-block:: bash

   apt install ./inithooks_2.2.1_all.deb

Alternatively, the package can be used when building an appliance by adding the
package name to the appliance plan (if required) and setting `FAB_POOL=y` prior
to appliance build. E.g.:

.. code-block:: bash

   export FAB_POOL=y
   make

.. _chroot: https://en.wikipedia.org/wiki/Chroot
.. _bootstrap: https://github.com/turnkeylinux/bootstrap
.. _buildroot: https://github.com/turnkeylinux/buildroot
.. _Pool: https://github.com/turnkeylinux/pool
