Build process high-level overview
=================================

The last phase described in `Setup`_ built TurnKey Core::
    
    cd core
    make

This generated ``product.iso`` in roughly 6 stages:

1. seed root filesystem from bootstrap
--------------------------------------

One of the first things that happens in the build process, is the
creation of a ``deck`` based on ``bootstrap``.

The ``bootstrap`` is the minimal root filesystem in which packages can
be installed.

A ``deck`` is a copy-on-write branch of a directory or another deck
created with the ``deck`` tool.

Decking a directory (or another deck) works like copying it to a new
location where you can apply arbitrary changes, except that it works
faster because there is no copying involved. See the `deck`_
documentation for full details.

2. install plan into root.build
-------------------------------

``root.build`` is branched off from ``bootstrap`` and into it the plan
is installed via the package manager.

The plan is a list of packages which may include references to other
plans containing additional packages, such as those in the ``common``
repository (e.g. /turnkey/fab/common/plans/turnkey/lamp).

3. apply conf scripts and overlay files to root.patched
-------------------------------------------------------

``root.patched`` is branched off from ``root.build`` and on to it
overlays and conf scripts are applied in the following order:

A) common ``overlays`` and ``conf`` scripts.
B) product specific ``overlays`` and ``conf`` scripts.

An ``overlay``: a directory containing files to be overlaid on top of
``root.patched``. For example youroverlay/etc/hostname will be copied
into root.patched/etc/hostname.

A ``conf`` script: any executable script in ``conf.d`` of the product
source code, or a specified script or directory in common.

The scripts are executed in alpha-numeric ordering based on the
filename, so if you need to control the order, you can prepend an
integer (e.g., conf.d/10myscript). This is used in complex products,
such as `GitLab`_.

Each script is copied into a temporary directory in ``root.patched`` and
executed while chrooted into ``root.patched``. After execution the
temporary directory is deleted.

4. squash root.tmp overlay - sandbox for manual changes
-------------------------------------------------------

``root.tmp`` is branched off from the ``root.patched`` deck.

This step isn't strictly a necessary part of the build process. It only
really exists to make life easier for the appliance developer.

``root.tmp`` is just like ``root.patched`` except it is designed to hold
temporary, manual modifications to the root filesystem. It serves as a
sandbox that can be used to accelerate the development cycle by making
it easy to test proposed changes to the root filesystem quickly, without
changing product source code and without having to wait for the build
process to resquash the ``root.patched`` root filesystem.

The way it works is that the build process squashes root.tmp's overlay
separately. This only takes a few seconds. It then copies the archived
filesystem overlay into the cdroot, where it will be used to apply the
changes to the root filesystem during boot.

5. package the components into the cdroot template
--------------------------------------------------

Now that the root filesystem is ready, the final ``cdroot`` can be
created.

The cdroot is a directory which includes all the files required to make
the appliance's CD ISO image bootable including the bootloader,
bootsplash configuration, kernel, initramfs, squashed ``root.patched``
filesystem and the ``root.tmp`` overlay if it exists.

6. generate product.iso
-----------------------

The final product.iso file is generated from the ``cdroot`` by the
genisoimage tool.

.. _Setup: ../setup.rst
.. _deck: https://github.com/turnkeylinux/deck
.. _GitLab: https://github.com/turnkeylinux-apps/gitlab/tree/master/conf.d/

