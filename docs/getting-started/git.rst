Git Configuration and Workflow
==============================

* Important: Read the recommended `Git Flow and guidelines`_. It will give you
  an overview of how TurnKey Linux uses Git and GitHub.

* We recommend you ``watch`` the `TKLDev`_ repository on GitHub.
  It makes it easy to follow changes to the documentation, and TKLDev itself.
  
* In TKLDev, tell git who you are by editing ``~/.bashrc.d/git``::

    export GIT_AUTHOR_NAME="Your Name"
    export GIT_AUTHOR_EMAIL="your@email.com"
    export GIT_COMMITTER_NAME=$GIT_AUTHOR_NAME
    export GIT_COMMITTER_EMAIL=$GIT_AUTHOR_EMAIL

  Then relogin to TKLDev or source the file into the current shell::
  
    . ~/.bashrc.d/git 

.. _Git Flow and guidelines: https://github.com/turnkeylinux/tracker/blob/master/GITFLOW.rst
.. _TKLDev: https://github.com/turnkeylinux-apps/tkldev/

