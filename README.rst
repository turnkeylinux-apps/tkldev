TKLDev - TurnKey Development Toolchain and Build System
=======================================================

TKLDev is the mother of all TurnKey apps. It's used to give birth to all
TurnKey apps, including new versions of `itself`_. It's designed to make
simple things simple, and hard things possible. It's a self-contained
build system that can be used to rapidly prototype and repeatably build
any generic Debian-based Linux distribution or TurnKey GNU/Linux system
`from source`_.

To get started read the `documentation`_. Read the `blog post`_
announcing TKLDev for the background story. 

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- Includes a fast copy-on-write build toolchain based on 
  GNU make, `fab`_, and `deck`_.
- Turnkey development directory structure with preconfigured CDPATH.
- Integrated caching proxy (squid) for fast and iterative development.
- Full usage and development `documentation`_.

Example build sources
---------------------

- `TurnKey GNU/Linux apps <https://github.com/turnkeylinux-apps>`_
- `Community developed distributions <https://github.com/turnkeylinux/tracker/issues?labels=new-appliance>`_

Credentials *(passwords set at first boot)*
-------------------------------------------

-  SSH: username **root**

.. _itself: https://github.com/turnkeylinux-apps/tkldev
.. _blog post: https://www.turnkeylinux.org/blog/introducing-tkldev
.. _fab: https://github.com/turnkeylinux/fab
.. _deck: https://github.com/turnkeylinux/deck
.. _from source: https://github.com/turnkeylinux-apps/
.. _TurnKey Core: https://www.turnkeylinux.org/core
.. _documentation: https://github.com/turnkeylinux-apps/tkldev/tree/master/docs
