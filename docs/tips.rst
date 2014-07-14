Logging in via SSH without a password
=====================================

To streamline connectivity, it's recommended to update your local
``/etc/hosts`` to include ``APPLIANCE_IP tkldev`` and setup SSH
public-key authentication::

    ssh-copy-id root@tkldev
    ssh root@tkldev

Shellinabox (as well as Webmin) is installed but disabled by default so
as not to conflict with builds that may use it. You should connect via
an SSH client.

Jumping around the filesystem with CDPATH
=========================================

While absolute paths are used in the documentation, the ``CDPATH``
environment variable is pre-configured to provide quick and easy
navigation through the filesystem::

    cd core             # changes to /turnkey/fab/products/core
    cd products/core    # changes to /turnkey/fab/products/core
    cd common           # changes to /turnkey/fab/common

This will work from any current working directory, saving you from
the drudgery of having to type in absolute paths.

Note that CDPATH supports tab auto-completion.

Interactively exploring a product's filesystem
==============================================

You can chroot into the product's filesystem to explore, hack or test
stuff interactively without having to make changes to source code::

    root@tkldev products/core# make root.sandbox
    root@tkldev products/core# fab-chroot build/root.sandbox

To make testing easier any changes you make in the sandbox will
(temporarily) show up in the next ISO image build. If you want to keep
these changes you'll need to update the source though.

For a more detailed example see `Hello world <helloworld.rst>`_.

Quick re-patch: how to reapply root.patched configurations
==========================================================

If we've only tweaked the configuration scripts in conf.d/ or files in overlay/
without changing the package installation plan then we can update
root.patched quickly without having to wait for TKLDev to reinstall all
packages::

    root@tkldev products/core# rm build/stamps/root.patched 
    root@tkldev products/core# make root.patched

Suppress building the product.iso
=================================

You can suppress building of the ISO images like this::

    export CHROOT_ONLY=yes

You might want to do this if you're at the stage where you only want to
experiment inside chroot. You can get a lot of mileage inside chroot
before you need to resort to testing an ISO on real hardware or a VM.
This allows faster development cycles.

If you get tired of setting this in your shell environment you can make
it permanent::
    
    echo "export CHROOT_ONLY=yes" >> /root/.bashrc.d/tkldev
    chmod +x /root/.bashrc.d/tkldev
    
Getting help
============

Did you know that the Makefile is self documenting?::

    root@tkldev products/core# make help
    === Configurable variables
    Resolution order:
    1) command line (highest precedence)
    2) product Makefile
    3) environment variable
    4) built-in default (lowest precedence)

    # Mandatory variables        [VALUE]
      FAB_PATH                   /turnkey/fab
      RELEASE                    debian/$(shell lsb_release -s -c)

    # Build context variables    [VALUE]
      CONF_VARS                  HOSTNAME ROOT_PASS NONFREE WEBMIN_THEME WEBMIN_FW_TCP_INCOMING WEBMIN_FW_TCP_INCOMING_REJECT WEBMIN_FW_UDP_INCOMING WEBMIN_FW_NAT_EXTRA WEBMIN_FW_MANGLE_EXTRA CREDIT_STYLE CREDIT_STYLE_EXTRA CREDIT_ANCHORTEXT CREDIT_LOCATION

      FAB_ARCH                   $(shell dpkg --print-architecture)
      FAB_POOL                   
      FAB_POOL_PATH              
      FAB_PLAN_INCLUDE_PATH      $(FAB_PATH)/common/plans/
      CDROOTS_PATH               $(FAB_PATH)/cdroots/
      COMMON_CONF_PATH           $(FAB_PATH)/common/conf/
      COMMON_OVERLAYS_PATH       $(FAB_PATH)/common/overlays/
      COMMON_REMOVELISTS_PATH    $(FAB_PATH)/common/removelists/

    # Local components           [VALUE]
      PLAN                       plan/main
      REMOVELIST                 
      ROOT_OVERLAY               overlay/
      CONF_SCRIPTS               conf.d/
      CDROOT_OVERLAY             cdroot.overlay/

    # Global components          [VALUE]
      POOL                       /
      BOOTSTRAP                  $(FAB_PATH)/bootstraps/$(CODENAME)/
      CDROOT                     gfxboot-turnkey
      MKSQUASHFS                 /usr/bin/mksquashfs
      MKSQUASHFS_OPTS            -no-sparse
      COMMON_CONF                turnkey.d 
      COMMON_OVERLAYS            turnkey.d 
      COMMON_REMOVELISTS         turnkey

    # Product output variables   [VALUE]
      O                          build/
      ISOLABEL                   $(shell basename $(shell pwd))

    # Built-in configuration options:
      DEBUG                      Turn on product debugging
      KERNEL                     Override default kernel package
      EXTRA_PLAN                 Extra packages to include in the plan
      CHROOT_ONLY                Build a chroot-only product

    === Usage
    # remake target and the targets that depend on it
    $ rm $O/stamps/<target>; make <target>

    # build a target (default: product.iso)
    $ make [target] [O=path/to/build/dir]
      redeck            # deck unmounted input/output decks (e.g., after reboot)

      clean             # clean all build targets
      bootstrap         # minimal chrootable filesystem used to bootstrap the root
      root.spec         # the spec from which root.build is built (I.e., resolved plan)
      root.build        # created by applying the root.spec to the bootstrap
      root.patched      # deck root.build and apply the root overlay and removelist
      root.sandbox      # temporary changes here are squashed into a separate layer
      cdroot            # created by squashing root.patched into cdroot template + overlay
      product.iso       # product ISO created from the cdroot

      updated-initramfs # rebuild product with updated initramfs

