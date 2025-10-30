Faster feedback FTW!
====================

Tight feedback loops are the key to having a fun & rewarding development
experience.

Test as early as possible
-------------------------

During development your goal should be to test everything as early and
frequently as possible. The more immediate the feedback you're getting
the better. The faster you can test something works, the earlier you get
can catch mistakes, the more you can achieve in less time. 

VMs are your friend!
--------------------

If developing a new appliance, initial prototyping integration details are
usually best done in a VM install of the "closest" appliance (e.g. LAMP). An
alternative is to just run the ISO in "live" mode. Although don't forget to
take notes as you go and copy out updated files &/or write your conf script as
you go! Stopping or rebooting a "live" instance will lose all your changes!

If updating or building on an existing appliance for a newer minor release
(e.g. v18.1), again initial prototyping and testing will often be quicker in a
VM of the current appliance.

Knowing the best way to work on a major version update of an appliance (e.g.
v19.0) is often a bit of a guess. It may be easier to start with a rebuild
of the current appliance build code on the new base (i.e. updated bootstrap and
common). Other times it may be easier to treat the update as if it were a new
appliance. Often reading the upstream docs regarding requirements for the
newer version to be installed and/or changes between the old version and the
new one will make an educated guess easier.

An important hint though: Always make sure that you copy/paste the commands you
run &/or copy out files you've updated during testing. That is especially
important when working in an appliance build chroot or on a live system.
Otherwise your changes may be gone permanently!

More tips to tighten the feedback loop
--------------------------------------

1) Testing a command is faster than testing a shell script.

2) Testing a single conf script is faster than testing all conf.d/
   scripts together.

3) Testing conf.d scripts in isolation is faster than testing all the
   changes to root.patched together.

4) Testing root.patched by rebuilding root.patched from the root.build
   step is faster than having to wait for root.patched to build from
   scratch after make clean.

5) Testing an app by booting the ISO in live mode is faster than testing
   an app by installing the ISO to a harddrive.

6) Testing the ISO in a VM is faster than burning the ISO to a CD and
   testing on real hardware.
