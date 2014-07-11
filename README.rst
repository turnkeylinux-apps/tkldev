TKLDev - TurnKey Development Toolchain and Build System
=======================================================

TKLDev is the mother of all TurnKey apps. It's used to give birth to all
TurnKey apps, including new versions of `itself`_. It's designed to make
simple things simple, and hard things possible. It's a self-contained
build system that can be used to rapidly prototype and repeatably build
any generic Debian-based Linux distribution or TurnKey GNU/Linux system
`from source`_.

Read the `blog post`_ announcing TKLDev for the background story. Read
the `documentation`_ for installation and usage instructions.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- Includes rapid copy-on-write TurnKey build toolchain including:
  `fab`_, `deck`_ and a simple Makefile based system that allows rapid
  prototyping of new turn-key system integrations quickly and easily.
- Turnkey development directory structure with preconfigured CDPATH.
- Integrated caching proxy for fast and iterative development.
- Full usage and development `documentation`_.

Example build sources
---------------------

- `TurnKey GNU/Linux apps <https://github.com/turnkeylinux-apps>`_
- `Community developed distributions <https://github.com/turnkeylinux/tracker/issues?labels=new-appliance>`_

Credentials *(passwords set at first boot)*
-------------------------------------------

-  SSH: username **root**

.. _itself: https://github.com/turnkeylinux-apps/tkldev
.. _blog post: http://www.turnkeylinux.org/blog/introducing-tkldev
.. _fab: https://github.com/turnkeylinux/fab
.. _deck: https://github.com/turnkeylinux/deck
.. _from source: https://github.com/turnkeylinux-apps/
.. _TurnKey Core: http://www.turnkeylinux.org/core
.. _documentation: https://github.com/turnkeylinux-apps/tkldev/tree/master/docs
