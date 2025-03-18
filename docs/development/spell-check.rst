Spell checking
==============

Ultimately, some auto spell checking for relevant files (and even git commit
messages) would be awesome, but for now, we'll settle with manual install and
setup.

Install
-------

apt update
apt install aspell aspell-en

Usage - non-interactive
-----------------------

To get a list of words that the spellchecker doesn't recognise, first cd to the
appliance build code directory, then::

   export COMMON=$FAB_PATH/common
   cat changelog | aspell list -a \
                     --encoding=utf-8 \
                     --personal=$PWD/spelling/.dic \
                     --add-extra-dicts=$PWD/spelling/dic \
                     --add-extra-dicts=$COMMON/spelling/common.dic \
                     --add-extra-dicts=$COMMON/spelling/common_changelog.dic \
                     > MIS_SPELLED.changelog

   export COMMON=$FAB_PATH/common
   cat README.rst | aspell list -a \
                     --encoding=utf-8 \
                     --personal=$PWD/spelling/.dic \
                     --add-extra-dicts=$PWD/spelling/dic \
                     --add-extra-dicts=$COMMON/spelling/common.dic \
                     --add-extra-dicts=$COMMON/spelling/common_readme.dic \
                     > MIS_SPELLED.readme

Usage - interactive
-------------------

It is suggested that you run the above and add any new words (that are spelled
right) to the spelling/dic (or one of the common dic files). Once you are ready
to interactively run through this, you can do it like this::

   export COMMON=$FAB_PATH/common
   aspell -c changelog \
         --dont-backup \
         --encoding=utf-8 \
         --personal=$PWD/spelling/.dic \
         --add-extra-dicts=$PWD/spelling/dic \
         --add-extra-dicts=$COMMON/spelling/common.dic \
         --add-extra-dicts=$COMMON/spelling/common_changelog.dic

   export COMMON=$FAB_PATH/common
   aspell -c README.rst \
         --dont-backup \
         --encoding=utf-8 \
         --personal=$PWD/spelling/.dic \
         --add-extra-dicts=$PWD/spelling/dic \
         --add-extra-dicts=$COMMON/spelling/common.dic \
         --add-extra-dicts=$COMMON/spelling/common_readme.dic

sort -f | uniq 
