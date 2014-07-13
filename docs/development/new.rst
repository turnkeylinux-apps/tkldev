Developing a new TurnKey appliance
==================================

Before developing an appliance from scratch, it's recommended to read
over the source code of a few `existing appliances`_. You should also be
familiar with `appliance maintenance`_.

If you're looking for new appliance ideas, take a look at `Appliance
candidates`_ on the `Wiki`_ for inspiration.

Requirements
------------

* Open source.
* No proprietry software, binaries, database dumps, etc.
* Compliance with the recommended `Git Flow`_.
* Compliance with the `Debian Policy`_ and `Filesystem Hierarchy Standard (FHS)`_.
* Completely automated build.
* Fully tested (chroot, live, installed).
* Changelog, readme and images.

High level steps
----------------

Update the Tracker Wiki
'''''''''''''''''''''''

The `Wiki`_ is used to track appliance candidates as well as a
whiteboard. To faciliate the open development model, it's recommended
that you:

* Create a whiteboard for the appliance you are about to develop.
* Create a candidate, and link it to the whiteboard.
* At a minimum, the whiteboard should include the state of development
  and updated periodically. Additionally, it's a wonderful place to keep
  ideas, development notes and resources related to the appliance.

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
* Does the appliance require accessible public ports that aren't
  pre-configured in the base appliance? If so, they should be defined in
  the ``Makefile`` and ``overlay/etc/confconsole/services.txt``.
* Can installation be performed via command line?

Decide on appliance name
''''''''''''''''''''''''

The appliance name will be used as the repository name, as well as the
appliance hostname, so it should be descriptive yet short.

Preferably the name of the main component should be used, such as
``wordpress`` (lower case). In other cases, be creative, such as
``asp-net-apache``.

Identify closest existing appliance
'''''''''''''''''''''''''''''''''''

By reading the installation documentation you should be familiar with
the required dependencies or base stack, such as `LAMP Stack`_,
`Tomcat-Apache`_, etc. Although the base appliance would be a great
starting point, usually there is another appliance whose code could be
adapted for the new appliance instead of writing it from scratch.

For example, when developing a new LAMP stack based appliance, it might
be better to base off of a `Bugzilla`_ (Debian package available) or
`Vanilla`_ (upstream software only).

Sometimes its just easier to start from scratch, in which case the best
candidate is `TurnKey Core`_.

Clone and start hacking
'''''''''''''''''''''''

Next up, clone the appliance identified above and reinitialize the git
repository::

    cd /turnkey/fab/products
    git-clone https://github.com/turnkeylinux-apps/APPLIANCE.git NEW_NAME
    
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

It is required that appliance builds are non-interactive, and completely
automated. The most common issues you might run into are Debian packages
that require preseeding, and web-based installers.

Debian package pre-seeding
``````````````````````````

For example, the `Drupal6`_ appliance uses the Debian drupal6 package,
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

Most appliances also include application specific inithooks, such as
regenerating secrets, setting the administrative users email address,
password and domain.

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

To improve the user experience of an appliance, either a welcome page/post is
injected into the database (e.g., `MediaWiki conf`_) or a TurnKey Web Control
panel (e.g., `DomainController tklweb-cp`_) is created.

Bonus: TKLBAM profile overrides
'''''''''''''''''''''''''''''''

Each appliance has a `TurnKey Backup and Migration`_ profile, which
describes what should be backed up, and what shouldn't. If you are
intimiate enough with the appliance, you should recommend overrides to
be included in the profile.

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

We're almost done. Appliances should be thoroughly tested. During the
development process you most likely performed lots of testing in the
``root.sandbox`` chroot. It's now time to perform a clean build::

    deck -D build/root.sandbox
    make clean
    make

And test ``build/product.iso`` in a VM (both live and installed).

Changelog, readme and images
----------------------------

The appliance is done, congrats!! There are a few things needed to
finalize the appliance though:

* **changelog**: You can use the changelog from the cloned appliance as
  a base, and extend it as needed. Keep in mind that it must comply with
  the `Debian Policy`_.

* **README.rst**: The readme should include an opening overview
  paragraph and any other information that a user of the appliance
  should know. It must be formatted in `reStructuredText`_.

* **images**: The images directory should include a logo and
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
* Create a new issue on the `Issue Tracker`_ with a title resembling
  *New appliance: APPLIANCE NAME* and include a link to your repository
  and wiki page in the description. One of the core developers will take
  it from there.
* Rejoice! Together we are creating a party of superb open source
  software so powerful it will repeal the oppressive laws of
  thermodynamics, and provide our children with a better tomorrow!


.. _existing appliances: https://github.com/turnkeylinux-apps/
.. _appliance maintenance: maintenance.rst
.. _Appliance candidates: https://github.com/turnkeylinux/tracker/wiki/Candidates
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
.. _Issue Tracker: https://github.com/turnkeylinux/tracker/issues

