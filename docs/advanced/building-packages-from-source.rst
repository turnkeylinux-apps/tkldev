Building Packages from Source
=============================

As of v14.2, TKLDev includes all the components needed to build packages from
souce code on the fly. This may be useful if you wish to test a piece of
software which is unpackaged, but you want it packaged. It can also be useful
if you wish to tweak an existing TurnKey package.

Please note that within these instructions, I make use of variables. If you
follow this from start to finish in a single shell, then you won't have any
issues. Please note though, that if you use multiple shells, or do it over
multiple sessions, then you'll either need to redefine the variables, or
substitue the real path/value.


Building packages - getting set up
----------------------------------

Before you can build packages, you'll need a buildroot to build them in. A
buildroot is essentially a minimalist Debian chroot_. TurnKey may provide one
for download at some point. But for now, you'll need to build it yourself.


Chanko - initial setup
----------------------

Chanko_ is a tool to download and cache Debian packages and is a prerequisite
for building our buildroot.

Initially, you will need to ensure that Chanko is fully configured and has
been pre-loaded with the packages required for the buildroot. If you haven't
already done it, please set up Chanko:

.. code-block:: bash

	tkldev-chanko-setup

Note: this script may not yet be included in TKLDev, you may  need to download
and prepare the script first:

.. code-block:: bash

    GH_URL=https://raw.githubusercontent.com/turnkeylinux-apps/tkldev/master/overlay
    SCRIPT=usr/local/bin/tkldev-chanko-setup
    wget -o /$SCRIPT $GH_URL/$SCRIPT
    chmod +x /$SCRIPT


Loading Chanko
--------------

To load Chanko with the required packages, you'll need to create some plans
which will note the required packages Chanko will need to download.

If you haven't already, please clone the buildroot source code:

.. code-block:: bash

    cd /turnkey
    git clone https://github.com/turnkeylinux/buildroot.git

Now to gather the plans for Chanko:

.. code-block:: bash

    CODENAME=$(lsb_release -cs)
    CHANKO=/turnkey/fab/chankos/${CODENAME}.chanko

    wget -O ${CHANKO}/plan/bootstrap-required \
        https://raw.githubusercontent.com/turnkeylinux/bootstrap/master/plan/required
    wget -O ${CHANKO}/plan/bootstrap-base \
        https://raw.githubusercontent.com/turnkeylinux/bootstrap/master/plan/base
    echo "/* buildroot */" >> ${CHANKO}/plan/buildroot
    cat /turnkey/buildroot/plan/main >> ${CHANKO}/plan/buildroot
    # extra TurnKey packages for buildroot:
    cat >> ${CHANKO}/plan/buildroot <<EOF
    turnkey-pylib
    pyproject-common
    autoversion
    EOF # note the 'EOF' must be at the start of a line

Then download the packages like this:

.. code-block:: bash

    cd ${CHANKO}
    chanko refresh -a
    echo y | chanko-get plan/bootstrap-base
    echo y | chanko-get plan/bootstrap-required
    echo y | chanko-get plan/buildroot

That will take a little while to do it's work, but hopefully not too long.


Build the buildroot
-------------------

Once you've configured Chanko, it's really easy! You just need to do this:

.. code-block:: bash

    CODENAME=$(lsb_release -cs)

    cd /turnkey/buildroot
    export FAB_POOL=y
    export RELEASE=debian/$CODENAME
    make


Put the buildroot in place
--------------------------

Once that has finished, you just need to move your buildroot to where Pool is
expecting it to be:

.. code-block:: bash

    CODENAME=$(lsb_release -cs)
    BUILDROOT=${FAB_PATH}/buildroots/${CODENAME}
    mkdir -p ${BUILDROOT}

    rsync --progress --delete -Hac build/root.patched/ ${BUILDROOT}

Once that's done, you can recover a bit of space by cleaning up:

.. code-block:: bash

    make clean

Initialize Pool
---------------

The last step is to initialize Pool_.

.. code-block:: bash

    cd pools/
    mkdir -p ${CODENAME}
    cd ${CODENAME}
    pool-init ${FAB_PATH}/buildroots/${CODENAME}

    # bugfix
    mkdir -p /turnkey/fab/deckdebuilds/chroots/

Now we should be nearly ready to build!


Build a package from source
---------------------------

Now it's time to build a package! For this test I'm going to build TurnKey's
inithooks package. So let's clone the source code first:

.. code-block:: bash

    mkdir /turnkey/public
    cd /turnkey/public
    git clone https://github.com/turnkeylinux/inithooks.git

Now we'll register this source code with Pool and build the package:

.. code-block:: bash

    cd pools/${CODENAME}

    pool-register /turnkey/public/inithooks
    pool-get . inithooks

And after a few moments, you should find the ccurl Debian package ready for use:

.. code-block:: bash

    root@tkldev pools/stretch# ls
    inithooks_0.9+270+g179b423_all.deb

You can now move this .deb to where you wish to use it and install with dpkg. 
Alternatively, if you are building an appliance you can automatically include
this package by adding the packagename to the plan and building with 
`export FAB_POOL=y`.

.. _chroot: https://en.wikipedia.org/wiki/Chroot
.. _Chanko: https://github.com/turnkeylinux/chanko
.. _Pool: https://github.com/turnkeylinux/pool
