Developing a new TurnKey app
============================

Before attempting to develop a new integration from scratch, it's
recommended to read over the source code of a few `existing apps`_.
Bonus points if you are already familiar with the `maintenance`_
process.

If you're looking for ideas, take a look at `candidates`_ on the `Wiki`_
for inspiration. Note that your integration doesn't have to be a
server-type app. It can be any Linux distribution (e.g., a desktop
system)

Requirements for official inclusion in TurnKey GNU/Linux
--------------------------------------------------------

* Contains free open source software.
* A completely automated build. No interactive steps.
* Following recommended practices in `Debian Policy`_ and `Filesystem Hierarchy Standard (FHS)`_.

High level steps
----------------

Update the Tracker Wiki
'''''''''''''''''''''''

The `Wiki`_ is used to track candidates as well as a whiteboard. To
faciliate the open development model, it's recommended that you:

* Create a whiteboard page for the integration you're develloping.
* Create a candidate, and link it to the whiteboard.
* Ideally, the whiteboard page is updated periodically with the state of
  development. It's also a good place to keep ideas, development notes
  and related resources.

Read upstream installation documentation, take notes
''''''''''''''''''''''''''''''''''''''''''''''''''''

Understanding how to install the software, its dependencies and
configuration is obviously important, so reading through all the
available documentation and taking notes is paramount.

Thing to look out for:

* Is there a recommended configuration for production deployments?
* What are the dependencies if any? Are they version specific?
* Are components available as packages in Debian? If so, these packages
  will be added to the ``plan``.
* Are components only available upstream? If so, what are the download
  URLs? Are releases signed and verifiable via GPG? If so, this
  information will most likely be added to ``conf.d/downloads``.
* Does the system require accessible public ports that aren't
  pre-configured in Core? If so, they should be defined in
  the ``Makefile`` and ``overlay/etc/confconsole/services.txt``.
* Can installation be performed via command line?

Decide on a name
''''''''''''''''

The name will be used as the repository name, as well as the hostname,
so it should be descriptive yet short.

Preferably the name of the main component should be used, such as
``wordpress`` (lower case). In other cases, be creative, such as
``asp-net-apache``.

Identify closest existing integration
'''''''''''''''''''''''''''''''''''

By reading the installation documentation you should be familiar with
the required dependencies or base stack, such as `LAMP Stack`_,
`Tomcat-Apache`_, etc. Although Core will work as a starting point, look
around if there is another TurnKey app whose code can be more easily
adapted to do what you want.

For example, when developing a new LAMP stack based integration, it
might be better to base off of a `Bugzilla`_ (Debian package available)
or `Vanilla`_ (upstream software only).

Sometimes its just easier to start from scratch, in which case the best
candidate is `TurnKey Core`_.

