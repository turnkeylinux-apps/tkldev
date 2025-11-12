TurnKey appliance changelog
===========================

All TurnKey appliances have a changelog file in the base appliance directory.
The changelog must be a plain text file, and be fully compliant with the
`Debian changelog policy`_.


Overview of a changelog entry
-----------------------------

As a general rule, the differences between a new changelog entry in an existing
appliance and a new one are minimal. The main difference is that a new
appliance changelog will only have one entry (the version about to be
released).

A changelog entry should include the appliance name, appliance version and
"dot points" of the changes of significance for that particular release.

A changelog entry should be signed off by the developer who worked on it most
or most recently (which ever seems most appropriate).

E.g. an example changelog entry for appliance 'APP_NAME' v15.1, done by Jeremy:

::

    turnkey-APP_NAME-15.1 (1) turnkey; urgency=low

      * APP_NAME updates/adjustments:

        - Change I did to APP_NAME config for this release noted here.

        - A change which closes an issue on the tracker - closes #123.

      * A more generic change by someone else, including email is optional.
       [ John Citizen <email.address@example.com> ]

    -- Jeremy Davis <jeremy@turnkeylinux.org>  Mon, 29 Apr 2019 10:43:31 +1000


Structure of a changelog entry
------------------------------

**Heading**

The heading starts at the beginning of the top line and is simply the appliance
name & the version number. The other info remains the same.::

    turnkey-APP_NAME-VERSION (1) turnkey; urgency=low

       ^       ^       ^     \                      /
       |       |       |      ----------------------
    Always     |       |               |
    'turnkey'  |   Version, e.g.       |
               |      '15.1'           |
        Appliance name         This bit is always the same.
        ('APP_NAME'),
        e.g. 'wordpress'.

**Changelog line**

Each individual change should be within a separate "dot point", preceded by 2
spaces and an asterisk. In some cases it may make sense to have a "nested" list
of sub-changes. If so, indent a further 2 spaces, and start the line with a
dash ('-'). See example entries below.

If changes include a bugfix and/or a feature request, then the associated issue
number preceded by a hash should be included (e.g. if issue number 123 was
addressed, then include 'closes #123' or similar). See example entry below.

If someone else worked on a specific change, then give credit by appending
their name (or GitHub username if their "real name" isn't known) and email (or
GitHub user URL) within square brackets below any/all change "dot points" that
are relevant. See final example entry below.

E.g.::

      * APP_NAME updates/adjustments:

        - Change I did to APP_NAME config for this release noted here.

        - A change which closes an issue on the tracker - closes #123.

      * A more generic change by someone else, including email is optional.
       [ John Citizen <email.address@example.com> ]

**Sign off**

Each changelog entry should be finalized by a "sign off" line. This should be
the "real name" of the person making the change(s) and the current timestamp
(in the format as compliant with the `Debian changelog policy`_).

If you are updating an existing changelog entry (i.e. adding additional info
prior to a new release), then replace the previous "Sign off" line with your
name/email/current timestamp. Move the existing name/email under any "dot
points" that they had previously added and surround with square brackets.

E.g.::

    -- Jeremy Davis <jeremy@turnkeylinux.org>  Mon, 29 Apr 2019 10:43:31 +1000


What changes to note in a changelog?
------------------------------------

As noted above, the changelog entry should include "changes of significance".
Examples of things to include are:

    Existing appliance (changes in comparison to previous release):

    - Bugs fixed and/or features added/removed - also note the issue number.
    - Modules, extensions, dependencies, etc. that have been
      included/removed/reconfigured.
    - Upstream software installation procedures that have changed (e.g. changed
      software install method).
    - Upstream software version updates (ideally note the specific version
      included).

    New appliance (overview of appliance basics):

    - Appliance the new appliance was based on/built from (e.g. "LAMP").
    - Specific software installed, plus any dependencies of note and/or
      additional modules/extensions (e.g. a particular module with dependencies
      which improves the user experience).
    - Notes on how the software was installed and where from. E.g. "install
      from upstream zip archive" or "install from upstream/3rd party apt repo",
      etc.


When to make a new entry? - existing appliances
-----------------------------------------------

Every new appliance release, must have a new changelog entry, with the new
version noted. Any changes of significance since the previous release should
be included within the changelog entry.

What constitutes a "change of significance" is somewhat subjective. But as a
general rule, any changes done since the last release should be noted. If the
change is something that may be useful for the end user to know, or a future
developer to be aware of; it should definitely be noted. For example, bugs
fixed should always be noted. Even if an appliance is simply rebuilt (with no
changes to the build code) then it still needs a new changelog entry.

There should only be one complete changelog entry for each release. And only
public releases should be represented by a changelog entry. Unreleased betas
or any other development builds should not have a changelog entry, unless
they have been publicly released.

If you are the first to work on an appliance since the last release, then you
should always create a new changelog entry and include it within the pull
request. E.g. add a new changelog entry with a bumped version. For example, if
the last release was 15.0, then the new entry should be 15.1.

You should always sign off on a changelog that you have edited. Ideally use
your real name and your TurnKey email address (if you have one - otherwise an
email with good spam filtering - it will be publicly displayed). Also your
changelog entry should be accompanied with a recent timestamp.

For more details on formatting, please see the previous sections.


When to update an existing entry? - existing appliances
-------------------------------------------------------

If someone has already worked on an appliance and an updated changelog entry
already exists, then update the existing entry. Obviously that only applies if
the new appliance version hasn't yet been released. If it has, then create a
new entry as per above.

If you are unsure whether to create a new entry, or update the existing one,
then you can check. Compare the top changelog entry version against the latest
"stable" version noted on the relevant (website) appliance page. Checking the
latest build on the mirror is another good option. If in doubt ask Jeremy.

Ideally in the future we will have some sort of tool that can automagically
work out whether a changelog needs to be updated, or a new entry made. But
for now, we'll need to make do...

Any new changes (i.e. "dot points") should be added to the existing changelog
entry. The "sign off" line should be replaced, with your details and a current
timestamp. The previous developer's name (and possibly email) should be
surrounded by square brackets and moved to any/all relevant previous "dot
point" entries.

For further details on formatting, please see previous sections


New appliances
--------------

If you are creating a new appliance, then when you make your final submission,
it should include a changelog file. It should only have a *single* changelog
entry pertaining to the new appliance. If based from another appliance, then
all previous entries should be replaced with a single point. E.g. something
like this::

  * Initial appliance release - based on LAMP appliance.

  * Anther point of interest here.

For details on what sort of info to include, please see the "New appliance"
section of "What changes to note in a changelog?" (above).

.. _Debian changelog policy : https://www.debian.org/doc/debian-policy/#debian-changelog-debian-changelog

