Importing a new appliance into turnkeylinux-apps
================================================

Below describes the process used by the core devs to import a `new`_
appliance into turnkeylinux-apps, and faciliate collaboration with the
upstream developer/maintainer.

Fork
----

* Fork appliance into turnkeylinux-apps.
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

The main branch will be ``master``, but to faciliate collaboration with
the upstream developer/maintainer, adhere to the `Git Flow`_ for pull
requests::

    git-checkout -b initial-tweaks
    # hack, test, commit...

    git-checkout master
    git-merge initial-tweaks

    git-push github
    git-push github initial-tweaks
    # send pull request on github


.. _new: new.rst
.. _requirements: new.rst#requirements
.. _Git Flow: https://github.com/turnkeylinux/tracker/blob/master/GITFLOW.rst

