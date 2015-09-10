Test as early as possible: faster feedback loops FTW
====================================================

Tight feedback loops are the key to having a fun & rewarding development
experience.

During development your goal should be to test everything as early and
frequently as possible. The more immediate the feedback you're getting
the better. The faster you can test something works, the earlier you get
can catch mistakes, the more you can achieve in less time. 

1) prototyping integration details on a live system (e.g., Core or LAMP
   Stack) is faster than having to go through the build system. 

2) testing a command is faster than testing a shell script

3) testing a single conf script is faster than testing all conf.d/
   scripts together

4) testing conf.d scripts in isolation is faster than testing all the
   changes to root.patched together

5) testing root.patched by rebuilding root.patched from the root.build
   step is faster than having to wait for root.patched to build from
   scratch after make clean 

6) testing an app by booting the ISO in live mode is faster than testing
   an app by installing the ISO to a harddrive

7) testing the ISO in a VM is faster than burning the ISO to a CD and
   testing on real hardware

Interactively exploring a product's filesystem
----------------------------------------------

You can chroot into the product's filesystem to explore, hack or test
stuff interactively without having to make changes to source code::

    root@tkldev products/core# make root.sandbox
    root@tkldev products/core# fab-chroot build/root.sandbox

To make testing easier any changes you make in the sandbox will
(temporarily) show up in the next ISO image build. If you want to keep
these changes you'll need to update the source though.

For a more detailed example see `Hello world <helloworld.rst>`_.

Quick re-patch: how to reapply root.patched configurations
----------------------------------------------------------

You'll save a lot of time and accelerate your development cycle if you
realize you don't have to start the build from scratch with a "make
clean" every time you make a change to the conf/ or overlay/.

Removing a build stamp forces make to rebuild that step::

    root@tkldev products/core# rm build/stamps/root.patched 

    root@tkldev products/core# make root.sandbox
    root@tkldev products/core# fab-chroot build/root.sandbox

root.sandbox depends on root.patched in the Makefile so after removing
the root.patched stamp root.sandbox will be automatically rebuilt.

This is very useful after you tweak the configuration scripts in conf.d/
or files in overlay/ without changing the list of packages in plan/.

Packages listed in plan/ are installed in the root.build step that
root.patched depends on so if you change the plan you need to rebuild
root.build.

CHROOT_ONLY: suppress ISO build and packages required for boot
--------------------------------------------------------------

Here's a time saving tip if you're at the stage where you only want to
experiment inside chroot. You can get a lot of mileage inside chroot
before you need to resort to testing an ISO on real hardware or a VM.
This allows faster development cycles.

You can suppress building of the ISO images like this::

    export CHROOT_ONLY=yes

Now running "make" will only proceed to the root.patched and
root.sandbox steps. No cdroot or ISO will be created.

This will also suppress installation of packages that are required to
boot the system such as the kernel, ISO bootloader (e.g., casper) and
the init system.

If you get tired of setting this in your shell environment you can make
it permanent::
    
    echo "export CHROOT_ONLY=yes" >> /root/.bashrc.d/tkldev
    chmod +x /root/.bashrc.d/tkldev
    

Reducing friction
=================

Jumping around the filesystem with CDPATH
-----------------------------------------

While absolute paths are used in the documentation, the ``CDPATH``
environment variable is pre-configured to provide quick and easy
navigation through the filesystem::

    cd core             # changes to /turnkey/fab/products/core
    cd products/core    # changes to /turnkey/fab/products/core
    cd common           # changes to /turnkey/fab/common

This will work from any current working directory, saving you from
the drudgery of having to type in absolute paths.

Note that CDPATH supports tab auto-completion.

Logging in via SSH without a password
-------------------------------------

To streamline connectivity, it's recommended to update your local
``/etc/hosts`` to include ``APPLIANCE_IP tkldev`` and setup SSH
public-key authentication::

    ssh-copy-id root@tkldev
    ssh root@tkldev

Shellinabox (as well as Webmin) is installed but disabled by default so
as not to conflict with builds that may use it. You should connect via
an SSH client.

Installing an ISO image to a USB drive
======================================

This assumes you are running Linux. Turn the ISO into a USB/CDROM hybrid -
this step happens automatically on newer versions of TKLDev::

    isohybrid build/product.iso

Identify the device path (e.g., /dev/sdc) of your USB drive::

    # lsblk
    sde                                     8:64   1   7.4G  0 disk  
    └─sde1                                  8:65   1   7.4G  0 part  /media/usbdrive

If it's been automounted, unmount it::

    umount /media/usbdrive

Use dd to write the ISO image to the disk path. That's /dev/sde NOT /dev/sde1::

    dd if=build/product.iso of=/dev/sde

Things to keep in mind:

- **Root access is required**: You will need to perform the above commands as root.
  On Ubuntu prepend the commands with sudo (e.g., sudo apt-get install
  syslinux)

- **dd will completely overwrite your USB drive**:. Any data on it will be lost so
  if you use this method you'll want to use it with a dedicated USB device.

- **dd needs to write to the disk path, not the partition path**: in the
  above example /dev/sde is the disk path device, /dev/sde1 is the
  partition path (e.g., sde1 is the first partition on sde). You need to
  write to the disk path because isohybrid prepends a partition
  structure to the ISO.

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

