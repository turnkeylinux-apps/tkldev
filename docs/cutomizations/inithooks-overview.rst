Inithooks
=========

(For more information regarding inithooks see inithooks package source on github
https://github.com/turnkeylinux/inithooks)

#. The majority of actions performed by inithooks should be in a python script
   called ``<appname>.py`` within ``/usr/lib/inithooks/bin``

    This script should be idempotent

#. This python script should be called by an executable bash script called
   ``<weight><appname>.sh`` where weight is a number used to ensure the inithook
   is ordered correctly, usually 40-50 for general initial setup. These scripts
   should also be made executable.

    This script should be idempotent

    firstboot scripts should source ``/etc/default/inithooks``

    firstboot scripts should also check for the existence of environment
    variables that hold preseeded values, set sane default values when needed but
    not found and pass them to the python inithook where applicable.

    Important: ALL values that do NOT apply to your software should be ignored.

    Note: the following preseedable values are GUARANTEED to be set. Even if their
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

    Other preseed values can be checked and used however sane defaults must
    be put in place to ensure that the appliance is fully functional when only
    base values are pre-seeded.

#. Any secret values need to be regenerated (these are things such as
   API keys, encryption keys, etc. things which should be secret AND unique for
   each server) should be regenerated in a SEPARATE firstboot script usually
   weighted at 20, with a name something like ``20regen-<appname>-secrets``.

    What does and doesn't count as a secret can seem a bit arbitrary so if
    you're having trouble deciding please ask on the forums.

