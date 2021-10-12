How to add customizations to multiple built images?
===================================================

Common components
-----------------

If you wish to add components to multiple appliances, then you'll want to
include them in common_ (by default on TKLDev: /turnkey/fab/common).

Shared plans - add common packages
----------------------------------
If you wish to add custom packages to multiple builds, the best place to put
them is in a common plan.

In the plans directory, you will find all of the shared plans. The top level
plans are quite generic and you'll almost certainly not want to touch them. In
the plans/turnkey directory, you'll find the base_ plan. That is applied to
all servers (it's essentially Core's plan).

Alternatively, if you don't want to do that, you could create your own custom
plan (I'd recommend putting it in the turnkey directory, e.g.
common/plans/turnkey/custom). Then in each appliance that wants this plan
included, add it near the top of the plan file (e.g. products/core/plan/main
- just below '#include ')::

  #include <turnkey/custom>

Other customizations - shared overlays and conf (and make files)
----------------------------------------------------------------

If you want other common customizations, you can add them to common too.
Including common custom conf scripts and/or overlays is similar (but slightly
different). If you want them to be included in all builds, then you can simply
add new conf script(s) and/or overlays to common/conf/turnkey.d and/or
common/overlays/turnkey.d. Overlays and conf scripts in those locations will
be included in all future builds.

Alternatively, if you don't necessarily want them in all builds, but more than
one, then you can put them in the directory above those (i.e. common/conf/
and/or common/overlays/ respectively). Then you can include them via each
appliance's Makefile. Add them at the top, like this::

   COMMON_OVERLAYS = custom-overlay
   COMMON_CONF = custom-conf

These will use conf/overlay from common/conf/custom-conf &
common/overlays/custom-overlay/ respectively. Additional items can be added on
the end (i.e. space separated list).

To make managing a group of conf script(s) and overlays(s) easier, you can
group then together via a common makefile (in common/mk/turnkey/). E.g.
common/mk/turnkey/custom.mk::

   COMMON_OVERLAYS += custom-overlay
   COMMON_CONF += custom-conf1 custom-conf2

   include $(FAB_PATH)/common/mk/turnkey/custom2.mk
   include $(FAB_PATH)/common/mk/turnkey/custom3.mk

Omit lines that aren't relevant (i.e. in my example I'm including other common
makefiles, which is likely not relevant in your scenario).

Then to use the common makefile, add this to each server Makefile::

   include $(FAB_PATH)/common/mk/turnkey/custom.mk

.. _common: https://github.com/turnkeylinux/common
.. _base: https://github.com/turnkeylinux/common/blob/master/plans/turnkey/base
