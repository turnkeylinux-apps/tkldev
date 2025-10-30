TurnKey appliance build steps
=============================

As noted elsewhere, TKLDev builds an appliance in steps. The build steps are
all stored in a `build` sub-directory. They are generated in the following
order and are as follows:

build/root.spec
- a file containing a list of the packages that need to be installed by apt

build/root.build
- a chroot containing the base OS (i.e. bootstrap) with the packages from
  root.spec installed

build/root.patched
- a chroot containing root.build with all common and appliance specific conf
  and overlays applied

build/root.sandbox
- a "sandbox" chroot for testing and playing

build/product.iso
- the completed ISO file; ready for testing or usage

Chroot directory notes
======================

The chroot directories above are "layers" on top of each other. Lower layers
are "read only" and the specific build/ directories will appear empty. E.g.
if you run `make root.patched`, when complete the patched OS will be in
`build/root.patched` and `build/root.build` will appear to be empty.

To "reload" an earlier layer, use `fab-rewind <layer-to-keep>`. E.g.
`fab-rewind root.build` will remove `build/root.patched` & `build/root.sandbox`
(if/when relevant) and `build/root.build` will be populated again, ready for
you to rebuild. Please note though, that the later layer directories and all
the files inside will be deleted.

Other relevant docs
-------------------

For further details about using the build layers during development, please see
the [interactive testing doc page](../tips/interactive-testing.md)
