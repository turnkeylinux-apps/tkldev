How to Create a New Appliance
=============================

Sane Base
    #. The first thing you should do is find a sane base for your new appliance. Many popular
       software solutions have already been dealt with in turnkey. If this new appliance uses
       PHP it might be best based off LAMP or LAPP, if it uses NodeJS then the nodejs base is
       for you.

        These common bases are used via the Makefile, here is a list of appliances which use
        these bases for you to use as examples.

            ====== ================== ==============
            Base   Appliance Name     URL
            ====== ================== ==============
            lamp   ``<some example>`` ``<some url>``
            lapp   ``<some example>`` ``<some url>``
            node   ``<some example>`` ``<some url>``
            rails  ``<some example>`` ``<some url>``
            web2py ``<some example>`` ``<some url>``
            ====== ================== ==============

    #. Now you've chosen a base we can get started. For this howto we'll use lamp as a base.

        The next thing to do is to cd into /turnkey/fab/products and create your directory
        structure, make it roughly as follows.

        .. code-block:: bash

            APP_NAME=myapp

            mkdir -p $APP_NAME/{overlay,conf.d,plan}
            cd $APP_NAME

        Now we've got our basic appliance build code directory structure first thing we'll
        want to do is create a Makefile.

        All turnkey appliances must include ``$(FAB_PATH)/common/mk/turnkey.mk``
        And all lamp-based appliances must include ``$(FAB_PATH)/common/mk/turnkey/lamp.mk``

        .. note:: 

            all appliance-base specific common makefiles must be included BEFORE turnkey.mk
            as they may modify how turnkey.mk behaves.

        For our lamp based appliance our Makefile will be as follows

        .. code-block:: Makefile

            include $(FAB_PATH)/common/mk/turnkey/lamp.mk
            include $(FAB_PATH)/common/mk/turnkey.mk

Install upstream software
    See `Installing Software <installing-software.rst>`_ for information on installing
    software in appliances.

Makefile
    1. Copy the makefile from core

    2. Set any appropriate build flags within the makefile

        WEBMIN_FW_TCP_INCOMING
            TCP ports which are allowed through firewall

        WEBMIN_FW_UDP_INCOMING
            UDP ports which are allowed through firewall

        WEBMIN_FW_NAT_EXTRA
            extra NAT controls?
    
        NONFREE
            enable non-free Debian repo

        COMMON_CONF
            space separated list of conf scripts to be included from common

        COMMON_OVERLAYS
            space separated list of overlays to be included from common

        CREDIT_ANCHORTEXT
            FIXME: don't know what this does

        CREDIT_LOCATION
            FIXME: don't know what this does

        PHP56

        .. note::
            including common stuff

Inithooks
    See `Inithooks Overview <inithooks-overview.rst>`_ for information
    regarding inithooks

FIXME: the following items have not been documented
* directory structure
* what a chroot is
* build targets and stamps
* buildtasks
* tklbam profile
* readme
* screenshots
* changelog
