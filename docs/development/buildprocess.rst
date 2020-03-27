Build process high-level overview
=================================

The last phase described in `Setup`_ built TurnKey Core::
    
    cd core
    make

This generated ``product.iso`` in the following 6 copy-on-write stages...

1. seed root filesystem from bootstrap
--------------------------------------

One of the first things that happens in the build process, is the
creation of a ``deck`` based on ``bootstrap``.

The ``bootstrap`` is the minimal root filesystem in which packages can
be installed. By default, TKLDev should contain a relevant bootstrap.
If not, one can be either downloaded from the `TurnKey mirror`_ or
generated via the `bootstrap buildcode`_.

A ``deck`` is a copy-on-write_ branch of a directory or another deck
created with the ``deck`` tool.

Decking a directory (or another deck) works like copying it to a new
location where you can apply arbitrary changes, except that it works
faster because there is no copying involved. See the `deck`_
documentation for full details.

After the ``bootstrap`` has been decked, a bootstrap specific apt overlay
and conf script are applied from the respective locations:

 - /turnkey/fab/common/overlays/apt_bootstrap/
 - /turnkey/fab/common/conf/apt_bootstrap

These provide apt related configurations required prior to building
``root.build``.

2. install plan into root.build
-------------------------------

``root.build`` is branched off from ``bootstrap`` and into it the plan
(by default ``plan/main``) is installed via the apt package manager.

A plan is a list of packages which may include references to other
plans containing additional packages, such as those in the ``common``
repository (e.g. /turnkey/fab/common/plans/turnkey/lamp).

3. apply overlay files, conf scripts & removelists to root.patched
------------------------------------------------------------------

``root.patched`` is branched off from ``root.build`` and into it
overlays and conf scripts are applied in the following order:

A) common ``overlays`` (i.e. those in /turnkey/fab/common/overlays/turnkey.d/).
B) common ``conf`` scripts (i.e. those in /turnkey/fab/common/overlays/turnkey.d/).
C) common ``removelists`` (i.e. /turnkey/fab/common/removelists/).
D) product specific ``overlay``.
E) product specific ``conf`` scripts.
F) product specific ``removelists``.
G) common ``removelists-final`` (i.e. /turnkey/fab/common/removelists-final/).

An ``overlay``: a directory containing files to be overlaid on top of
``root.patched``, relevative to /. For example youroverlay/etc/hostname will be
copied into root.patched/etc/hostname.

A ``conf`` script: any executable script in ``conf.d`` of the product
source code, or a specified script or directory in common.

The scripts are executed in alpha-numeric ordering based on the
filename, so if you need to control the order, you can prepend an
integer (e.g., conf.d/10myscript). This is used in complex products,
such as `GitLab`_.

Each script is copied into a temporary directory in ``root.patched`` and
executed while chrooted into ``root.patched``. After execution the
temporary directory is deleted.

A ``removelist`` (including ``removelists-final``) is file with a list of paths
to be removed from the filesystem. If the file(s) do not exist, a warning is
issued, but the build proceeds.

4. squash root.sandbox overlay - sandbox for manual prototyping
---------------------------------------------------------------

NOTE: Unfortunately as of v15.0, the ``root.sandbox`` no longer
      functions as intended. It is still created, but it is not mounted
      when booting the ISO. So it should not be used. This section remains
      as we hope to fix this functionality at some point in the future and
      this note will be removed.

``root.sandbox`` is branched off from the ``root.patched`` deck.

This step isn't strictly a necessary part of the build process. It only
really exists to make life easier for developers.

``root.sandbox`` is just like ``root.patched`` except it is designed to
hold temporary, manual modifications to the root filesystem. It serves
as a sandbox for quick & dirty protyping of changes. This accelerates
the development cycle by making it easy to test proposed changes to the
root filesystem quickly, without changing product source code and
without having to wait for the build process to resquash the
``root.patched`` root filesystem.

The way it works is that the build process squashes root.sandbox's overlay
separately. This only takes a few seconds. It then copies the archived
filesystem overlay into the cdroot, where it will be used to apply the
changes to the root filesystem during boot.

5. package the components into the cdroot template
--------------------------------------------------

Now that the root filesystem is ready, the final ``cdroot`` can be
created.

The cdroot is a directory which includes all the files required to make
the CD ISO image bootable. This includes the bootloader, bootsplash
configuration, kernel, initramfs, squashed ``root.patched`` filesystem
and the ``root.sandbox`` overlay if it exists.

6. generate product.iso
-----------------------

The final product.iso file is generated from the ``cdroot`` by the
genisoimage tool.

Extra note
----------

If you wish to build a "production ready" ISO which is named correctly and
a hash file also generated, you can use the ``bt-iso`` script from
`buildtasks`_. Note that ``bit-iso`` will name the ISO by the standard TKL
naming convention (we refer to this internally as "appver")::

    turnkey-_APPLIANCE-NAME_-VERSION-CODENAME_ARCH.iso

Where _APPLIANCE-NAME_-VERSION comes from the first line of changelog
(e.g. lamp-16.0), CODENAME is the Debian codename (unless set, comes from
the build host - e.g. buster) and ARCH is the architecture (comes from
the build host - e.g. amd64). The iso and the hash file will go into the
directory stored in the value of BT_ISOS (/mnt/isos by default).

.. _Setup: ../setup.rst
.. _TurnKey mirror: http://mirror.turnkeylinux.org/turnkeylinux/images/bootstrap/
.. _bootstrap buildcode: https://github.com/turnkeylinux/bootstrap
.. _copy-on-write: https://en.wikipedia.org/wiki/Copy-on-write
.. _deck: https://github.com/turnkeylinux/deck
.. _GitLab: https://github.com/turnkeylinux-apps/gitlab/tree/master/conf.d/
.. _buildtasks: https://github.com/turnkeylinux/buildtasks
