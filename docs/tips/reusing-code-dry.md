Reusing appliance build code
============================

DRY principle - Don't Repeat Yourself
-------------------------------------

The essence of the DRY principle is to reuse code as much as possible - to
avoid rewriting the same - or similar - code over and over again.

The are a number of ways to minimize the amount of code that you need to write
for new appliances, as well as major appliance updates.

It's also worth noting that there can be a trade off to apply DRY principles to
your code. Sometimes it may be obvious when code can be reused. However often
it is a subjective decision. Sometimes writing code that can be reused in
general cases can be more work than just having specific code in numerous
places. So when it is appropriate to write generalised code is somewhat
subjective.

A good rule of thumb is that if you find yourself spending time trying to
generalize code to account for numerous different scenarios, it's probably time
to back out and just write specific code which can be applied to a known state.

The "common" directory/code repository
======================================

Code that is useful for a number of - or all - appliances (e.g. LAMP based
apps) should go in [`common`](https://github.com/turnkeylinux/common). common
uses a very similar structure to an appliance build code directory. But instead
of `overlay`, `conf.d` and `plan`, the common directories are `overlays`,
`conf` and `plans` respectively. Common also contains a `mk` directory which
allows inclusion of bundles of shared common overlays &/or conf scripts (not
plans).

Common overlays/conf scripts are included in an appliance via it's `Makefile`.
E.g. to apply all common LAMP conf & overlays to an appliance, include this
line in your `Makefile`:

```
include $(FAB_PATH)/common/mk/turnkey/lamp.mk
```

Shared plans work very similarly but are included via your appliance's
`plan/main` file.

For further context on the build code file tree structure, including common,
see the [buildcode directories doc page](../appliance/buildcode-directories.md).


Appliance conf scripts and/or overlays
======================================

DRY in a conf script
--------------------

As appliance conf scripts are bash scripts, the usual bash methods of applying
DRY apply here too. Where relevant use of variables, variable manipulation,
loops & other flow control and/or functions to minimize the amount of code you
need to write are often useful. They can often (but not always) make the conf
script easier to read and/or maintain too.

Writing a simple separate "env" file
------------------------------------

If you find that you have a really big conf script and/or a lot of functions,
you may want to move the functions out and/or break it up into separate conf
scripts. Because each conf script is run in isolation, adding a single conf
script that defines env vars and reusable functions won't work.

It's important to note that scripts in the `conf.d` directory are executed in
alpha-numeric order. I.e. `downloads` runs before `main` and if `00-setup` and
`zzz-final` existed, they would run first and last respectively. You need to
keep this in mind when naming your conf scripts so one script doesn't try to
get information from a file that does not yet exist.

If you only want to have a few environment variables shared between conf
scripts, then you can just use echo a line or 2 directly to a file.

E.g. to write an env var to `/tmp/env` in `downloads`:

```
echo "MY_VAR=$MY_VAR" >> /tmp/env
```

Then you can "load" the contents of the file from another conf script such as
`main` by adding the line `source /tmp/env`. This can be especially useful to
calculate a value in one script and reuse the value in another - without
needing to recalculate the value.

Note the `>>` means that the line will be appended to a file if it already
exists. If want to overwrite a file, use a single `>` instead. If you want to
include quotes in the text written to the file, "escape" the internal quotes
by prefixing `\` E.g. to reuse the above example but quoting the value of
MY_VAR:

```
echo "MY_VAR=\"$MY_VAR\"" >> /tmp/env
```

More complex shared code
------------------------

If you want to create an "env" file with functions writing it using a "heredoc"
is often a better option. E.g.; a silly `conf.d/00-env` example:

```
cat > /tmp/env << EOF
MY_VAR_1="$MY_VAR"
MY_VAR_2="345"

echo_message() {
    # escape $ to evaluate when the function is used
    local stuff_to_echo="\$@"
    echo "message: \$stuff_to_echo"
}

setup_dirs() {
    local default_dir="/some/dir"
    local dir1=\$1
    local dir2=\$2
    mkdir -p "\$dir1 \$dir2 $\default_dir"
    chmod 755 "\$dir1 \$dir2 $\default_dir"
}
```

Then you can load the file and use the functions in other conf scripts. E.g.:

```
#/bin/bash -e

source /tmp/env

echo_message "making dirs"
setup_dirs "/some/dir /some/other/dir"

# more code here...
```

Code that may also be useful for end users
------------------------------------------

If you develop code that might be useful for end users, then it could also be
written via a heredoc. But it's generally cleaner to add the script as a file
in the overlay.

Generally scripts intended to be included in the appliance for use by end users
should go in `/usr/local/bin`. That way they will be in the user's PATH
automatically, but also clear that they do not come from installed apt
packages.

Convention is to prefix end user scripts with `turnkey-` or `tkl-` although
some TKLDev scripts use a `tkldev-` prefix. Similar to conf scripts, scripts in
the overlay must include `#!/bin/bash` (aka a bash "shebang") as the firstline.
They must also be executable.

Where scripts like this are useful for multiple appliances, it may be relevant
to add it to a common overlay instead?
