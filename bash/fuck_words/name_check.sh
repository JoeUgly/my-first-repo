#!/usr/bin/env bash
# Description: Check files and directory names in current directory for problem characters.
	# e.g. ampersand, quotes, whitespace
# Offer nonrecursive option +

detectedchar=0

if [[ $1 =~ '-n' ]]
then
mode="echo $2"
else
mode="find -type f"
fi

# Check for ampersand in names
ampcheck=$($mode | grep \&)
if [[ -n $ampcheck ]]
then
echo -e '\033[1;33m' ~~~  Ampersand\(s\) detected. ~~~
echo -e Run \"fuckamper\" to remove them. '\033[1;32m'\\n
let detectedchar=1
fi

# Check for quotes in names
quocheck=$($mode | grep -e \' -e \")

if [[ -n $quocheck ]]
then
echo -e '\033[1;33m' \\n~~~ Quote\(s\) detected. ~~~
echo -e Run \"fuckquotes\" to remove them. '\033[1;32m'\\n
let detectedchar=1
fi

# Check for whitespace in names
spacecheck=$($mode | grep \\s)

if [[ -n $spacecheck ]]
then
echo -e '\033[1;33m' \\n~~~ Whitespace\(s\) detected. ~~~
echo -e Run \"fuckw\" to remove them. '\033[1;32m'\\n
let detectedchar=1
fi


if [[ $detectedchar -eq 0 ]]
then
echo No problem characters detected. 
fi

# Write results to temp file for other programs
echo $detectedchar >~/code/tmpfile.txt






