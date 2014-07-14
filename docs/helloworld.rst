Playing in the sandbox
======================

root.sandbox (root.tmp in earlier TKLDev versions) can be used to
accelerate development with quick and dirty manual prototyping of
changes to the root filesystem. 

This makes it easier to test changes without having to edit source code
and then rebuild from scratch.

root.sandbox is implemented as a copy-on-write filesystem that branches
off from root.patched. If you dirty the sandbox by making changes inside
it, then your changes get saved to a separate overlay in product.iso.

Note that before we start playing in the sandbox the overlay does not
exist::

    root@tkldev products/core# ls -la build/cdroot/casper/*sandbox*
    ls: cannot access build/cdroot/casper/*sandbox*: No such file or directory

Now let's make a small "hello world" change inside the sandbox::

    root@tkldev products/core# fab-chroot build/root.sandbox/
    root@tkldev /# hello
    bash: hello: command not found

    root@tkldev /# apt-get install hello
    Reading package lists... Done
    Building dependency tree       
    Reading state information... Done
    The following NEW packages will be installed:
      hello
    0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
    Need to get 0 B/68.7 kB of archives.
    After this operation, 566 kB of additional disk space will be used.
    debconf: delaying package configuration, since apt-utils is not installed
    Selecting previously unselected package hello.
    (Reading database ... 22578 files and directories currently installed.)
    Unpacking hello (from .../archives/hello_2.8-2_amd64.deb) ...
    Processing triggers for man-db ...
    Setting up hello (2.8-2) ...

    root@tkldev /# hello
    Hello, world!

    root@tkldev /# echo hello > /root/.bashrc.d/hello
    root@tkldev /# chmod +x /root/.bashrc.d/hello
    root@tkldev /# exit
    exit

The result of this small change is that root shells will now say hello::

    root@tkldev products/core# fab-chroot build/root.sandbox/
    Hello, world!
    root@tkldev /# exit
    exit
    root@tkldev products/core# 

Usually building a new ISO from scratch would take about 5 minutes.

But repacking a new ISO for testing only takes about 5 seconds because
we don't need to rebuild everything from scratch, just save the changes
made to the copy-on-write sandbox::

    root@tkldev products/core# time make
    cp build/root.sandbox/usr/lib/syslinux/isolinux.bin build/cdroot/isolinux
    cp build/root.sandbox/boot/vmlinuz-3.2.0-4-amd64 build/cdroot/casper/vmlinuz
    cp build/root.sandbox/boot/initrd.img-3.2.0-4-amd64 build/cdroot/casper/initrd.gz
    rm -f build/cdroot/casper/20sandbox.squashfs
    mksquashfs $(deck --get-level=last build/root.sandbox) build/cdroot/casper/20sandbox.squashfs
    Parallel mksquashfs: Using 1 processor
    Creating 4.0 filesystem on build/cdroot/casper/20sandbox.squashfs, block size 131072.
    [===========================================================================================|] 5/5 100%
    Exportable Squashfs 4.0 filesystem, gzip compressed, data block size 131072
        compressed data, compressed metadata, compressed fragments, compressed xattrs
        duplicates are removed
    Filesystem size 0.85 Kbytes (0.00 Mbytes)
        45.09% of uncompressed filesystem size (1.89 Kbytes)
    Inode table size 232 bytes (0.23 Kbytes)
        38.03% of uncompressed inode table size (610 bytes)
    Directory table size 249 bytes (0.24 Kbytes)
        66.05% of uncompressed directory table size (377 bytes)
    Number of duplicate files found 4
    Number of inodes 19
    Number of files 8
    Number of fragments 1
    Number of symbolic links  0
    Number of device nodes 0
    Number of fifo nodes 0
    Number of socket nodes 0
    Number of directories 11
    Number of ids (unique uids + gids) 1
    Number of uids 1
        root (0)
    Number of gids 1
        root (0)
    genisoimage -o build/product.iso -r -J -l -V core -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table build/cdroot/
    Size of boot image is 4 sectors -> No emulation
      6.68% done, estimate finish Fri Jul 11 16:27:37 2014
     13.34% done, estimate finish Fri Jul 11 16:27:37 2014
     20.01% done, estimate finish Fri Jul 11 16:27:37 2014
     26.67% done, estimate finish Fri Jul 11 16:27:37 2014
     33.35% done, estimate finish Fri Jul 11 16:27:37 2014
     40.01% done, estimate finish Fri Jul 11 16:27:37 2014
     46.68% done, estimate finish Fri Jul 11 16:27:37 2014
     53.34% done, estimate finish Fri Jul 11 16:27:37 2014
     60.02% done, estimate finish Fri Jul 11 16:27:37 2014
     66.68% done, estimate finish Fri Jul 11 16:27:37 2014
     73.35% done, estimate finish Fri Jul 11 16:27:38 2014
     80.01% done, estimate finish Fri Jul 11 16:27:38 2014
     86.69% done, estimate finish Fri Jul 11 16:27:39 2014
     93.36% done, estimate finish Fri Jul 11 16:27:39 2014
    Total translation table size: 2048
    Total rockridge attributes bytes: 1902
    Total directory bytes: 4096
    Path table size(bytes): 40
    Max brk space used 0
    74991 extents written (146 MB)

    real	0m4.980s
    user	0m1.496s
    sys	0m0.716s

How the sandbox works: a peak under the hood
--------------------------------------------

Now that we've "dirtied" the sandbox and rebuilt the product.iso, the
overlay does exist::

    root@tkldev products/core# ls -la build/cdroot/casper/*sandbox*
    -rw-r--r-- 1 root root 3297280 Jul 13 11:09 build/cdroot/casper/20sandbox.squashfs

Let's unpack it to look inside::

    root@tkldev products/core# unsquashfs -dest sandbox-squashfs build/cdroot/casper/20sandbox.squashfs 
    Parallel unsquashfs: Using 2 processors
    2224 inodes (188 blocks) to write

    [=======================================================================================|] 188/188 100%
    created 82 files
    created 332 directories
    created 0 symlinks
    created 0 devices
    created 0 fifos

The sandbox overlay is only 10MB because copy-on-write only saves
filesystem changes (relative to root.patched)::

    root@tkldev products/core# du -s sandbox-squashfs/
    10556	sandbox-squashfs/

    root@tkldev products/core# ls -l sandbox-squashfs/root/.bashrc.d/ sandbox-squashfs/usr/bin/
    sandbox-squashfs/root/.bashrc.d/:
    total 4
    -rwxr-xr-x 1 root root    6 Jul 13 11:00 hello

    sandbox-squashfs/usr/bin/:
    total 32
    -rwxr-xr-x 1 root root 31232 Jun  7  2012 hello

Hacking Core by example: Hello world!
=====================================

We'll now throw away our sandbox and re-implement "hello world" in
source code.

First, we throw away the sandbox::

    deck -D build/root.sandbox

Note that before we implement this, we don't get a hello world when we
chroot into root.patched::

    root@tkldev products/core# fab-chroot build/root.patched/
    root@tkldev /#  exit

Implement hello world change::

    root@tkldev products/core# echo hello >> plan/main 
    root@tkldev products/core# cat plan/main 
    #include <turnkey/base>
    hello
    root@tkldev products/core# mkdir -p overlay/root/.bashrc.d
    root@tkldev products/core# echo hello > overlay/root/.bashrc.d/hello
    root@tkldev products/core# chmod +x overlay/root/.bashrc.d/hello

Rebuild:: 

    root@tkldev products/core# make clean
    root@tkldev products/core# make

Now we do get "hello world"::

    root@tkldev products/core# fab-chroot build/root.patched/
    Hello, world!
    root@tkldev /# exit

Hacking root.patched without rebuilding from scratch
----------------------------------------------------

Note that changing the package installation plan like we did above
(I.e., by adding hello) requires us to "make clean" first.

That can take a few minutes because we need to reinstall all the
packages into the root.build target.

However, we can save time and skip this step if we don't need to change
the package plan. This is the case if we're only making changes to
scripts in conf.d/ or files in overlay/

For example, let's say we want the root shell to print "hello universe"
instead of "hello world".

So we'll edit the root bashrc.d configuration::

    root@tkldev products/core# cat overlay/root/.bashrc.d/hello 
    hello
    root@tkldev products/core# echo echo hello universe > overlay/root/.bashrc.d/hello 

And we'll rebuild root.patched::

    root@tkldev products/core# make root.patched
    make: Nothing to be done for `root.patched'.

Woops. That didn't work because we forgot to tell "make" it needed to
rebuild the already existing root.patched target. 

We do that by removing the rooot.patched "build stamp"::

    root@tkldev products/core# rm build/stamps/root.patched 

It only takes 12 seconds to rebuild root.patched::

    root@tkldev products/core# time make root.patched
    deck -D build/root.patched
    deck build/root.build build/root.patched
    # apply the common overlays
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/apt build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/autologin build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/bashrc build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/etckeeper build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/grub build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/interfaces build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/ntp build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/profile build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/rcS-sulogin build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/resolvconf build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/ssh-emptypw build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/sslcert build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/turnkey-init-fence build/root.patched
    fab-apply-overlay /turnkey/fab/common/overlays/turnkey.d/webmin build/root.patched
    # run the common configuration scripts
    $(call run-conf-scripts, /turnkey/fab/common/conf/turnkey.d)
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/apt
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/busybox
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/console-setup
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/cronapt
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/etckeeper
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/hostname
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/locale
    Generating locales (this might take a while)...
    Generation complete.
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/motd
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/persistent-net
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/roothome
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/rootpass
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/shellinabox
    Adding group `certssl' (GID 1000) ...
    Done.
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/sshd
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/sslcert
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/sysctl
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/vim.tiny
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/webmin-cats
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/webmin-deftab
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/webmin-fw
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/webmin-history
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/webmin-port
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/webmin-theme
    fab-chroot build/root.patched --script /turnkey/fab/common/conf/turnkey.d/webmin-updates
    # apply the common removelists
    fab-apply-removelist /turnkey/fab/common/removelists/turnkey build/root.patched; 
    # apply the product-local root overlay
    if [ -d overlay ]; then fab-apply-overlay overlay build/root.patched; fi
    # run the product-local configuration scripts
    # apply the product-local removelist
    # update initramfs (handle reconfigured initramfs scripts)
    fab-chroot build/root.patched "update-initramfs -u"
    update-initramfs: Generating /boot/initrd.img-3.2.0-4-amd64
    fab-chroot build/root.patched "rm -rf /boot/*.bak"
    # 
    # tagging package management system with release package
    # setting /etc/turnkey_version and apt user-agent
    #
    /usr/share/fab/make-release-deb.py /turnkey/fab/products/core/changelog build/root.patched
    dpkg-deb: building package `turnkey-core-13.0' in `build/root.patched/turnkey-core-13.0_1_all.deb'.
    /usr/share/fab/make-release-deb.py ./changelog build/root.patched
    dpkg-deb: building package `turnkey-core-13.0' in `build/root.patched/turnkey-core-13.0_1_all.deb'.
    fab-chroot build/root.patched "dpkg -i *.deb && rm *.deb && rm -f /var/log/dpkg.log"
    Selecting previously unselected package turnkey-core-13.0.
    (Reading database ... 22631 files and directories currently installed.)
    Unpacking turnkey-core-13.0 (from turnkey-core-13.0_1_all.deb) ...
    Setting up turnkey-core-13.0 (1) ...
    fab-chroot build/root.patched "which insserv >/dev/null && insserv"
    fab-chroot build/root.patched "which postsuper >/dev/null && postsuper -d ALL || true"
    fab-chroot   build/root.patched "rm -f /var/cache/debconf/*-old"; fab-chroot   build/root.patched "rm -f /var/log/dpkg.log"; fab-chroot   build/root.patched "rm -f /var/log/apt/*"; fab-chroot   build/root.patched "rm -f /var/cache/apt/*.bin"; fab-chroot   build/root.patched "rm -f /var/cache/apt/archives/*.deb"; fab-chroot   build/root.patched "rm -rf /var/lib/apt/lists/*"; fuser -k  build/root.patched || true;
    touch build/stamps/root.patched

    real	0m11.819s
    user	0m3.284s
    sys	0m3.176s

Now a root shell launched inside root.patched says hello universe
instead of hello world::

    root@tkldev products/core# fab-chroot build/root.patched/
    hello universe
    root@tkldev /# exit

We can test the integration by chrooting into root.patched, or we can
continue with the build and test the product.iso image (e.g., in a VM)

The default make target is product.iso so if we run make with no 
target it will just continue from where it left off (root.patched in
this example)::

    root@tkldev products/core# time make
    if [ -e build/cdroot ]; then rm -rf build/cdroot; fi
    cp -a /turnkey/fab/cdroots/gfxboot-turnkey build/cdroot
    mkdir build/cdroot/casper
    if [ -d cdroot.overlay ]; then fab-apply-overlay cdroot.overlay build/cdroot; fi
    /usr/bin/mksquashfs build/root.patched build/cdroot/casper/10root.squashfs -no-sparse
    Parallel mksquashfs: Using 2 processors
    Creating 4.0 filesystem on build/cdroot/casper/10root.squashfs, block size 131072.
    [=====================================================================================================|] 24754/24754 100%
    Exportable Squashfs 4.0 filesystem, gzip compressed, data block size 131072
        compressed data, compressed metadata, compressed fragments, compressed xattrs
        duplicates are removed
    Filesystem size 135873.83 Kbytes (132.69 Mbytes)
        38.36% of uncompressed filesystem size (354167.31 Kbytes)
    Inode table size 296013 bytes (289.08 Kbytes)
        29.63% of uncompressed inode table size (998902 bytes)
    Directory table size 284687 bytes (278.01 Kbytes)
        46.79% of uncompressed directory table size (608393 bytes)
    Number of duplicate files found 1213
    Number of inodes 29458
    Number of files 23630
    Number of fragments 1584
    Number of symbolic links  2770
    Number of device nodes 38
    Number of fifo nodes 0
    Number of socket nodes 0
    Number of directories 3020
    Number of ids (unique uids + gids) 18
    Number of uids 6
        root (0)
        man (6)
        libuuid (100)
        ntp (101)
        proxy (13)
        shellinabox (103)
    Number of gids 17
        root (0)
        tty (5)
        kmem (15)
        disk (6)
        shadow (42)
        certssl (1000)
        bin (2)
        utmp (43)
        crontab (102)
        ssh (104)
        staff (50)
        libuuid (101)
        proxy (13)
        ntp (103)
        shellinabox (105)
        adm (4)
        mail (8)
    touch build/stamps/cdroot
    deck -D build/root.sandbox
    deck build/root.patched build/root.sandbox
    touch build/stamps/root.sandbox
    cp build/root.sandbox/usr/lib/syslinux/isolinux.bin build/cdroot/isolinux
    cp build/root.sandbox/boot/vmlinuz-3.2.0-4-amd64 build/cdroot/casper/vmlinuz
    cp build/root.sandbox/boot/initrd.img-3.2.0-4-amd64 build/cdroot/casper/initrd.gz
    rm -f build/cdroot/casper/20sandbox.squashfs
    genisoimage -o build/product.iso -r -J -l -V core -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table build/cdroot/
    Size of boot image is 4 sectors -> No emulation
      6.67% done, estimate finish Sun Jul 13 14:24:22 2014
     13.35% done, estimate finish Sun Jul 13 14:24:22 2014
     20.00% done, estimate finish Sun Jul 13 14:24:22 2014
     26.68% done, estimate finish Sun Jul 13 14:24:22 2014
     33.34% done, estimate finish Sun Jul 13 14:24:22 2014
     40.01% done, estimate finish Sun Jul 13 14:24:22 2014
     46.67% done, estimate finish Sun Jul 13 14:24:22 2014
     53.34% done, estimate finish Sun Jul 13 14:24:22 2014
     60.00% done, estimate finish Sun Jul 13 14:24:22 2014
     66.67% done, estimate finish Sun Jul 13 14:24:22 2014
     73.33% done, estimate finish Sun Jul 13 14:24:22 2014
     80.00% done, estimate finish Sun Jul 13 14:24:22 2014
     86.66% done, estimate finish Sun Jul 13 14:24:22 2014
     93.32% done, estimate finish Sun Jul 13 14:24:22 2014
    Total translation table size: 2048
    Total rockridge attributes bytes: 1816
    Total directory bytes: 4574
    Path table size(bytes): 40
    Max brk space used 0
    75014 extents written (146 MB)
    isohybrid build/product.iso

    real	0m51.614s
    user	1m30.394s
    sys	0m4.080s

What next?
==========

* `Development`_: understand how stuff works in greater detail.

.. _Development: development/README.rst

