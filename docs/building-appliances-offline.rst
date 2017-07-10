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

    PLAN_DIR=$FAB_PATH/common/plans
    BASE_PLAN=$PLAN_DIR/turnkey/base
    INCLUDES=$(sed -n "/#include/ s|^.*<|${PLAN_DIR}/|; s|>.*$||p" $BASE_PLAN)
    grep -v \#include $BASE_PLAN > /tmp/base.plan

    cd chanko/jessie.chanko/
    chanko refresh -a
    export AMD64=y
    for plan in $INCLUDES /tmp/base.plan; do
        echo y | chanko get $plan
    done

    # go get yourself a [insert beverage of choice here] while it downloads all
    # those packages


That should give you all the packages that you need to build Core offline. For
other appliances you will need to also download some additional packages. 
Hopefully that is fairly straight forward?!

Building your Appliance
-----------------------

Now you can build your appliance offline. It's almost identical to building
appliances normally; you just need to explictly tell TKLDev to do it. We do
that by setting FAB_POOL. It shouldn't also be neccessary to set the RELEASE
but I'm going to demonstrate that for interest:

.. code-block:: bash

    CODENAME=$(lsb_release -c | cut -f2)
    cd core
    export FAB_POOL=y
    export RELEASE=debian/$CODENAME
    make

As simple as that! If you get any errors noting packages not found, you may
have missed them when you were loading them via Chanko. To resolve that, simply
cd to the Chanko dir and get the required package. E.g. I need the hello-world
package but I don't have it in my Chanko yet: 

.. code-block:: bash

    cd chankos/jessie
    chanko-get hello-world
    

