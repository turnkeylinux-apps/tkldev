Building Applicances Offline
============================

It is possible to build TurnKey appliances offline; although you will
need to at least initially be online to collect the required packages.
That's where Chanko_ comes in.


Chanko
------

Chanko is a tool to download and cache Debian packages.

It is highly recommended that you double check that you have all the required
packages cached before trusting that it will successfully build offline. If you
try to build offline and you have missing packages, it will fail.


Chanko - Initial Setup
----------------------

Whilst Chanko is included in TKLDev, there is some initital config required.
If you haven't already, please run:

.. code-block:: bash

    tkldev-chanko-setup

Note: this script may not yet be included in TKLDev, you may  need to download
and prepare the script first:

.. code-block:: bash

    GH_URL=https://raw.githubusercontent.com/turnkeylinux-apps/tkldev/master/overlay
    SCRIPT=usr/local/bin/tkldev-chanko-setup
    wget -o /$SCRIPT $GH_URL/$SCRIPT
    chmod +x /$SCRIPT


Chanko - packages for Core
--------------------------

You'll also need to configure the packages which Chanko will download. If you
want to build appliances offline, then this will do the job for Core:

.. code-block:: bash

    # set CHANKO if not already set:
    export CHANKO=${CHANKO:-$FAB_PATH/chankos/$(lsb_release -sc).chanko}

    export FAB_PLAN_INCLUDE_PATH=$FAB_PATH/common/plans
    fab-plan-resolve $FAB_PATH/products/core/plan/main > ${CHANKO}/plan/main

Note: to download packages for an alternate product, replace 'core' with the
name of the appliance whose plan you wish to process.

To download and cache all the required packages using chanko, do the following:

.. code-block:: bash

    cd ${CHANKO}
    chanko refresh -a
    export AMD64=y
    export DEBIAN=y
    echo y | chanko-get plan/main

    # go get yourself a [insert beverage of choice here] while it downloads all
    # those packages


That will collect all the packages needed to build Core offline. For other
appliances you will need to process the relevant plan(s).


Building your Appliance
-----------------------

Now you can build Core offline. It's almost identical to building appliances
normally; you just need to explicitly tell TKLDev to do it. We do that by
setting the FAB_POOL environment variable. It shouldn't also be necessary to
set the RELEASE but I'm going to demonstrate that for interest:

.. code-block:: bash

    CODENAME=$(lsb_release -cs)
    cd core
    export FAB_POOL=y
    export RELEASE=debian/$CODENAME
    make

As simple as that! If you get any errors noting packages not found, you may
have missed them when you were loading them via Chanko. Chanko can also get
individual packages. So cd to the Chanko dir and get the required package. E.g.
I need the hello package but I don't have it in my Chanko yet:

.. code-block:: bash

    cd ${CHANKO}
    chanko-get hello

.. _Chanko: https://github.com/turnkeylinux/chanko
