#!/usr/bin/env bash
# Description: Removes quotes from file and folder names recursively.

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

function fucksquo {
for orig in $(ls -A)
do

# Single quote

	# rename if $orig contains a single quote
	hassq="$(echo $orig | grep \')"
	if [[ -n $hassq ]]
	then
	new=$(echo "$orig" | sed 's|'\''||g')
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
cd $dir && fucksquo
exit1=$?
done
	if [[ $exit1 -ne 0 ]]
	then 
	echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING RECURSION. EXITING...  ~~~\\n\\n
	exit
	fi


squocheck=$(find -type f | grep \')

if [[ -z $squocheck ]]
then
echo  -e '\033[1;37m'\\n\\n~~~  Single quote subsitution complete. No errors detected.  ~~~\\n\\n
else
echo  -e '\033[1;31m' \\n\\n~~~  SINGLE QUOTE DETECTED AFTER COMPLETION.  ~~~\\n\\n
fi





# Double quote
function fuckdquo {
for orig in $(ls -A)
do

# Double quote

	# rename if $orig contains a double quote
	hassq="$(echo $orig | grep \")"
	if [[ -n $hassq ]]
	then
	new=$(echo "$orig" | sed 's|'\"'||g')
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
cd $dir && fuckdquo
exit1=$?
done
	if [[ $exit1 -ne 0 ]]
	then 
	echo -e '\033[1;31m' \\n\\n~~~  ERROR DURING RECURSION. EXITING...  ~~~\\n\\n
	exit
	fi


dquocheck=$(find -type f | grep \")

if [[ -z $dquocheck ]]
then
echo  -e '\033[1;37m'\\n\\n~~~  Double quote subsitution complete. No errors detected.  ~~~\\n\\n
else
echo  -e '\033[1;31m' \\n\\n~~~  DOUBLE QUOTE DETECTED AFTER COMPLETION.  ~~~\\n\\n
fi



