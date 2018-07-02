TurnKey appliance changelog
===========================

TurnKey appliances must have a changelog in the base appliance directory.
The changelog must comply with `Debian changelog policy`_.

A changelog entry should include the appliance name, appliance version and
the changes of significance for that particular release (if an existing
appliance). A changelog entry should be signed off by the developer who worked
on it most or most recently (which ever seems most appropriate).

E.g. an example changelog entry for appliance 'APP_NAME' v15.0, done by Jeremy:

::

   turnkey-APP_NAME-15.0 (1) turnkey; urgency=low

     * change I did for this release noted here

     * a change which closes an issue on the tracker - closes #000

     * a change by someone else
       [ John Citizen <email.address@example.com> ]

   -- Jeremy Davis <jeremy@turnkeylinux.org>  Mon, 02 Jul 2018 10:43:31 +1000

When to make a new entry
------------------------

Every time an appliance has changes of significance, the changelog should be
updated.

What consititues a "change of significance" is somewhat subjective. But if it's
something that would be useful for the end user, or a future developer to know
it should be noted.

However, there should only be one complete changelog entry (see example
above) for each release. And only public releases should be represented by a
changelog entry.






E.g. if you work on a released appliance, then add a
new changelog entry with a bumped version (e.g. if last release was 15.0, then
the new entry shoudl be 15.1)


are creating a new appliance, then when
you make your final submission, it should have a single changelog entry with
the proposed 
than add a complete new entry for each time you make changes, just add a new
line(s) to the existing changelog.



An
already released appliance should not have it's changelog and each release should have a
corresponding entry.



If you wish to keep track of changes that you've made 

New appliances should have a single changelog entry only. which notes the base
appliance used (e.g. Core, LAMP, etc)
Below we describe the current process used to import a `new`_ app into
turnkeylinux-apps. The idea is to faciliate easy collaboration with the
original integration developer/maintainer.


.. _Debian changelog policy : https://www.debian.org/doc/debian-policy/#debian-changelog-debian-changelog

