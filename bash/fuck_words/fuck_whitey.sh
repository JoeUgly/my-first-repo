#!/usr/bin/env bash
# Description: Removes spaces from file and folder names recursively.

IFS=$'\n'
here=$(pwd)

# Warn if not in a video dir
if [[ $here =~ ^('/home/joepers/Videos'|'/home/joepers/Desktop/torrents')$ ]]
then
echo
else
echo pwd = $here
echo Present working directory is not \"Video\" nor \"torrent\" folder.
echo Continue?
echo y/n
read resp
	if [[ $resp =~ ^('yes'|'y')$ ]]
	then
	echo
	else
	exit
	fi
fi

function fuckem {
for orig in $(ls -A)
do

# rename if $orig contains a space
hasspace=$(echo $orig | grep \\s)
if [[ -n $hasspace ]]
then
new=$(echo "$orig" | sed 's| |_|g')
	if [[ $orig != $new ]]
	then
	mv -v "$orig" $new
	exit0=$?		
		if [[ $exit0 -ne 0 ]]
		then
		echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING RENAME. EXITING...  ~~~\\n\\n
		exit
		fi
	fi
fi
done
}

# go into deepest dir first
for dir in $(find -type d -printf "%d %p\n" | sort -r | cut -d ' ' -f2-)
do
cd $here
cd $dir && fuckem
exit1=$?
done
	if [[ $exit1 -ne 0 ]]
	then 
	echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING RECURSION. EXITING...  ~~~\\n\\n
	exit
	fi

# Attempt detection after completion
spacecheck=$(find -type f | grep -e \\s)

if [[ -z $spacecheck ]]
then
echo  -e '\033[1;37m'\\n\\n~~~  Done. No errors detected.  ~~~\\n\\n
else
echo  -e '\033[1;31m' \\n\\n~~~  WHITESPACE DETECTED AFTER COMPLETION.  ~~~\\n\\n
fi

