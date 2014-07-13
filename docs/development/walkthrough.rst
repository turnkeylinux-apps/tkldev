TurnKey Core source code walkthrough
====================================

`TurnKey Core`_ is a good place to start, as it's source code is
minimal, and mainly inherits from `common`_.

Makefile
--------

::

    include $(FAB_PATH)/common/mk/turnkey.mk

As you can see, the `Makefile`_ includes `mk/turnkey.mk`_, which defines
variables and the `build process`_ for TurnKey apps. `mk/turnkey.mk` in
turn includes `fab/share/product.mk`_ which is the main Makefile.

The ``fab's product.mk`` is designed to be configurable and extendable.

plan
----

::

    #include <turnkey/base>

Core's plan doesn't include packages of its own, but rather includes the
packages defined in `turnkey/base`_. The path is relative to
FAB_PLAN_INCLUDE_PATH which is defined in the ``fab's product.mk``.

overlay
-------

The overlay is minimum, but lets not forget that `mk/turnkey.mk`_
defines ``COMMON_OVERLAYS`` which specifies common
`overlays/turnkey.d`_.

conf.d
------

Core doesn't have a ``conf.d``, but as we saw in the overlay,
``mk/turnkey.mk`` defines ``COMMON_CONF`` which specifies common
`conf/turnkey.d`_.

As described in the `build process`_, common overlays and confs are
applied before the product ``overlay`` and ``conf.d``.

changelog, readme and images
----------------------------

The `changelog`_ describes changes for each release, and the version
specified is used in the product release package.

The `readme`_ and `.art`_ (logo and screenshots) are used to
automatically generate the website page on the TurnKey Linux website. In
the future it will be used to automatically generate listings for
"unofficial" integrations developed by the community.

.. _TurnKey Core: https://github.com/turnkeylinux-apps/core/
.. _common: https://github.com/turnkeylinux/common/
.. _Makefile: https://github.com/turnkeylinux-apps/core/blob/master/Makefile
.. _mk/turnkey.mk: https://github.com/turnkeylinux/common/blob/master/mk/turnkey.mk
.. _build process: buildprocess.rst
.. _fab/share/product.mk: https://github.com/turnkeylinux/fab/blog/master/share/product.mk
.. _turnkey/base: https://github.com/turnkeylinux/common/blob/master/plans/turnkey/base
.. _overlays/turnkey.d: https://github.com/turnkeylinux/common/tree/master/overlays/turnkey.d
.. _conf/turnkey.d: https://github.com/turnkeylinux/common/tree/master/conf/turnkey.d
.. _changelog: https://github.com/turnkeylinux-apps/core/blob/master/changelog
.. _readme: https://github.com/turnkeylinux-apps/core/blob/master/README.rst
.. _.art: https://github.com/turnkeylinux-apps/core/tree/master/.art

