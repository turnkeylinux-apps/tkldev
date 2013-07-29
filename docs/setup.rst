CDPATH
======

While absolute paths are used in the documentation, the ``CDPATH``
environment variable is pre-configured to provide quick and easy
navigation through the filesystem::

    cd core             # changes to /turnkey/fab/products/core
    cd products/core    # changes to /turnkey/fab/products/core
    cd common           # changes to /turnkey/fab/common

Note that CDPATH supports tab auto-completion.

Prerequisites
=============

By convention, the source code for an appliance is placed within tkldev
in /turnkey/fab/products (e.g., /turnkey/fab/products/core,
/turnkey/fab/products/wordpress, etc.).

Though you can build any TurnKey appliance from source code within
TKLDev, we recommend first trying to build TurnKey Core as it is the
simplest and easiest to understand of all TurnKey appliances.

But before you build your first appliance, you will need to download 3
prerequisite build dependencies and place them into their appropriate
paths within the TKLDev filesystem:

1. ``/turnkey/fab/bootstraps``: contains minimal bootstrap filesystems.
2. ``/turnkey/fab/cdroots``: contains the cdroot template for the built
   ISO.
3. ``/turnkey/fab/common``: contains source code shared amongst all
   TurnKey appliances.

1. bootstrap
------------

An appliance filesystem is first initialized as a copy of ``bootstrap``,
which is an archived filesystem containing the bare minimum essential
operating system components required to run the package manager and
install additional packages.

Bootstraps are specific to a specific OS release and architecture. This
means there are 32-bit and 64-bit versions of bootstrap for each major
operating system release.

TurnKey's bootstrap is similar to the bootstrap filesystem created by
Debian's debootstrap tool, except it is slightly smaller and more
efficient. Other then that there is nothing TurnKey specific about it so
you can roll your own if you don't want to use the bootstrap tarballs
TurnKey provides for convenience.

The easiest way to get started is to download a suitable bootstrap
archive for your version of TKLDev, verify it, and proceed to unpack it
to /turnkey/fab/bootstraps::

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
---------

When an ISO is booted it displays a bootsplash prompting the user to
select whether to install to harddisk or run in live non-persistent
mode. The bootsplash configuration, files which facilitate the boot
process (initrd, kernel), and root filesystem are stored in the
``cdroot``::

    cd /turnkey/fab
    git-clone https://github.com/turnkeylinux/cdroots.git

3. common
---------

While each TurnKey appliance has a product specific plan, conf scripts
and overlay it also shares a common base of functionality with other
appliances.

For example, all appliances share the common ``TurnKey Core``
functionality, all LAMP stack based appliances have a LAMP stack in
common, and so forth.

The common repository provides the common code and configuration files
used by multiple appliances. This prevents wasteful and ineffecient
repetition of build instructions that would otherwise have to be
repeated for each appliance, in accordance with the DRY (Don't repeat
yourself) principle::

    cd /turnkey/fab
    git-clone https://github.com/turnkeylinux/common.git

Building your first appliance (TurnKey Core)
============================================

Now that everything is in place, clone the source code of `TurnKey
Core`_ - The common base for all appliances::

    cd /turnkey/fab/products
    git-clone https://github.com/turnkeylinux-apps/core.git

If you're behind a web proxy, then you'll need to set the ``parentProxy``
in ``/etc/polipo/config`` and restart the ``polipo`` service.

Finally, perform the build::

    cd core
    make

The above will create ``build/product.iso`` which you should copy to
your host system for testing in a VM.

Finally, perform cleanup::

    deck -D build/root.tmp
    make clean

.. _TurnKey Core: http://www.turnkeylinux.org/core/

