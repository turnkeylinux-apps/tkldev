Importing a new app into turnkeylinux-apps
==========================================

Below we describe the current process used to import a `new`_ app into
turnkeylinux-apps. The idea is to facilitate easy collaboration with the
original integration developer/maintainer.

Fork
----

* Fork repository into turnkeylinux-apps.
* Update title and website.
* Change repository name (if required).
* Disable unneeded GitHub repo features (wiki, issues, etc.)

Clone
-----

::

    git-clone git@github.com:turnkeylinux-apps/APPLIANCE.git
    git-remote rename origin github

Review and test
---------------

* Review source code is compliant with `requirements`_.
* During review, note any issues that need fixing.
* Perform a test build

Optional: Bugfix, tweak, refactor
---------------------------------

The main branch will be ``master``, but to facilitate collaboration with
the upstream developer/maintainer, adhere to the `Git Flow`_ for pull
requests::

    git-checkout -b initial-tweaks
    # hack, test, commit...

    git-checkout master
    git-merge initial-tweaks

    git-push github
    git-push github initial-tweaks
    # send pull request on github

.. _new: ../development/new-app.rst
.. _requirements: ../development/new-app.rst
.. _Git Flow: https://github.com/turnkeylinux/tracker/blob/master/GITFLOW.rst

