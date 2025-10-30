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

A buildroot is a minimalist Debian chroot_ which provides an environment
specifically for building packages. TurnKey uses our bootstrap_ as a
base, then preinstalls some extra build related packages/tools.

It is highly recommended that you `generate a buildroot`_ using our
tool. Do that like this:

.. code-block:: bash

   cd /turnkey
   git clone https://github.com/turnkeylinux/buildroot.git
   cd buildroot
   make install

Always run `make clean` if you rebuild the buildroot.

Note that using a pre-built buildroot will speed up package building,
although strictly speaking is not required. A vanilla bootstrap may
be used, as the dependencies noted in the `Build-Depends`_ section of
the pacakge control file will be installed into the buildroot prior
to building the package.

Pool configuration
------------------

Pool_ is the custom TurnKey tool for building packages. With the exception
of a buildroot, TKLDev should have (most of) pool configured out of the box.

All you need to do is build the buildroot as linked above and you are ready
to go.

Build a package with pool
-------------------------

I'll use TurnKey's "inithooks" package as an example:

First, clone or copy your source code to an appropriate location. We use
/turnkey/public, but it can be any directory you like:

.. code-block:: bash

    mkdir -p /turnkey/public
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


Package versioning
------------------

By default, a Debian package will generate it's version from the heading of
the debian/changelog. That's fine when building "stable" packages. However,
when hacking on a package it can be useful to preserve each package iteration
as you make changes. By default, that requires manual update to the changelog
version for each rebuild - and remembering to do it.

To help out, our default buildroot includes our custom `autoversion`_ tool.
As the name suggests, it can generate a unique version for you; each time you
rebuild a package.

The requiremens for autoversion to generate a custom version are:
- package source code must be in a git repo
- changes must be committed
- the must not be a changelog in the source debian directory

If your package does already have a changelog, then move/remove it until you
are ready for a new "stable" release.

The generated versions are nicest if your code has at least one annotated tag.
See the `tags`_ section of the `Git Pro`_ online book for details about
annotated tags. For example if package "foo" has the git HEAD tagged 'v0.1',
autoversion will generate version '0.1'. I.e. 'foo_0.1_all.deb'.

Further commits generate versions noting how many commits since the tag and
the commit ID of HEAD. The new version string will be
'<version_tag>+<commits_since_tag>+g<commit_id>'. E.g. if foo has 2 commits
since the 'v0.1' tag and the HEAD commit ID is "59286ad", the new version will
be "0.1+1+g59286ad" - i.e. 'foo_0.1+1+g59286ad_all.deb'.

It still works if there are no tags, but the versions are a bit ugly. They are
in the form of '0+<YYYY>.<MM>.<DD>+<HH>.<MM>.<SS>+<commit_id>'. E.g.:
'foo_0+2025.2.19+06.45.45+a42fea97_all.deb'.

The versions will sort properly, so it's no issue to push them to an apt
package repo as is, but ideally you want to have a "nice" version number for a
stable pacakge. So either give it a new version tag - add/replace the
changelog.

.. _chroot: https://en.wikipedia.org/wiki/Chroot
.. _bootstrap: https://github.com/turnkeylinux/bootstrap
.. _generate a buildroot: https://github.com/turnkeylinux/buildroot?tab=readme-ov-file#build
.. _Build-Depends: https://github.com/turnkeylinux/inithooks/blob/master/debian/control#L5-L8
.. _Pool: https://github.com/turnkeylinux/pool
.. _autoversion: https://github.com/turnkeylinux/autoversion?tab=readme-ov-file#map-git-commits-to-auto-versions-and-vice-versa
.. _tags: https://git-scm.com/book/en/v2/Git-Basics-Tagging
.. _Git Pro: https://git-scm.com/book/en/v2
