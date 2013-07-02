Deploy to cloud or install locally
==================================

The easiest way to get up and running fast, not to mention a blazingly
fast network connection, is to deploy TKLDev on the Amazon EC2 cloud
using the `TurnKey Hub`_. Alternatively, it's also available for
download in multiple build formats from the `TurnKey Linux`_ website.

TKLDev is architecture specific, meaning, to build a 64-bit appliance
image, TKLDev amd64 is required.

Connect via SSH
===============

Shellinabox (as well as Webmin) is installed but disabled by default so
as not to conflict with appliance builds. You should connect via an SSH
client.

To streamline connectivity, it's recommended to update your local
``/etc/hosts`` to include ``APPLIANCE_IP tkldev`` and setup SSH
public-key authentication::

    ssh-copy-id root@tkldev
    ssh root@tkldev


.. _TurnKey Hub: https://hub.turnkeylinux.org/
.. _TurnKey Linux: http://www.turnkeylinux.org/tkldev/

