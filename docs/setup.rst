Overview
========

By the end of this setup guide you should be able to build a TurnKey
Core ISO from source. If you can do that, then you've setup TKLDev
correctly.

Of course you can build any TurnKey system from source code within
TKLDev, not just TurnKey Core. We recommend starting with TurnKey Core
because its the simplest TurnKey system.

We'll setup TKLDev and build TurnKey Core in 3 steps:

A. Deploy TKLDev
B. Setup the build dependencies
C. Clone Core from GitHub and run "make"

A. Deploy TKLDev
================

Like any other TurnKey system, TKLDev is available for `download`_ in
multiple build formats from the TurnKey Linux website. 

An even easier way to get an instance of TKLDev up and running is to
deploy it on the Amazon EC2 cloud using the `TurnKey Hub`_. Besides
being easy, developing your Linux distribution on Amazon EC2 has the
additional benefit of providing you with a network connection that is
much faster than the one you have locally, shortening download times for
packages and other components.

TKLDev doesn't support cross-architecture builds (yet). That means
building an amd64 type image requires an amd64 build of TKLDev. 

.. _TurnKey Hub: https://hub.turnkeylinux.org/
.. _download: http://www.turnkeylinux.org/tkldev/

B. Setup the build dependencies
===============================

In the next version of TKLDev, this step happens automatically the first
time TKLDev boots. 

If it doesn't (e.g., we didn't have a working Internet connection)
you'll be able to trigger it by running this command inside TKLDev as
root::

    tkldev-setup

But you're not using the next version of TKLDev (yet), so you'll want to
download the new tkldev-setup from GitHub::

    cd /usr/local/sbin
    wget https://raw.githubusercontent.com/turnkeylinux-apps/tkldev/master/overlay/usr/local/sbin/tkldev-setup
    chmod +x tkldev-setup

    ./tkldev-setup

The build dependencies: what are they?
--------------------------------------

1. **bootstrap** in ``/turnkey/fab/bootstraps``: contains minimal bootstrap filesystems.

2. **cdroots** in ``/turnkey/fab/cdroots``: contains the cdroot template for the built
   ISO.

3. **common** in ``/turnkey/fab/common``: contains source code shared amongst all
   TurnKey systems.

1. bootstrap
''''''''''''

Your Linux distribution's filesystem is first initialized as a copy of
``bootstrap``, which is an archived filesystem containing the bare
minimum essential operating system components required to run the
package manager and install additional packages.

Bootstraps are specific to a specific OS release and architecture. This
means there are 32-bit and 64-bit versions of bootstrap for each major
operating system release.

TurnKey's bootstrap is similar to the bootstrap filesystem created by
Debian's debootstrap tool, except it is slightly smaller and more
efficient. Other then that there is nothing TurnKey specific about it so
you can roll your own if you don't want to use the bootstrap tarballs
TurnKey provides for convenience.

Manual setup::

    ARCH=$(dpkg --print-architecture)
    CODENAME=$(lsb_release -s -c)
    SOURCEFORGE="http://downloads.sourceforge.net/project/turnkeylinux"

    cd /turnkey/fab/bootstraps
    wget $SOURCEFORGE/bootstrap/bootstrap-$CODENAME-$ARCH.tar.gz
    wget $SOURCEFORGE/bootstrap/bootstrap-$CODENAME-$ARCH.tar.gz.sig

    gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 0xA16EB94D
    gpg --verify bootstrap-$CODENAME-$ARCH.tar.gz.sig

    mkdir $CODENAME
    tar -zxf bootstrap-$CODENAME-$ARCH.tar.gz -C $CODENAME

2. cdroot
'''''''''

When an ISO is booted it displays a bootsplash prompting the user to
select whether to install to harddisk or run in live non-persistent
mode. The bootsplash configuration, files which facilitate the boot
process (initrd, kernel), and root filesystem are stored in the
``cdroot``.

Manual setup::

    cd /turnkey/fab
    git-clone https://github.com/turnkeylinux/cdroots.git

3. common
'''''''''

Each system has its own unique package plans, conf scripts and overlay,
but can also inherit from a common pool of configurations that live in
the "common" repository.

This prevents wasteful and ineffecient repetition of build instructions
that would otherwise have to be repeated for each system (I.e., AKA the
DRY - Don't repeat yourself - principle).

For example, all current TurnKey apps share the common ``TurnKey Core``
functionality, all LAMP stack based apps have a LAMP stack in common,
and so forth.

Manual setup::

    cd /turnkey/fab
    git-clone https://github.com/turnkeylinux/common.git

C. Clone Core from GitHub and run "make"
========================================

You're about to use TKLDev to build your first TurnKey Linux
distribution.

By convention, the source code for an appliance is placed within tkldev
in /turnkey/fab/products (e.g., /turnkey/fab/products/core,
/turnkey/fab/products/wordpress, etc.).

Clone the source code of `TurnKey Core`_ from GitHub::

    cd /turnkey/fab/products
    git-clone https://github.com/turnkeylinux-apps/core.git

Note that if you're behind a web proxy, then you need to set
``parentProxy`` in ``/etc/polipo/config`` and restart the ``polipo``
service.

Next, perform the build::

    cd core
    make

The above will create ``build/product.iso`` which you should copy to
your host system for testing in a VM.

.. _TurnKey Core: http://www.turnkeylinux.org/core/
