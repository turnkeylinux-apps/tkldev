Appliance buildcode directory overview
======================================

A quick overview of the contents of an appliance git repository.

Notes/key
---------

Notes are provided on a new line below and preceeded by an asterisk. E.g.::

   * some notes...

Optional files/directories  are surrounded by square brackets. E.g.::

   [some-optional-file-or-dir]

Multiple files and directories that are not explictly noted (i.e.
optional) are denoted by elipses within square brackets. I.e.::

   [...]

Example directory
-----------------

::

   .
   |-- .art
   |   * artwork related to the appliance; a logo and screenshots
   |   |-- logo.png
   |   |-- screenshot_1.png
   |   `-- [...]
   |-- .git
   |   * revision control information - please ignore this dir
   |   `-- [...]
   |-- .gitignore
   |   * files to be ignored by git listed in here
   |-- Makefile
   |   * set env vars for build, include relevant common mk files
   |-- README.rst
   |   * appliance overview and notes; is converted to the appliance website page
   |-- changelog
   |   * note changes since last release of this appliance
   |-- conf.d
   |   * configuration scripts - these are run within build/root.patched
   |   |-- [downloads]
   |   `-- main
   |-- [docs]
   |   * docs related to this appliance, not included within the appliance
   |   `-- [...]
   |-- overlay
   |   * files to be copied over the root filesystem - applied to build/root.patched
   |   |-- [etc]
   |   |   |-- [confconsole]
   |   |   |   `-- services.txt
   |   |   |       * appliance specific services to be noted in confconsole
   |   |   `-- [...]
   |   |       * other config overlays for /etc/[...]
   |   |-- [root]
   |   |   `-- [...]
   |   |   * overlays for root home dir
   |   |-- [usr]
   |   |   * overlays for /usr
   |   |   |-- [...]
   |   |   `-- [local]
   |   |       |-- [bin]
   |   |       |   `-- [...]
   |   |       |       * appliance specific custom scripts
   |   |       `-- [src]
   |   |           `-- [...]
   |   |               * appliance specfic source files - often (re)moved within conf scripts
   |   |-- [var]
   |   |   `-- [www]
   |   |       |-- [...]
   |   |       `-- index.html
   |   |           * webroot overlays - where appropriate
   |   `-- [...]
   |       * other overlaid files/dirs
   |-- [patches.d]
   |   `-- [...]
   |       * patches to be applied at build time - applied to build/root.patched
   `-- plan
       `-- main
           * Debian or TurnKey apt packages to install - installed to build/root.build
