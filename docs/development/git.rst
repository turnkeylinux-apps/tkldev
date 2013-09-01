Recommended Git Flow and configuration
======================================

* Important: Read and follow the recommended `Git Flow and guidelines`_.

* We highly recommend you ``watch`` the `TKLDev`_ repository on GitHub,
  so you can track any changes made to the development documentation, as
  well as improvements to the appliance.

* Tell git who you are by editing ``~/.bashrc.d/git``::

    export GIT_AUTHOR_NAME="Your Name"
    export GIT_AUTHOR_EMAIL="your@email.com"
    export GIT_COMMITTER_NAME=$GIT_AUTHOR_NAME
    export GIT_COMMITTER_EMAIL=$GIT_AUTHOR_EMAIL

* And finally source that file as changes will only take effect at
  login::

    . ~/.bashrc.d/git 


.. _Git Flow and guidelines: https://github.com/turnkeylinux/tracker/blob/master/GITFLOW.rst
.. _TKLDev: https://github.com/turnkeylinux-apps/tkldev/

