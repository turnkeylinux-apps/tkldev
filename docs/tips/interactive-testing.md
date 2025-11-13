Development and testing in a build chroot
=========================================

When working on appliance development &/or updates, you can tighten the
feedback loop by only rebuilding the build step/s you need to. That will save
you from having to build from scratch to ISO, then install in a VM every time!

Build steps
-----------

As you may know by now the build happens in separate steps. See First packages
noted in the plan/s (first common plans, then the appliance plan) are
installed.

Then the overlays are applied (common & specific)

Adding new packages
-------------------




Interactively exploring a product's filesystem
----------------------------------------------

You can chroot into the product's filesystem to explore, hack or test
stuff interactively without having to make changes to source code.:

```
root@tkldev products/core# make root.sandbox
root@tkldev products/core# fab-investigate build/root.sandbox
(core chroot)root@tkldev /#
```

Then when you're done:

```
(core chroot)root@tkldev /# exit
root@tkldev products/core#
```

For a more detailed example see `Hello world <helloworld.rst>`_.

Remember though, if you do a `make clean` (or rebuild root.patched as noted
below) then any changes within root.sandbox will be lost. So be sure to:

- copy out overlay files you want to keep; &/or
- copy/paste commands you want to rerun at build time into a conf.d script.

Quick re-patch: how to reapply root.patched configurations
----------------------------------------------------------

You'll save a lot of time and accelerate your development cycle if you
realize you don't have to start the build from scratch with a `make clean`
every time you make a change to a conf script or an overlay file.

Removing a build step can be done with `fab-rewind`. E.g. to clean
root.sandbox to play some more without having to completely rebuild
from scratch:

```
root@tkldev products/core# fab-rewind root.patched
root@tkldev products/core# make root.sandbox
root@tkldev products/core# fab-investigate build/root.sandbox
```

To test your updated overlays/conf-scripts, rebuild root.patched:

```
root@tkldev products/core# fab-rewind root.build
root@tkldev products/core# make root.sandbox
```

This is very useful after you tweak the configuration scripts in conf.d/
or files in overlay/ without changing the list of packages in plan/.

Packages listed in plan/ are installed in the root.build step that
root.patched depends on so if you change the plan you need to rebuild
from scratch, i.e.:

```
root@tkldev products/core# make clean
root@tkldev products/core# make root.sandbox
```
