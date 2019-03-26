New Appliance
=============

* install upstream software
    1. install software from debian repositories. to do this. Simply put the package name(s)
        inside ``plan/main``.

    2. use upstream third party apt repos.

        to do this you must:

        a. check if gpg key is ascii armored or not. Often ascii armored keys are suffixed with
            ``.asc`` however running ``file <key.gpg|asc>`` will give you a definitive result.

            ``<filename>: PGP public key block ...`` for ascii armored

            ``<filename>: GPG key public ring ...`` for un-armored

        b. if the gpg key IS armored, you need to either ensure it has a ``.asc`` extension OR
           dearmor the key using ``cat <file> | gpg --dearmor > <file>-unarmored.gpg``

        c. place a copy of the repositories gpg key in ``/usr/share/keyrings``

        d. add ``deb [signed-by=/usr/share/keyrings/<key-name>.gpg] <url> <codename> <component>``
            where ``key-name`` is the filename of the gpg key.

        e. in a ``conf.d/...`` script run ``apt update`` and ``apt install <package>``

    3. use a third party package management system such as pip, npm, composer, etc.

    4. install from upstream binary release

    5. install from upstream source


* Makefile

    1. copy the makefile from core

    2. set any appropriate build flags within the makefile

        WEBMIN_FW_TCP_INCOMING
            tcp ports which are allowed through firewall

        WEBMIN_FW_UDP_INCOMING
            tcp ports which are allowed through firewall

        WEBMIN_FW_NAT_EXTRA
            extra nat controls?
    
        NONFREE
            enable nonfree debian repo

        more build flags

* inithooks
    (For more information regarding inithooks see inithooks package source on github
    https://github.com/turnkeylinux/inithooks)

    1. the majority of actions performed by inithooks should be in a python script
        called ``<appname>.py`` within /usr/lib/inithooks/bin

        this script should be idempotent

    2. this python script should be called by an executable bash script called
        ``<weight><appname>.sh`` where weight is a number used to ensure the inithook
        is ordered correctly, usually 40-50 for general initial setup. These scripts
        should also be made executable.

        this script should be idempotent

        firstboot scripts should source ``/etc/default/inithooks``

        firstboot scripts should also check for the existence of environment
        variables that hold preseeded values, set sane default values when needed but
        not found and pass them to the python inithook where applicable.

        Note: the following preseedable values are GARUANTEED to be set. even if their
            value is "DEFAULT", they all should be set.

            ROOT_PASS should be entirely ignored as it is the root user password for
                      this appliance

            DB_PASS   should be used as the password for any database relating to
                      this appliance.

            APP_PASS  should be used as the password for any admin account relating
                      to this appliance.

            APP_EMAIL should be used as the admin email for this appliance wherever
                      applicable.

            APP_DOMAIN should be used as the appliance domain wherever applicable.

            HUB_APIKEY should be entirely ignored as it is used by the turnkey hub

            SEC_ALERTS should be entirely ignored as it is used internally

            SEC_UPDATES should be entirely ignored as it is used internally
            
        other preseed values can be checked and used however sane defaults must
        be put in place to ensure that the appliance is fully functional when only
        base values are pre-seeded. 

* tklbam profile
* readme
* screenshots
* changelog

