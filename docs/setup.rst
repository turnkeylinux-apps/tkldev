Download requirements
=====================

layout overview
---------------

Before getting started, it's useful to understand the file-system layout
of TKLDev, the most relevant for now is the ``/turnkey`` root folder::

    /turnkey/
        bootstraps/
        cdroots/
        common/
        products/
            core/
            wordpress/
            ...

Note that absolute paths are used in the documentation, even though
``CDPATH`` is pre-configured and supports tab completion, providing
quick and easy navigation, for example::

    cd core             # changes to /turnkey/products/core
    cd products/core    # changes to /turnkey/products/core
    cd common           # changed to /turnkey/common

bootstrap
---------

All appliances (ie. products) are built by layering on top of a
bootstrap. Bootstraps are release and architecture specific, so here we
download the bootstrap suitable for the TKLDev deployment, verify it,
and proceed to unpack it::

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

cdroots
-------

Without going into too much detail, when an ISO is booted it displays a
bootsplash prompting the user to select whether to install to harddisk
or run in live non-persistent mode. The bootsplash configuration, files
which facilitate the boot process (initrd, kernel), and root filesystem
are stored in the ``cdroot``::

    cd /turnkey/fab
    git-clone https://github.com/turnkeylinux/cdroots.git

common
------

Again, without going into too much detail, each appliance (usually) has
a product specific plan, conf scripts and overlay. Common provides the
common code and configuration files used by multiple appliances adhering
to the DRY (Don't repeat yourself) principle::

    cd /turnkey/fab
    git-clone https://github.com/turnkeylinux/common.git

Building your first appliance (TurnKey Core)
============================================

Now that everything is in place, clone the source code of `TurnKey
Core`_ - The common base for all appliances, and perform the build::

    cd /turnkey/fab/products
    git-clone https://github.com/turnkeylinux-apps/core.git
    cd core
    make

The above will create ``build/product.iso`` which you should copy to
your host system for testing in a VM.

Finally, perform cleanup::

    deck -D build/root.tmp
    make clean


.. _TurnKey Core: http://www.turnkeylinux.org/core/

