#!/usr/bin/env bash
# Description: Recursively copy files to USB, verify, and unmount.

# Known bugs: {Error when trying to copy dir and file.} - Solved?
#	Must cd into original file directory. e.g. Hashing dir1/a and dir2/b will produce error.
#	Destination only works with absolute path.
# 	Must remove quotes from file and dir names.
# 	{Single option only.} - Solved?
# 	Unmount hangs. +


# Tested functions: Multifiles, multidirectories, files and dir recursively, 


# Build array
for everyarg in "$@"
do
	# Check and set options
	# Append array
	if [[ "$everyarg" =~ ^[^-].* ]]
	then
	copyarr+=("$everyarg")

	# -d 	Manually set destination
	elif [[ $everyarg == "-d" ]]
	then
	echo Enter destination
	read destdir
	mandest="true"
	
	# -m	Remain mounted
	elif [[ $everyarg == "-m" ]]
	then
	umdev=xxxxxx

	# -u 	Unmount all drives
	elif [[ $everyarg == "-u" ]]
	then
	umall=$(df | grep sd[bc] | cut -d ' ' -f1)
	umdev=$umall
	fi
done

## this sucks. replace with quoted names
# Check names for problem characters using subshell and tempfile
bash ~/code/name_check.sh -n ${copyarr[@]}

read detectedchar <~/code/tmpfile.txt
rm ~/code/tmpfile.txt

if [[ $detectedchar -ne 0 ]]
then
echo -e '\033[1;37m' Possible problem characters detected.
echo -e Disregard and continue? y/n '\033[1;32m'
read probcharresp
	if [[ $probcharresp =~ ^('y'|'yes')$ ]]
	then
	echo good luck...
	else
	exit
	fi
fi

# Set usual destination
if [[ -z $destdir ]]
then

# If one drive exist then
usualdest=$(find /media/joepers -maxdepth 2 -mindepth 2 -type d | grep -i video)
udmulti=$(printf '%s\n' $usualdest | wc -l)
	if [[ $udmulti -eq 1 ]]
	then
		if [[ -d $usualdest ]]
		then
		destdir=$usualdest
		echo Setting usual destination: \"$destdir\"
		fi
	else

	# Manually set destination
	echo -e '\033[1;37m' Destination not found. Enter destination '\033[1;32m'
	read destdir
	fi
fi

echo -e \\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \\n

## this can be made more sophisticated eg 5 matching letters in a row
# Check and auto-set destination directory
if [[ -z $mandest ]]
then
attemptdir=$(echo ${copyarr[0]} | cut -c 1-5)
founddir=$(find $destdir -type d | grep -i "$attemptdir" | head -1)
printf '%s\n' "${copyarr[@]}"

	if [[ -d $founddir ]]
	then
	echo -e '\033[1;37m' Auto-set directory found. '\033[1;32m'
	echo -e Changing destination from \"$destdir\" to \"$founddir\"  
	destdir=$founddir
	fi
fi

# Set unmount port if not set already
if [[ -z $umdev ]]
then

# Unmount device defined by the destination
ponies=$(echo $destdir | cut -d / -f-4)
umdev=$(df | grep $ponies | cut -d ' ' -f1)
	if [[ -z $umdev ]] 
	then
	umdev="(unmount disabled)"
	fi
fi

echo unmount port = $umdev
echo -e destination = $destdir \\n

IFS=$(echo -en "\n\b")

# copy file(s)
for eachcopyfile in "${copyarr[@]}"
do
#echo ecf "$eachcopyfile"
#echo destdir "$destdir"

rsync --progress -Rruv "$eachcopyfile" "$destdir"
exit1=$?
	if [[ $exit1 -ne 0 ]]
	then
	echo -e '\033[1;31m'\\n\\n~~~~   COPY ERROR = $exit1 \\n EXITING...   ~~~~\\n\\n
	exit
	fi

#destdirandfile="$destdir"/"$eachcopyfile"


done



# List directory contents as files for hashing
hasharr=$(find "${copyarr[@]}" -type f)



for eachhashfile in ${hasharr[@]}
do

# Check hashes for original files
fromhash=$(md5sum "$eachhashfile" | cut -c 1-30)

# Check hashes for copied files
destdirandfile="$destdir"/"$eachhashfile"
tohash=$(md5sum "$destdirandfile" | cut -c 1-30)
	if [[ $fromhash != $tohash ]]
	then
	echo -e '\033[1;31m'\\n\\n~~~~ \\t HASHES DON\'T MATCH \\t $eachhashfile ~~~~\\n\\n'\033[1;32m'
	elif [[ $fromhash == $tohash ]] && [[ -n $fromhash ]]
	then
	echo -e '\033[1;37m' ~~~~ \\t Hashes match. \\t $eachhashfile ~~~~ '\033[1;32m'
	fi
done



# Unmount
count=0
# necessary?
if [[ $umdev =~ .*sd[b,c].* ]]
	then
	echo -e \\n\\n Unmount \"$umdev\"\? \\t 8 sec...\\n
	echo y/n
	read -t 8 answer
		if [[ $answer =~ ^('n'|'no')$ ]]
		then
		exit
		fi
	echo Unmounting $umdev...
	umount -v $umdev
	exit2=$?

	# nonzero exit code should go to response
	# Check unmount
	if [[ $exit2 -eq 0 ]]
	then
		while [[ -n $(df | grep $umdev) ]]
		do
		echo waiting... $count
		sleep 1
			if [[ $count -eq 5 ]]
			then
			echo Unmount is unsuccessful. Try again? or force or lazy?
			echo y/n/f/l
				read $response
				if [[ $response == 'y' ]]
				then
				echo Trying again ...
				elif [[ $response == 'n' ]]
				then
				exit
				# force needs root
				elif [[ $response == 'f' ]]
				then
				umount -vf $umdev
				elif [[ $response == 'l' ]]
				then
				umount -vl $umdev
				else
				echo Invalid response. Trying again...
				fi
			count=0
			fi
		count=$count+1
		done
	echo
	echo -e '\033[1;37m'\\n\\n ~~~~ \\t Unmount successful. \\t ~~~~\\n\\n
	echo
	elif [[ $exit2 -ne 0 ]]
	then
	echo -e '\033[1;31m'\\n\\n ~~~~ \\t UNMOUNT ERROR = $exit2 \\t ~~~~\\n\\n
	fi
fi
