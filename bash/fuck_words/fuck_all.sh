#!/usr/bin/env bash

# Description: Removes quotes, &, @, $, and whitespace from file and folder names recursively.

# Proposed features: Make characters a variable and use args to include them in search and replace

IFS=$'\n'
here=$(pwd)

# Warn if not in a video dir
if [[ $here =~ ^('/home/joepers/Videos'|'/home/joepers/Desktop/torrents')$ ]]
then
echo
else
echo -e Characters to be removed = \\t \@ \$ \& \' \" \(whitespace\) \\n pwd = $here \\n
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



# Ampersand

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
	echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING AMPER RENAME. EXITING...  ~~~\\n\\n
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
	echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING AMPER RECURSION. EXITING...  ~~~\\n\\n
	exit
	fi
echo

ampcheck=$(find -type f | grep \&)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Single quote

function fucksquo {
for orig in $(ls -A)
do
	# rename if $orig contains a single quote
	hassq="$(echo $orig | grep -e \' -e \" -e @ -e \\$)"
	if [[ -n $hassq ]]
	then
	new=$(echo "$orig" | sed 's|'\''||g'| sed 's|'\"'||g'| sed 's|@||g'| sed 's|\$||g')
			if [[ $orig != $new ]]
			then
			mv -v "$orig" $new
			exit0=$?
			fi		
		if [[ $exit0 -ne 0 ]]
		then
		echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING MISC RENAME. EXITING...  ~~~\\n\\n
		exit
		fi
	fi
done
}

# go into deepest dir first
for dir in $(find -type d -printf "%d %p\n" | sort -r | cut -d ' ' -f2-)
do
cd $here
cd $dir && fucksquo
exit1=$?
done
	if [[ $exit1 -ne 0 ]]
	then 
	echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING MISC RECURSION. EXITING...  ~~~\\n\\n
	exit
	fi
echo

squocheck=$(find -type f | grep -e \' -e \" -e @ -e \\$)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Whitespace

function fuckem {
for orig in $(ls -A)
do

# rename if $orig contains a space
hasspace=$(echo $orig | grep '\s')
if [[ -n $hasspace ]]
then
new=$(echo "$orig" | sed 's| |_|g')
		if [[ $orig != $new ]]
		then
		mv -v "$orig" $new
		exit0=$?
		fi		
	if [[ $exit0 -ne 0 ]]
	then
	echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING SPACE RENAME. EXITING...  ~~~\\n\\n
	exit
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
	echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING SPACE RECURSION. EXITING...  ~~~\\n\\n
	exit
	fi


spacecheck=$(find -type f | grep -e \\s)

# Attempt detection after completion
if [[ -z $ampcheck ]] & [[ -z $squocheck ]] & [[ -z $dquocheck ]] & [[ -z $spacecheck ]]
then
echo -e '\033[1;37m'\\n\\n~~~  All subsitution complete. No errors detected.  ~~~\\n\\n
else
	if [[ -n $ampcheck ]]
	then
	echo -e '\033[1;31m' \\n~~~  AMPERSAND DETECTED AFTER COMPLETION.  ~~~\\n
	fi
	if [[ -n $squocheck ]]
	then
	echo -e '\033[1;31m' \\n~~~  MISC DETECTED AFTER COMPLETION.  ~~~\\n
	fi	
	if [[ -n $spacecheck ]]
	then
	echo -e '\033[1;31m' \\n~~~  WHITESPACE DETECTED AFTER COMPLETION.  ~~~\\n
	fi
fi



