#!/usr/bin/env bash
# Description: Removes ampersands from file and folder names recursively.

IFS=$'\n'
here=$(pwd)

# Warn if not in a video dir
if [[ $here =~ ^('/home/joe/Videos'|'/home/joe/Desktop/torrents')$ ]]
then
echo
else
echo pwd = $here
echo Present working directory is not \"Video\" nor \"torrent\" folder.
echo Continue?
echo y/n
read resp
fi
if [[ $resp =~ ^('yes'|'y')$ ]]
then
echo
else
exit
fi 

function fuckamp {
for orig in $(ls -A)
do

# rename if $orig contains an ampersand
hasamp="$(echo $orig | grep \&)"
if [[ -n $hasamp ]]
then
new=$(echo "$orig" | sed 's|&|and|g')
		if [[ $orig != $new ]]
		then
		mv -v "$orig" $new
		exit0=$?
		fi		
	if [[ $exit0 -ne 0 ]]
	then
	echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING RENAME. EXITING...  ~~~\\n\\n
	exit
	fi
fi
done
}

# go into deepest dir first
for dir in $(find -type d -printf "%d %p\n" | sort -r | cut -d ' ' -f2-)
do
cd $here
cd $dir && fuckamp
exit1=$?
done
	if [[ $exit1 -ne 0 ]]
	then 
	echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING RECURSION. EXITING...  ~~~\\n\\n
	exit
	fi


ampcheck=$(find -type f | grep \&)

if [[ -z $ampcheck ]]
then
echo  -e '\033[1;37m'\\n\\n~~~  Done. No errors detected.  ~~~\\n\\n
else
echo  -e '\033[1;31m' \\n\\n~~~  AMPERSAND DETECTED AFTER COMPLETION.  ~~~\\n\\n
fi

