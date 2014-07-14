TurnKey Core source code walkthrough
====================================

`TurnKey Core`_ is a good place to start, as it's source code is
minimal, and mainly inherits from `common`_.

Makefile
--------

::
	root@tkldev products/core# cat Makefile 
	WEBMIN_FW_TCP_INCOMING = 22 12320 12321

	include $(FAB_PATH)/common/mk/turnkey.mk

The `Makefile`_ includes `common/mk/turnkey.mk`_, which defines default values for
important variables (e.g., COMMON_CONF COMMON_OVERLAYS) and configures the
default `build process`_ for TurnKey apps.

`common/mk/turnkey.mk` in turn includes `fab/share/product.mk`_ which is the main
Makefile. It's designed to be highly configurable and extensible.

plan
----

::
	root@tkldev products/core# cat plan/main 
	#include <turnkey/base>

Core's plan doesn't include packages of its own, but rather includes the
packages defined in `turnkey/base`_. The path is relative to
FAB_PLAN_INCLUDE_PATH which is defined in the `fab/share/product.mk`_.

overlay
-------

The overlay for Core is minimal::

	root@tkldev products/core# find overlay/
	overlay/
	overlay/etc
	overlay/etc/confconsole
	overlay/etc/confconsole/services.txt

In addition Core inherits common overlays through the `common/mk/turnkey.mk`_
``COMMON_OVERLAYS`` configuration which pulls in `common/overlays/turnkey.d`_.

conf.d
------

Core only has a dummy script in ``conf.d``::
	
	root@tkldev products/core# cat conf.d/main 
	#!/bin/sh -ex
	echo "do nothing - core requires no post-package configuration commands"

In addition, like with the overlay configurations, Core inherits common
configuration scripts through the ``mk/turnkey.mk`` ``COMMON_CONF``
configuration which pulls in `common/conf/turnkey.d`_.

As described in the `build process`_, common overlays and confs are applied
before the product-specific ``overlay`` and ``conf.d``.

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
.. _fab/share/product.mk: https://github.com/turnkeylinux/fab/blog/master/share/product.mk
.. _common/mk/turnkey.mk: https://github.com/turnkeylinux/common/blob/master/mk/turnkey.mk
.. _common/overlays/turnkey.d: https://github.com/turnkeylinux/common/tree/master/overlays/turnkey.d
.. _common/conf/turnkey.d: https://github.com/turnkeylinux/common/tree/master/conf/turnkey.d
.. _build process: buildprocess.rst
.. _turnkey/base: https://github.com/turnkeylinux/common/blob/master/plans/turnkey/base
.. _changelog: https://github.com/turnkeylinux-apps/core/blob/master/changelog
.. _readme: https://github.com/turnkeylinux-apps/core/blob/master/README.rst
.. _.art: https://github.com/turnkeylinux-apps/core/tree/master/.art

