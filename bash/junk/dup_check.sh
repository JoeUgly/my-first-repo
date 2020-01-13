#!/usr/bin/env bash

# Description: Find duplicates in directories and ask to delete

# _________________________________ Unusable until further notice. 2/19 ____________________________

# Known bugs:
# File names must not contain string '@@@@@'
# File names must not have problem chars +
# File names must not start with a non alphanumeric char
# Manual directiories must have a trailing /
# Paths must be absolute


# -d to manually set directories
if [[ $1 =~ "-d" ]]
then
echo Enter first directory to check
read tordir
echo Enter second directory to check
read convdir

# or supply directories as args without -d
elif [[ -n $2 ]]
then
tordir=$1
convdir=$2

# otherwise set usual directories
else
tordir=~/Desktop/torrents/
convdir=~/Videos/
fi

echo -e Using these folders: \\n $tordir \\n $convdir


## neccesary?
# Check for the special character
#charcheck=$(find $tordir -type f | grep @)
#if [[ -n $charcheck ]]
#then
#echo -e '\033[1;33m' \\n ~~~  \"@\" detected. ~~~ \\n
#exit
#fi

echo -e Duplicates found in \"$tordir\" and \"$convdir\": '\033[1;37m' \\n


# Set IFS because chaos otherwise
IFS=$(echo -en "\n\b")

# List first dir then grep second dir
for eachfile in $(ls $tordir)
do

# Create search terms by swapping out fist nonletter with special char sequence and then removing that seq
#abeachfile=$(echo "$eachfile" | sed 's|[^a-zA-Z0-9]|@@@@@|g' | awk -F"@@@@@" '{$0=$1}1')
inc_count=0
abeachfile=a
while [[ $(echo $abeachfile | wc -c) -lt 11 ]]
do
let "inc_count++"
#echo inc_count = $inc_count
abeachfile=$(echo "$eachfile" | sed "s|[^a-zA-Z0-9]|@@@@@|$inc_count" | awk -F"@@@@@" '{print $1}')
echo abeachfile = $abeachfile
#echo $abeachfile | wc -c
done
echo -e \\n\\n 1

foundmatch=$(ls -A "$convdir" | sed 's|[^a-zA-Z0-9]|@@@@@|g' | awk -F"@@@@@" '{$0=$1}1' | grep -iw "$abeachfile")
	
	# 
	if [[ -n "$foundmatch" ]]
	then
	arr+=("$eachfile")
	fullpath="$tordir$eachfile"
	filesize=$(du -sb "$fullpath" | awk '// {print $1;}')
	#echo fullpath = $fullpath
	#echo filesize = $filesize
	inmb=$(echo "scale=1; $filesize/1000000000" | bc)
	sizearr+=($inmb)
	fi

done

# Display dup files and their respective sizes
count=0

# Set abreviated file names
for i in ${arr[@]}; do
abvname=$(echo $i | cut -c 1-50)
abvarr+=($abvname)
done

while [[ $count -lt ${#abvarr[@]} ]]
do
fmt="%-55s%-10s\n"
printf "$fmt" "${abvarr[$count]}" "${sizearr[$count]} GB"
count=$count+1
done


tot=0
for i in ${sizearr[@]}
do
tot=$(echo "$tot+$i" | bc)
done

if [[ ${#arr[@]} -gt 0 ]]
then
printf "$fmt" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~
fmt1="%-55s%0s\n"
printf "$fmt1" "			   Total space to be freed     $tot GB"
echo -e \\n '\033[1;33m' Delete all ${#arr[@]} duplicates from \"$tordir\"? \\n
read answer
	if [[ $answer =~ ^('y'|'yes')$ ]]
	then
	echo
		for rmfiles in "${arr[@]}"; do
		rm -rv "$tordir$rmfiles"
		done
	else
	exit
	fi
else
echo -e \\n No duplicates found.
fi













