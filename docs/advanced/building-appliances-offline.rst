Building Applicances Offline
============================

Chanko - Download packages
--------------------------

It is possible to build TurnKey appliances offline; although you will
need to at least initially be online to collect the required packages.
That's where Chanko comes in.

It is highly recommended that you double check that you have all the required
packages cached before trusting that it will successfully build offline. If you
try to build offline and you have missing pacakges, it will fail.

As of TKLDev v14.2, Chanko is included and pre-configed for initial basic
useage. So to download and cache all the packages to build core; using chanko,
do the following:

.. code-block:: bash

    cd chankos/jessie.chanko/
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
normally; you just need to explictly tell TKLDev to do it. We do that by
setting the FAB_POOL environment variable. It shouldn't also be neccessary to
set the RELEASE but I'm going to demonstrate that for interest:

.. code-block:: bash

    CODENAME=$(lsb_release -c | cut -f2)
    cd core
    export FAB_POOL=y
    export RELEASE=debian/$CODENAME
    make

As simple as that! If you get any errors noting packages not found, you may
have missed them when you were loading them via Chanko. Chanko can also get
individual packages. So cd to the Chanko dir and get the required package. E.g.
I need the hello package but I don't have it in my Chanko yet:

.. code-block:: bash

    cd chankos/jessie
    chanko-get hello
    

