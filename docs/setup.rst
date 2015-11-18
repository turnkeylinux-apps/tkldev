Overview
========

By the end of this setup guide you should be able to build a TurnKey
Core ISO from source. If you can do that, then you've setup TKLDev
correctly.

Of course you can build any TurnKey system from source code within
TKLDev, not just TurnKey Core. We recommend starting with TurnKey Core
because it's a simple example.

We'll setup TKLDev and build TurnKey Core in 3 steps:

A. Deploy TKLDev
B. Setup the build dependencies automatically or by hand
C. Clone Core from GitHub and run "make"

A. Deploy TKLDev
================

Like any other TurnKey system, TKLDev is available for `download`_ in
multiple build formats from the TurnKey Linux website. To deploy TKLDev,
download the ISO and prepare a new VM (for example with Virtualbox). Mount
the downloaded ISO file as boot-cd and start it.

An even easier way to get an instance of TKLDev up and running is to
deploy it on the Amazon EC2 cloud using the `TurnKey Hub`_. Besides
being easy, developing your Linux distribution on Amazon EC2 has the
additional benefit of providing you with a network connection that is
much faster than the one you have locally, shortening download times for
packages and other components.

TKLDev doesn't support cross-architecture builds (yet). That means
building an amd64 type image requires an amd64 build of TKLDev. 

.. _TurnKey Hub: https://hub.turnkeylinux.org/
.. _download: https://www.turnkeylinux.org/tkldev/

B. Setup the build dependencies
===============================

Officially, TKLDev will be setup automatically on first boot.

If it doesn't (e.g., we didn't have a working Internet connection)
you'll be able to trigger it by running this command inside TKLDev as
root:

    tkldev-setup
    
This will checkout the build dependencies.

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

Bootstraps are specific to a specific OS release and architecture.

TurnKey's bootstrap is similar to the bootstrap filesystem created by
Debian's debootstrap tool, except it is slightly smaller and more
efficient. Other then that there is nothing TurnKey specific about it so
you can roll your own (e.g., with Debian's debootstrap) if you prefer
not to use the bootstrap tarballs TurnKey provides for convenience.

Manual setup::

    ARCH=$(dpkg --print-architecture)
    CODENAME=$(lsb_release -s -c)
    IMAGES="http://mirror.turnkeylinux.org/turnkeylinux/images"

    cd /turnkey/fab/bootstraps
    wget $IMAGES/bootstrap/bootstrap-$CODENAME-$ARCH.tar.gz
    wget $IMAGES/bootstrap/bootstrap-$CODENAME-$ARCH.tar.gz.sig

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

By convention, the source code for TurnKey integrations is placed within
tkldev in /turnkey/fab/products (e.g., /turnkey/fab/products/core,
/turnkey/fab/products/wordpress, etc.).

At first boot, the `TurnKey Core`_ should have been checked out by ``tkldev-setup``
into ``/turnkey/fab/products/core``. 

If you want to be sure if it did, you can use the following commands::

    cd /turnkey/fab/products
    ! [ -d core ] && git-clone https://github.com/turnkeylinux-apps/core.git

Note that if you're behind a web proxy, then you need to set
``parentProxy`` in ``/etc/polipo/config`` and restart the ``polipo``
service.

Next, perform the build::

    cd core
    make

The build should take about 3-5 minutes.

The above will create ``build/product.iso`` which you can image to a USB
drive, burn on a CD or copy to your host system for testing in a VM.

Congratulations on your first build!

What next?
==========

* `Hello world`_: say hello by making your first change.

.. _Hello world: helloworld.rst
.. _TurnKey Core: https://www.turnkeylinux.org/core/
