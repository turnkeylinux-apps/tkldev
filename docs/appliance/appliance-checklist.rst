Makefile
--------

See `Sane Base <../development/customizations/howto-new-app.rst>`_ and
    `Makefile <../development/customizations/howto-new-app.rst>`_.

- [ ] ensure any ``/common/mk/turnkey/*`` loaded BEFORE ``/common/mk/turnkey.mk``
- [ ] shared code included from common rather than re-implemented

Upstream Software
-----------------

Third Party Apt Repos
~~~~~~~~~~~~~~~~~~~~~
- [ ] gpg keys are set up correctly
    - [ ] gpg keys downloaded to ``/usr/share/keyrings``
    - [ ] ascii armored gpg keys are either dearmored or have a ``.asc`` suffix
    - [ ] ``/etc/apt/sources.list`` line includes ``[signed-by=/usr/share/keyrings/<key>.gpg]``
- [ ] apt pinning
    - [ ] packages MEANT for install are pinned to 500
    - [ ] packages NOT meant for install are pinned to 10

Third Party Package Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    not sure what to put here

Install from Upstream
~~~~~~~~~~~~~~~~~~~~~

- [ ] ``conf.d/downloads`` setup correctly
    - [ ] ``conf.d/downloads`` includes proxy compliant ``dl`` function.
    - [ ] URL variable points to download URL.
    - [ ] VERSION variables interpolates into URL variable if applicable.
    - [ ] both source and binary packages downloaded to ``/usr/local/src``

- [ ] ``conf.d/main`` setup correctly
    - [ ] compilation occurs in ``conf.d/main``

Inithooks vs Conf.d/Main
~~~~~~~~~~~~~~~~~~~~~~~~

- [ ] any one-time configuration that doesn't include secrets should always be in ``conf.d/main``
- [ ] any idempotent configuration which isn't required for basic functionality should PROBABLY be in inithooks
- [ ] any one-time configuration that does include secrets should be treated on a case-by-case basis possibly
      in ``conf.d/main`` with secret regeneration occuring in firstboot scripts.

Inithooks
~~~~~~~~~

- [ ] ensure any of the following preseed values that ARE related to this appliance should be passed from
      firstboot scripts to the inithooks:

    - ROOT_PASS
    - DB_PASS
    - APP_PASS
    - APP_EMAIL
    - APP_DOMAIN

- [ ] all non standard pre-seed values MUST have sane defaults or initialization from hub wont work.
- [ ] ensure passwords are all set
- [ ] ensure admin email is set and added to inithooks cache

Other
-----

- [ ] tklbam profile is up-to-date and working
- [ ] changelog has been updated - see `Changelog <../development/changelog.rst>`_
- [ ] if applicable readme has been updated
- [ ] if applicable artwork has been updated
