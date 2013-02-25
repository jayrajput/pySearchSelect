#!/bin/bash

myDir=~/.viewSearchSelect
selViewFile=$myDir/selViewFile
mruViewFile=$myDir/mruViewFile
allViewFile=$myDir/allViewFile

if [ ! -e $myDir ]; then mkdir $myDir; fi
touch $selViewFile;
touch $mruViewFile;
touch $allViewFile;

CT_SETVIEW="cleartool setview "
CT_LSVIEW="cleartool lsview -short "
# FORTESTING CT_SETVIEW="echo"
# FORTESTING CT_LSVIEW="cat /tmp/views"

function myview()
{
    # clear any previous selection.
    cat /dev/null > $selViewFile;
    # $pySearchSelect shall be defined and be in your $PATH
    $pySearchSelect -f $selViewFile -l $(cat $mruViewFile) $(cat $allViewFile)
    # if file has some contents
    if [[ -s $selViewFile ]]; then
        pushViewToMruList $(cat $selViewFile);
        $CT_SETVIEW $(cat $selViewFile);
    fi
}

function pushViewToMruList()
{
    local view=$1;
    # remove if exist
    sed -i "/^$view\$/d" $mruViewFile;
    # add to the top of the file
    if [[ ! -s $mruViewFile ]]; then
        echo $view > $mruViewFile;
    else
        sed -i "1i $view" $mruViewFile;
    fi
}

# call this to remove dead view from mru list.
function updateMruViewList()
{
    # remove any dead view
    # for the terse grep statement see 
    # http://blog.codevariety.com/2012/03/07/shell-subtract-lines-of-one-file-from-another-file/
    for deadView in $(grep -Fvx --file=$allViewFile $mruViewFile); do
        sed -i "/$deadView/d" $mruViewFile;
    done
}

# call this to add new views and remove dead views from the list.
function updateAllViewList()
{
    $CT_LSVIEW 2>&1 > $allViewFile
    # TESTING cat /tmp/views 2>&1 > $allViewFile
    # remove any view which already exist in the mruViewFile
    for view in $(cat $mruViewFile); do
        sed -i "/$view/d" $allViewFile;
    done
}

# Test helper
function viewdebug()
{
    for i in $selViewFile $mruViewFile $allViewFile; do
        echo "cat $i";
        cat $i;
        echo ""; # new line character
    done
}

# helpful non-interactive functions.
function lastview()
{
    local lastView=$(head -1 $mruViewFile)
    $CT_SETVIEW $lastView
}

function mruview
{
    PS3="Your choice: "
    export VIEW=""
    # running all view to the select will be bad, so just stick with most
    # recently used.
    select VIEW in $(cat $mruViewFile)
    do
        case $VIEW in
        * ) break ;;
        quit ) return ;;
        esac
    done
    pushViewToMruList $VIEW
    $CT_SETVIEW $VIEW
}
