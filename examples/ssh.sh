#!/bin/bash

myDir=~/.mySsh
selSshFile=$myDir/selSshFile
mruSshFile=$myDir/mruSshFile
allSshFile=$myDir/allSshFile

if [ ! -e $myDir ]; then mkdir $myDir; fi
touch $selSshFile;
touch $mruSshFile;
touch $allSshFile;

SSH_CMD=ssh

function myssh()
{
    # If parameter set, use alt_value, else use null string.
    # See http://tldp.org/LDP/abs/html/parameter-substitution.html
    search=${1+" -s $1"}
    # clear any previous selection.
    cat /dev/null > $selSshFile;
    # pss.py shall be available in your $PATH
    pss.py -f $selSshFile -l $(cat $mruSshFile) $(cat $allSshFile) $search
    # if file has some contents
    if [[ -s $selSshFile ]]; then
        pushSshToMruList $(cat $selSshFile);
        $SSH_CMD $(cat $selSshFile);
    fi
}

function pushSshToMruList()
{
    local ssh=$1;
    # remove if exist
    sed -i "/^$ssh\$/d" $mruSshFile;
    # add to the top of the file
    if [[ ! -s $mruSshFile ]]; then
        echo $ssh > $mruSshFile;
    else
        sed -i "1i $ssh" $mruSshFile;
    fi
}

# call this to remove dead ssh from mru list.
function updateMruSshList()
{
    # remove any dead ssh
    # for the terse grep statement see 
    # http://blog.codevariety.com/2012/03/07/shell-subtract-lines-of-one-file-from-another-file/
    for deadSsh in $(grep -Fvx --file=$allSshFile $mruSshFile); do
        sed -i "/$deadSsh/d" $mruSshFile;
    done
}

# call this to add new sshs and remove dead sshs from the list.
function updateAllSshList()
{
    $CT_LSVIEW 2>&1 > $allSshFile
    # TESTING cat /tmp/sshs 2>&1 > $allSshFile
    # remove any ssh which already exist in the mruSshFile
    for ssh in $(cat $mruSshFile); do
        sed -i "/$ssh/d" $allSshFile;
    done
}

# Test helper
function sshdebug()
{
    for i in $selSshFile $mruSshFile $allSshFile; do
        echo "cat $i";
        cat $i;
        echo ""; # new line character
    done
}

# helpful non-interactive functions.
function lastssh()
{
    local lastSsh=$(head -1 $mruSshFile)
    $SSH_CMD $lastSsh
}

function mrussh
{
    PS3="Your choice: "
    export SSH=""
    # running all ssh to the select will be bad, so just stick with most
    # recently used.
    select SSH in $(cat $mruSshFile)
    do
        case $SSH in
        * ) break ;;
        quit ) return ;;
        esac
    done
    pushSshToMruList $SSH
    $SSH_CMD $SSH
}
