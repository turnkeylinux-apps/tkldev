Optimized Builds
================

Buildtasks - Build TurnKey optimized builds
-------------------------------------------

Buildtasks is the tool that TurnKey uses to build all of the optimized builds.
E.g. OVA, VMDK, Xen, OpenStack, LXC (Proxmox), Docker, etc.

As of TKLDev v14.2, Buildtasks is included with TKLDev. As it's the tool we use
ourselves, it's more aimed at releases, and our release workflow. However, it
is still useful for end users to build alternate appliance builds.

Configuration & Setup
---------------------

.. code-block:: bash

    cd buildtasks/
    mkdir config
    cp config.example/* config/.

The default settings should be fine for builds you plan to use locally.

To keep TKLDev as slim as possible, we decided to not preinstall all of the
dependencies. So please read through the Buildtask `setup docs`_ and install
the appropriate dependencies (you won't need them all unless you intend to
build all the appliance types).

Building from TurnKey ISO
-------------------------

To build one of the optimized builds of an official TurnKey ISO, you first need
to install all the relevant dependencies (see above).

For example, let's build Core as an LXC container (aka Proxmox) build. Note
that if there isn't already a Core ISO and matching hash file in /mnt/isos
buildtasks will download it from the TurnKey mirror.

Note: As of v14.2, you need to explictly use the full appliance-version name.
That is in the form:

    APPLIANCE_NAME-VERSION-DEBIAN_CODENAME-ARCH

E.g. Core 14.2 is:

    core-14.2-jessie-amd64

So to build:

.. code-block:: bash

    cd buildtasks/
    ./bt-vm core-14.2-jessie-amd64

When that's finished, you should find an official Core TurnKey ISO (and
matching hash file) in /mnt/isos/ and a Core container build in 
/mnt/builds/container/

Building from your own ISO
--------------------------

This is probably of more interest to most TKLDev users. And it's simple really.
You just need to build your ISO with Buildtasks first, then reprocess your own
ISO.

Say you've developed a new appliance called "new-app" in the usual TKLDev place
(i.e. $FAB_DIR/products/new-app). It's pretty straight forward, the only real
difference is that bt-iso only requires the appliance name (not the full name &
version as per the other scripts).

Note: building an ISO with buildtasks first runs `make clean` in your appliance
directory and rebuilds the iso from scratch.

.. code-block:: bash

    cd buildtasks/
    ./bt-iso new-app

Once that runs, simply run the relevant bt script. Don't forget to install the
relevant dependencies.

.. code-block:: bash

    ./bt-vm new-app-14.2-jessie-amd64


.. _setup docs: https://github.com/turnkeylinux/buildtasks/blob/master/docs/setup
