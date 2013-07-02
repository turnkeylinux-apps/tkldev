Build process high-level overview
=================================

You should recall that the last phase of `Setup`_ was to build TurnKey
Core using the command ``make``, which generated ``product.iso``. Let's
describe what actually happened and introduce some terminology.

bootstrap
---------

One of the first things that happen in the build process, is the
creation of a ``deck`` based on ``bootstrap``.

* A ``deck`` is a virtual filesystem branch derived from a directory or
  another deck.

* The ``bootstrap`` was already introduced in `Setup`_, which is
  basically the minimal root filesystem in which packages can be
  installed.

root.build
----------

Next, a new ``deck`` called ``root.build`` is created from the bootstrap
deck.

* The ``root.build`` is the chroot'able root filesystem of the product,
  built by installing the resolved packages from the ``plan``.

* A ``plan`` defines a set of packages to be installed in the product,
  which may include other plans, such as those in ``common``.

* ``common``, also introduced in `Setup`_, includes common plans,
  overlays, conf scripts and more adhering to the DRY principle.

root.patched
------------

The ``root.patched`` deck is then created from the root.build deck.

* The ``root.patched`` is the chroot'able root filesystem of the
  product, built by applying common ``overlays`` and ``confs``, and
  finally the product specific ``overlays`` and ``confs``.

* An ``overlay`` is a directory containing files to be overlayed in
  ``root.patched``.

* A ``conf`` is any executable script in ``conf.d`` of the product
  source code, or a specified script or directory in common.

  The scripts are executed in alpha-numeric ordering based on the
  filename, so if you have to control the order, you can prepend an
  integer (e.g., conf.d/10myscript). This is used in complex products,
  such as `GitLab`_.

  Each script is copied into a temporary directory in ``root.patched``
  and executed while chrooted into ``root.patched``. After execution the
  temporary directory is deleted.

root.tmp
--------

Next, a new ``deck`` called ``root.tmp`` is created from the
root.patched deck.

* The ``root.tmp`` is a chroot'able root filesystem of the product, used
  as a sandbox to accelerate the development cycle by providing a
  mechanism for testing manual changes to the root filesystem.

  Instead of re- ``squashing`` the root filesystem from scratch, root.tmp's
  overlay is squashed separetly - ie. rebuilding a product to test a
  change to the root filesystem only takes a few seconds.

cdroot
------

Now that the root filesystem is ready, the ``cdroot`` (introduced in
`Setup`_) is created, including the initrd, kernel, ``squashed`` root
filesystem, the bootsplash and a few other files to facilite the boot
process.

product.iso
-----------

The final product used by the end-user. The product is generated from
the prepared ``cdroot``.


.. _Setup: ../setup.rst
.. _GitLab: https://github.com/turnkeylinux-apps/gitlab/tree/master/conf.d/

