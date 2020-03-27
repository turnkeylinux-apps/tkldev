Installing Software
-------------------

Install upstream software
    #. Install software from Debian repositories. To do this. Simply put the package name(s)
       inside ``plan/main``.

    #. Use upstream third party apt repos.

        To do this you must:

        #. Setup the repo's GPG key.

            #. Find the third party repo's GPG key.

            #. Check if GPG key is ASCII armored or not. Often ASCII armored keys are suffixed with
                ``.asc`` however running ``file <key.gpg|asc>`` will give you a definitive result.

                ``<filename>: PGP public key block ...`` for ASCII armored

                ``<filename>: GPG key public ring ...`` for unarmored

            #. If the GPG key IS armored, you need to either ensure it has a ``.asc`` extension OR
               de-armor the key using ``cat <file> | gpg --dearmor > <file>-unarmored.gpg``.
               Likewise if the key is NOT armored it must be suffixed with ``.gpg``.

            #. Place a copy of the repositories GPG key in ``/usr/share/keyrings``

            #. Add ``deb [signed-by=/usr/share/keyrings/<key-name>.gpg] <url> <codename> <component>``
               where ``key-name`` is the filename of the GPG key.

        #. Pin the specific packages you want to get from your repo.

			See `AptPreferences <https://wiki.debian.org/AptPreferences>`_ for more information on
			apt pinning. However the following should be enough for turnkey development.

			#. Create a file in ``/etc/apt/preferences.d/<name>``

			#. Pin all packages from this repo to never install by adding the following:

				.. code-block::

					Package: *
					Pin: origin "<url-to-apt-repo>"
					Pin-Priority: 10

				You can still install packages pinned to 10 but only explicitly, never automatically.

			#. Pin all packages you require to priority over default repos.

				.. code-block::

					Package: *
					Pin: origin "<url-to-apt-repo>"
					Pin-Priority: 500

        #. In a ``conf.d/...`` script run ``apt update`` and ``apt install <package>``

    #. Use a third party package management system such as pip, npm, composer, etc.

        It's worth remembering third party package managers still need to be installed i.e. pip is
        provided by Debian repos and should be added to the plan if required.

    #. Install from upstream (applies to source and binary packages)

        #. Create ``conf.d/downloads``

        #. Add the following

            .. code-block:: bash

                dl() {
                    [ "$FAB_HTTP_PROXY" ] && PROXY="--proxy $FAB_HTTP_PROXY"
                    cd $2; curl -L -f -O $PROXY $1; cd -
                }

            This code adds a bash function called ``dl``, it takes 2 arguments, a URL and
            a directory location. It downloads the URL to the given location whilst abiding
            by the proxy settings.

        #. Add variable "URL" which is the download URL of the upstream software and includes
           http/https/etc.

            If the version appears in the URL e.g.:

                "https://www.example.com/download/v3.6.9.tar.gz"

            Then add an addition variable "VERSION" e.g.:

                ``VERSION="3.6.9"``

            And interpolate the VERSION variable into URL variable e.g.:

                ``URL="https://www.example.com/download/v${VERSION}.tar.gz"``

        #. Add ``dl $URL /usr/local/src``

        #. Unpack, set permissions and if applicable; compile in the ``conf.d/main`` script.