Clone and start hacking
'''''''''''''''''''''''

Next up, clone the integration repository you want to fork off of and
reinitialize the git repository to reset the history::

    cd /turnkey/fab/products
    git-clone https://github.com/turnkeylinux-apps/core.git NEW_NAME
    
    cd NEW_NAME
    rm -rf .git
    git-init

Now you can start hacking and commiting new code. You'll usually want to
start with the ``Makefile``, ``plan`` and finally ``conf.d and
overlay``.

It's usually easier to comment out code in conf.d scripts, rename the
overlay to something temporary, and build the ``root.sandbox`` for manual
integration and testing::

    make CHROOT_ONLY=y
    fab-chroot build/root.sandbox
    
    # start required services
    
    # perform installation and configuration manually, while updating
    # the conf.d and overlay so it can be done automatically.
    
    # stop services
    
    exit

Then, test your code::

    deck -D build/root.sandbox
    deck -D build/root.patched
    make CHROOT_ONLY=y

Rince and repeat as needed.

Completely automated build
''''''''''''''''''''''''''

It is required that builds are non-interactive, and completely
automated. The most common issues you might run into are Debian packages
that require preseeding, and web-based installers.

Debian package pre-seeding
``````````````````````````

For example, TurnKey `Drupal6`_ uses the Debian drupal6 package,
but the database setup cannot be completed during the build. In this
case, we preseed the package and reconfigure it in the conf::

    debconf-set-selections << EOF
    drupal6 drupal6/dbconfig-reinstall boolean true
    EOF
    DEBIAN_FRONTEND=noninteractive dpkg-reconfigure drupal6

Web based installers
````````````````````

When there is no command line based installation, you sometimes need to
use the web based installer. Automating this is usually done by
scripting ``curl`` to perform the installation.

Firefox has a great extension called ``Live HTTP Headers``, which allows
you to perform the installation with the browser while capturing all the
requests and responses in a log. Using this log, it's easy to script the
installation, for example, in `Joomla25`_::

    URL="http://127.0.0.1/installation/index.php"
    CURL="curl -c /tmp/cookie -b /tmp/cookie"

    $CURL $URL --data "jform%5Blanguage%5D=en-US&task=setup.setlanguage&$SEC=1"
    $CURL ${URL}?view=preinstall
    $CURL ${URL}?view=database
    $CURL $URL --data "jform%5Bdb_type%5D=mysqli&jform%5Bdb_host%5D=localho...
    ...

But, you can get creative. For example, in `WordPress`_ we create a
``turnkey-install.php`` and call it with ``curl`` to perform the
installation and configuration automatically.

Initialization Hooks (inithooks)
''''''''''''''''''''''''''''''''

Initialization hooks are an important part of the user experience as
well as a security mechanism. You should already be familiar with some
of the inithooks that run on firstboot, such as the regeneration of SSL
certificates, SSH keys, setting the root and database passwords, etc.

Many integrations also include application specific inithooks, that do
things such as regenerating secrets, setting the admin user's email
address, password, etc.

Note that when the email and/or domain are not required, inithooks are
not required nor recommended. For example, some applications require a
domain name, but it's possible to bypass this requirement by serving all
domains. For example, in `TomatoCart`_ the ``conf`` script sets the
domain to be dynamic::

    CONF=$WEBROOT/includes/configure.php
    sed -i "s|HTTP_SERVER'.*|HTTP_SERVER', 'http://'.\$_SERVER['HTTP_HOST']);|" $CONF
    sed -i "s|HTTPS_SERVER'.*|HTTPS_SERVER', 'https://'.\$_SERVER['HTTP_HOST']);|" $CONF

When inithooks are required, such as in `Drupal7`_, the following naming
conventions should be used::

    overlay/usr/lib/inithooks/bin/drupal7.py
    overlay/usr/lib/inithooks/firstboot.d/20regen-drupal7-secrets
    overlay/usr/lib/inithooks/firstboot.d/40drupal7

Inithooks are executed in alpha-numeric ordering. Secret regeneration
should be prefixed with ``20`` and application settings such as email,
passwords and domain with ``40``.

Application passwords are usually stored as hashes in the database. When
possible, the hashing mechanism should be implemented in Python (e.g.,
`GitLab inithook`_). When not feasible, leverage embedded code (e.g.,
`Vanilla inithook`).

Note that inithooks must support being run multiple times, as well as
handle service state. For example:

* If a service is required and is not running, it should be started,
  action performed, then stopped returning it to it's previous state.
* If a service must not be running but is, it should be stopped, action
  performed, then restarted returning it to it's previous state.

Bonus: Welcome post / tklweb-cp
'''''''''''''''''''''''''''''''

To improve the user experience a welcome page/post is injected into the
database (e.g., `MediaWiki conf`_) or a TurnKey Web Control panel (e.g.,
`DomainController tklweb-cp`_) is created.

Bonus: TKLBAM profile overrides
'''''''''''''''''''''''''''''''

Each TurnKey app has a `TurnKey Backup and Migration`_ profile, which
describes what should be backed up, and what shouldn't. 

For example, to keep bloat out of `Drupal7`_, backup sessions, cache and
search tables are excluded::

    $ cat overlay/etc/tklbam/overrides
    -mysql:drupal7/sessions
    -mysql:drupal7/cache
    -mysql:drupal7/cache_filter
    -mysql:drupal7/cache_menu
    -mysql:drupal7/cache_page
    -mysql:drupal7/cache_views
    -mysql:drupal7/devel_queries
    -mysql:drupal7/devel_times
    -mysql:drupal7/search_dataset
    -mysql:drupal7/search_index
    -mysql:drupal7/search_total

The same can be done for `directory paths`_.

Testing
-------

We're almost done. To avoid nasty surprises integrations should be well
tested. During the development process you most likely performed lots of
testing in the ``root.sandbox`` chroot. It's now time to perform a clean
build::

    deck -D build/root.sandbox
    make clean
    make

And test ``build/product.iso`` in a VM (both live and installed).

Packaging: changelog, readme and artwork
----------------------------------------

Your new Linux distribution is done, congrats! TurnKey apps follow a
packaging convention with the idea of making automatic maintenance of
integration showcases eventually automatic.

Components:

* **changelog**: You can use the changelog from the integration you
  started out from (e.g., Core) as a base, and extend it as needed. The
  format is the same as for Debian packages. The Debian devscripts
  package includes a helper to make the changelog easier to edit::
  
    dch -i

* **README.rst**: The readme should include an opening overview
  paragraph and any other information that you think users should know.
  Like this document, it's formatted in `reStructuredText`_.

* **.art**: This directory should include a logo and
  screenshots. Templates and guidelines are available in `TurnKey
  Artwork`_.

Publishing
----------

Woohoo! You did it. The final step is to get it included in the TurnKey
Linux library:

* If you haven't already, register a new repository on GitHub and push
  your branch.

* If you haven't already, update the whiteboard on the `Wiki`_ you
  created earlier.

* Create a new issue on the `Issue Tracker`_ with a #new-appliance tag.

.. _existing apps: https://github.com/turnkeylinux-apps/
.. _maintenance: maintenance.rst
.. _candidates: https://github.com/turnkeylinux/tracker/wiki/Candidates
.. _wiki: https://github.com/turnkeylinux/tracker/wiki
.. _Git Flow: https://github.com/turnkeylinux/tracker/blob/master/GITFLOW.rst
.. _Debian Policy: http://www.debian.org/doc/debian-policy/
.. _Filesystem Hierarchy Standard (FHS): http://www.pathname.com/fhs/
.. _LAMP Stack: https://github.com/turnkeylinux-apps/lamp/
.. _Tomcat-Apache: https://github.com/turnkeylinux-apps/tomcat-apache/
.. _Bugzilla: https://github.com/turnkeylinux-apps/bugzilla/
.. _Vanilla: https://github.com/turnkeylinux-apps/vanilla/
.. _TurnKey Core: https://github.com/turnkeylinux-apps/core/
.. _Drupal6: https://github.com/turnkeylinux-apps/drupal6/
.. _Joomla25: https://github.com/turnkeylinux-apps/joomla25/
.. _Wordpress: https://github.com/turnkeylinux-apps/wordpress/
.. _TomatoCart: https://github.com/turnkeylinux-apps/tomcatocart/
.. _Drupal7: https://github.com/turnkeylinux-apps/drupal7/
.. _GitLab inithook: https://github.com/turnkeylinux-apps/gitlab/blob/master/overlay/usr/lib/inithooks/bin/gitlab.py
.. _Vanilla inithook: https://github.com/turnkeylinux-apps/vanilla/blob/master/overlay/usr/lib/inithooks/bin/vanilla_pass.php
.. _MediaWiki conf: https://github.com/turnkeylinux-apps/mediawiki/blob/master/conf.d/main
.. _DomainController tklweb-cp: https://github.com/turnkeylinux-apps/domaincontroller/blob/master/overlay/var/www/index.shtml
.. _TurnKey Backup and Migration: http://www.turnkeylinux.org/tklbam/
.. _directory paths: http://www.turnkeylinux.org/faq/backup-and-migration-tklbam#t601n2382
.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _TurnKey Artwork: https://github.com/turnkeylinux/artwork/
.. _Issue Tracker: https://github.com/turnkeylinux/tracker/issues?labels=new-appliance

