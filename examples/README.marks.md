directory bookmarking
=====================

bash script to interactively search and select bookmarked directories. I have
used multiple directory bookmarking tricks in my life and this script is
inspired from those. Here are the tricks:

* Use pushd and popd with dirs -v
* Use GNU wdl. I used it in 2007 but now unable to find it on internet. This was using perl
* DirB (http://www.linuxjournal.com/article/10585)
* cdargs (http://linux.die.net/man/1/cdargs)

cdargs deliver a shell script wrapper which works great. The actual cdargs
command called by the shell script tries to do too much like file system
navigation and it does not support search and quick select and is written in
C++ which you cannot edit as easily as python.

This shell script provide a function called marks which shows the directories
bookmarked by cdargs in the pySearchSelect.

To install cdargs on ubuntu execute "sudo apt-get install cdargs". Once cdargs
is installed, get the bash file from
/usr/share/doc/cdargs/examples/cdargs-bash.sh and then source it from your
bashrc.

You may want to update the cdargs-bash.sh to use the marks function to have the
interactive display in place of using the default cdargs. Or you can keep the
cdargs-bash.sh unchanged and use the marks function when you looking for
interactive search.
