Install locally or deploy to cloud
==================================

Like any other TurnKey appliance, TKLDev is available for `download`_ in
multiple build formats from the TurnKey Linux website. 

An even easier way to get an instance of TKLDev up and running is to
deploy it on the Amazon EC2 cloud using the `TurnKey Hub`_. Besides
being easy, doing appliance development on Amazon EC2 has the additional
benefit of providing you with a network connection that is probably much
faster than the one you have locally, shortening download times for
packages and other components.

TKLDev doesn't support cross-architecture builds (yet). That means building an
amd64 type appliance image requires an amd64 build of TKLDev. 

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
.. _download: http://www.turnkeylinux.org/tkldev/

