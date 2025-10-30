Getting help via CLI
====================

Did you know that the Makefile is self documenting? You can access the built-in
help by "making" the 'help' target:

```
make help
```

E.g.:

```
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
```
