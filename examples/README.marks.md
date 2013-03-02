directory bookmarking
=====================

python script to interactively search and select bookmarked directories. I have
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

This python script when execute shows the formatted content of the ~/.cdargs.
That is all it does and it does it using pss module.

To install cdargs on ubuntu execute "sudo apt-get install cdargs". Once cdargs
is installed, get the bash file from
/usr/share/doc/cdargs/examples/cdargs-bash.sh and then source it from your
bashrc.

Since marks does not do much on its own you might want to update cdargs-bash.sh
to use marks.

```bash
48if cdargs --noresolve "${1/\/*/}"; then
49   dir=`cat "$HOME/.cdargsresult"`
50   /bin/rm -f "$HOME/.cdargsresult";
51fi

to these updated lines:

marks -s "${1/\/*/}"
if [[ -s $HOME/.cdargsresult ]]; then
    dir=$(cat $HOME/.cdargsresult | sed -e 's!\[.*\] !!g')
fi
```
