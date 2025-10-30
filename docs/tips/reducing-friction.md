Reducing friction
=================

Auto-completion
---------------

By default TKLDev has auto-completion enabled for commands and paths. Many
commands also have auto-completion for sub commands as well. The way it works
is that you start typing and then use the <Tab> key to complete the
command/path. If there are multiple options, then it requires 2x <Tab> to see
the possibilities. If there are many otions, then it will ask if you wish to
display them all.

git aliases
-----------

All the TurnKey code is stored within Git version control and hosted on GitHub.
Because developing and sharing TurnKey code requires lots of git usage, we
provide a number of shorthand aliases for git preconfigured. To view them all:

```
cat ~/.bashrc.d/git
```

They can be changed or new ones can be added by editing that file. To apply
your changes either open a new shell, or manually load the file:

```
source ~/.bashrc.d/git
```

Note that reloading the file will only overwrite existing aliases and add new
ones. Deleted ones will be retained until you open a new shell.

If you want to disable all of the git aliases, make the script non-executable:

```
chmod -x ~/.bashrc.d/git
```

And then open a new shell.

Jumping around the filesystem with CDPATH
-----------------------------------------

While absolute paths are used in the documentation, the `CDPATH`
environment variable is pre-configured to provide quick and easy
navigation through the filesystem:

```
cd core             # changes to /turnkey/fab/products/core
cd products/core    # changes to /turnkey/fab/products/core
cd common           # changes to /turnkey/fab/common
```

This will work from any current working directory, saving you from the drudgery
of having to type in absolute paths.

Note that CDPATH supports tab auto-completion.

Accessing your TKLDev by name
-----------------------------

To streamline connectivity, it's recommended to update your local hosts file
to point a name to your TKLDev instance's IP. That way you don't need to
remember an IP address. Note that only works if your TKLDev has a static IP.

Note that you need to do this on all PCs that you wish to use when doing TKLDev
development. Editing the hosts file requires root privileges on Linux/Mac and
Administrator privileges Windows. On Linux and Mac, the hosts file is
`/etc/hosts`. On Windows it's `C:\Windows\System32\drivers\etc\hosts`. Each
line is whitespace separated pair of IP and hostname. For example, to add
your TKLDev with an IP of '192.168.1.100' as the hostname 'tkldev' add this
line to your hosts file:

```
192.168.1.100   tkldev
```

Logging in via SSH without a password
-------------------------------------

By default, TKLDev requires access either via SSH or direct access (via the UI
window in a VM, or via physical keyboard and screen on bare metal). Webmin is
still installed, but it is disabled by default to avoid conflict with
appliances being built. Arguably that leaves SSH as the preferred access
method.

Setting up public key authentication for SSH means that you won't need a
password to log in to your TKLDev. I don't have access to a Windows machine at
the moment, so I can't confirm this also works on Windows, but OpenSSH on
Linux and Mac includes a command to copy your public SSH key/s to your TKLDev.
Assuming that you have already set up access via hostname (see above):

```
ssh-copy-id root@tkldev
```

And then enter the root user password. The command will copy across your keys
and exit. From then on key authentication will be the default, so no password
required.
