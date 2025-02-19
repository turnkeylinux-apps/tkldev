TKLDev - TurnKey Development Toolchain and Build System
=======================================================

TKLDev_ is the mother of all TurnKey appliances. It's used to give birth
to them all, including new versions of itself. It's designed to make
simple things simple, and hard things possible. It's a self-contained
build system that can be used to rapidly prototype and repeatably build
TurnKey appliances `from source`_. Or for that matter, any generic
Debian-based Linux distribution. It also supports `building packages
from source`_ too.

To get started have a look at the `documentation`_. Read the `blog post`_
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

.. _TKLDev: https://github.com/turnkeylinux-apps/tkldev
.. _from source: https://github.com/turnkeylinux-apps/
.. _building packages from source: https://github.com/turnkeylinux-apps/tkldev/blob/master/docs/advanced/building-packages-from-source.rst
.. _documentation: https://github.com/turnkeylinux-apps/tkldev/blob/master/docs
.. _blog post: https://www.turnkeylinux.org/blog/introducing-tkldev
.. _TurnKey Core: https://www.turnkeylinux.org/core
.. _fab: https://github.com/turnkeylinux/fab
.. _deck: https://github.com/turnkeylinux/deck
.. _TurnKey Core: https://www.turnkeylinux.org/core
