Improving and maintaining an appliance
======================================

Lets say you find a bug in an appliance, want to add more functionality,
upgrade the version of upstream software, or make any other change, then
this guide should help you do that and get your changes included in the
official TurnKey appliance and earn some street cred.

For example, say a new version of ``projectpier`` has been released, so
lets update `TurnKey ProjectPier`_.

Fork and clone the source
-------------------------

As described in the TurnKey `Git Flow`_, GitHub is used to facilitate
collaboration, so the first thing to do is fork the appliance source
code:

* Log into GitHub, and browse to https://github.com/turnkeylinux-apps/projectpier/
* Click the ``fork`` button.

That's it. You've successfully forked the ``projectpier`` repository,
but so far it only exists on GitHub.

To be able to work on the project you'll need to clone it::

    cd /turnkey/fab/products
    git-clone git@github.com:USERNAME/projectpier.git

So far so good. When a repository is cloned, it has a default ``remote``
called ``origin`` that points to your fork on GitHub, not the original
repository it was forked from.

To keep track of the original repository, you need to add another
remote, we'll call it ``upstream``::

    cd projectpier
    git remote add upstream https://github.com/turnkeylinux-apps/projectpier.git

    # Fetch any new changes to the original repository
    git-fetch upstream

    # Merge any changes fetched into your working branch
    git merge upstream/master

Make your changes
-----------------

OK, so now we're almost ready to make our changes. As described above,
we are updating the version of projectpier.

Create a branch
'''''''''''''''

The first thing to do is create a branch for the update. Note that you
have only one ``pull request`` per branch::

    git-checkout -b upgrade-to-vXX.YY

Perform change
''''''''''''''

So now we are ready to make our changes. It's recommended to read the
release notes of new versions to see if there are any other changes that
might need to be made. For arguments sake, lets say there aren't.

We get the new versions download URL as well as the md5sum, and update
``conf.d/downloads``.

Test
''''

And we're done, not so hard. Lets perform a build for testing, but
instead of building the ISO, we'll take a quick shortcut and specify
``CHROOT_ONLY=y``. This excludes boot-related packages and stops the
build at the ``root.tmp`` stage::

    make CHROOT_ONLY=y

If there were any issues during the build, we'll need to fix them, and
run ``make CHROOT_ONLY=y`` again. Note that the build will pick up from
where it left off, and re-make the target that caused the issue.

Once the ``CHROOT_ONLY`` build is successful, lets test it::

    fab-chroot build/root.tmp
    /etc/init.d/mysql start
    /etc/init.d/apache2 start
    /usr/lib/inithooks/firstboot.d/20regen-projectpier-secrets

    # on host system, browse to http://ip-of-tkldev-vm
    # verify there are no issues

    /etc/init.d/apache2 stop
    /etc/init.d/mysql stop
    exit

Testing complete? Let's perform a cleanup::

    deck -D build/root.tmp
    make clean

Cautionary note: not all changes can be tested reliably (or at all)
inside chroot using the CHROOT_ONLY shortcut. For large changes or
changes that may effect the boot process (e.g., inithooks) it is
recommended not to use CHROOT_ONLY. Instead, perform a full build and
test the ISO in a VM.

Commit
''''''

Now we commit our example change to the repository::

    $ git-status
    # On branch upgrade-to-vXX.YY
    # Changed but not updated:
    #   (use "git add <file>..." to update what will be committed)
    #   (use "git checkout -- <file>..." to discard changes in working directory)
    #
    #	modified:   conf.d/downloads
    #
    no changes added to commit (use "git add" and/or "git commit -a")

    $ git-add conf.d/downloads
    $ git-commit -m "Upgraded projectpier to version XX.YY"

Push changes to GitHub and submit a Pull Request
------------------------------------------------

Now that you're finished hacking and all changes are committed, you need
to push them to your GitHub repository::

    git-push origin upgrade-to-vXX.YY

Last thing to do is send a ``pull request`` so the maintainer or one of
the core developers can review, sign off, and perform the merge in the
official repository.

* Browse to https://github.com/USERNAME/projectpier/tree/upgrade-to-vXX.YY
* Click ``Pull Request``, describe the change and click ``Send pull request``.

Hooray! You did it.

If for some reason the maintainer or one of the core developers has a
problem with your change, they won't want to merge until fixed.

The good news is that whenever you commit and push more changes to that
branch of your code, they will be included in that original pull request
until it is closed.

.. _TurnKey ProjectPier: https://github.com/turnkeylinux-apps/projectpier/
.. _Git Flow: https://github.com/turnkeylinux/tracker/blob/master/GITFLOW.rst

