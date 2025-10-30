Appliance buildcode directory overview
======================================

This page provides an overview of the contents of a both an appliance git
repository and the common (shared) build code git repospitory. They are
displayed as a file tree which hopefully makes it easy to see.

Formatting explanation
----------------------

The files and directories are shown in a file tree format, which hopefully
makes it easier to see how it all fits together. To give additional explanation
and context, some specific formatting has been used:

**Notes and explanations:**

General notes about the purpose of a particular path or other specific details
are prefixed with an asterisk: `*`. Short comments will be on the same line as
the path; longer ones on the line after. E.g.:

```
    |- a_path * this is a comment about the path
```
Or
```
    |- another_path
       * this is a longer comment about the purpose of the above path
```

**Optional paths:**

There are a number of optional files/directories, they are surrounded by square
brackets. E.g.:

```
   |- [optional-file-or-dir]
```

**Skipped detail:**

In an effort to make this doc as clear as possible, some detail is skipped. If
a directory may contain additional files and/or directories that is
demonstrated by 3 ellipses within square brackets. I.e.:

```
   |- [...]
```

Example appliance buildcode directory
-------------------------------------

```
.
|-- .art * artwork related to the appliance
|   |-- logo.png
|   |-- screenshot_1.png
|   `-- [...]
|-- .git * revision control information - ignore this dir
|   `-- [...]
|-- .gitignore * files that can be ignored by git
|-- Makefile 
|       * configure optional inclusions from common and some other config
|-- README.rst
|       * appliance overview and notes; source of appliance website page
|-- changelog
|       * since last release of this appliance
|-- conf.d * configuration script/s to run at build time
|   |-- [downloads]
|   |-- main * technically optional but used by convention in 99% of apps
|   `-- [other optional scripts]
|-- [docs] * appliance specific docs - note not included within the appliance
|   `-- [...]
|-- overlay * files to be copied over the root filesystem
|   |-- [etc] 
|   |   |-- [confconsole]
|   |   |   `-- services.txt * services to be displayed by confconsole
|   |   |       * optional because common provides this file, however if there
|   |   |       * are any additional ports/paths include this file with details 
|   |   `-- [...] * other config overlay files in /etc/[...]
|   |-- [root]
|   |   `-- [...] * overlays for root home dir
|   |-- [usr] * overlays to be include in /usr - generally only /usr/local
|   |   |-- [...] * /usr subdirs other than /usr/local should be avoided!
|   |   `-- [local]
|   |       |-- [bin]
|   |       |   `-- [...] * appliance specific custom executable scripts
|   |       `-- [src]
|   |           `-- [...] * source files - often re/moved via conf scripts
|   |-- [var]
|   |   `-- [www] * webroot overlays - where appropriate
|   |       `-- [...]
|   `-- [...] * other overlaid files/dirs
|-- [patches.d]
|   `-- [...]
|       * patches to be applied to build/root.patched; rarely used
`-- plan
    `-- main * packages to be installed at build time
```

Common shared appliance buildcode repository
--------------------------------------------

The below tree view uses the same format as above, although some contents are
generally only intended for internal TKL usage.

Which common components to include are defined via the appliance `Makefile`.
All appliance specific `Makefile`s should include the common TKL make file:
`common/mk/turnkey.mk`. That ensures that all the common conf and overlays
intended for all appliances are included by default. Additional optional shared
common components - and some settings - can also be included via the appliance
specific `Makefile`.

```
.
|-- changes/ * shared changelog snippets (internal changelog generation)
|   |-- README.rst
|   |-- [...]
|   `-- turnkey.changelog
|-- conf/ * common shared conf scripts
|   |-- adminer-apache * optional conf script
|   |-- [...] * these scripts are included via app Makefile
|   `-- turnkey.d/ * conf scripts applied to all appliances
|       |-- confconsole-autorun
|       `-- [...]
|-- keys
|   |-- tkl-bookworm-images.asc
|   |-- tkl-bookworm-main.asc -> ../overlays/bootstrap_apt/usr/share/keyrings/tkl-bookworm-main.asc
|   `-- [...] * image signing keys and links to apt repo signing keys
|-- mk
|   |-- turnkey/ * optional make files to include common groups of conf/overlay
|   |   |-- apache.mk * common conf/overlays for apps with apache (not LAMP)
|   |   |-- [...] * other optional common make files
|   |   `-- lamp.mk * common conf/overlays for apps based on LAMP
|   |-- turnkey-desktop.mk
|   `-- turnkey.mk * common conf/overlays applied to all apps
|-- overlays/ * shared overlays
|   |-- adminer
|   |   `-- [...] * optional overlay files for adminer (included in LAMP)
|   |-- [...] * other optional overlays
|   |   `-- [...]
|   `-- turnkey.d/
|       |-- bashrc
|       |   `-- [...] * bashrc related overlay files for all appliances
|       `-- [...] * other overlay files for all appliances
|-- patches/ * patches are generally only used by third parties
|   |-- [a_patch_file.gz] * optional patch file/s
|   |-- [a_patch_dir] * optional patch dir/s
|   |   |-- [conf]
|   |   `-- [overlay]/
|   |       `-- [...]
|   `-- turnkey.d/
|       `-- [...] * patch file/s &/or dir/s for all apps
|-- plans * plans; lists of deb packages to be installed
|   |-- boot * applied to all apps
|   |-- [...] * other plans to be applied to all apps
|   `-- turnkey/ * optional/app specific plans
|       `-- [...]
|-- removelists * lists of paths to be removed before app specific code applied
|   |-- [...] * optional/app specific removelists
|   `-- turnkey * removelists for all apps
`-- removelists-final * removelists to be applied after app code applied
    |-- [a_removelist] * app specific removelists
    `-- turnkey * removelists for all apps
```
