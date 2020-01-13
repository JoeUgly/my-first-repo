#!/usr/bin/env bash
# Description: Searches the provided webpages for keyword and attempts one level of crawling.

# things to do:
# resolve "curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connection to labor.ny.gov:443" +
# allow for different options with args eg -m or -x keyword portallocation -
# select states and counties
# AND search
# good hits in real time in parent shell -
# user-defined levels of crawling
# multiple search strings and subshells should be default
# remove grep -a ?
# new easy means of appending to the blacklist


# Blacklist 
checkedarr=$(cat ~/code/current/civ_crawl/blacklist)

# Set variables and counts
hitcount=0
dupomithitcount=0
miscomithitcount=0
totalpages=0
progresscount=0
errorhitcount=0
errorcode=0
funccount=0
abscount=0

# Set args
# Set portal location
if [[ -n $2 ]]
then
portallocation=$2
else
portallocation=~/code/current/civ_crawl/Civil
fi

if [[ -n $1 ]]
then
keyword=$1
else

echo -e Expected runtime = ~17 minutes \\n
echo -e Enter search string or \"-m\" \for multiple search strings
read keyword
fi

# Multiple keyword search
if [[ $keyword =~ "-m" ]]
then
	while [[ $keyword != "end" ]]
	do
		if [[ -z ${keywordarr[@]} ]]
		then
		echo -e \\n Enter first search string
		read keyword
			if [[ $keyword != "end" ]]
			then
			keywordarr+=("$keyword")
			fi
		else
		echo -e \\n Enter next search string or \"end\"
		read keyword
			if [[ $keyword != "end" ]]
			then
			keywordarr+=(\|"$keyword")
			fi
		fi
	done

# Convert keyword array into spaceless variable readable by grep eg one|two|three
keyword=$(printf %s "${keywordarr[@]}" $'\n')
fi

start=$SECONDS
echo -e '\033[0;32m' Searching \for \"$keyword\" ... \\n

# Got to civil service employment portal
for portalurl in $(grep -ao https*.* $portallocation | cut -d \" -f1 | cut -f1 -d$'\t')
do
let progresscount=$progresscount+1
let totalpages=$totalpages+1
	if [[ -z $2 ]]
	then
	echo -e \\n Progress = $progresscount of ~164
	else
	echo -e \\n Progress = $progresscount of $BLOCKSIZE
	fi
echo -e \\n '\033[1;32m' portalurl = "$portalurl" \\n '\033[0;32m'

# Exclude previously checked URLs
dupcheck=$(printf '%s\n' "${checkedarr[@]}" | grep -io "$portalurl")
	if [[ -n $dupcheck ]]
	then
	let dupomithitcount=$dupomithitcount+1
	echo dup omitted = $dupcheck
	else
	
	# Curl portal page
	keywordmatch0=$(curl --max-time 10 --retry 1 -sL "$portalurl")
	errorcode=${PIPESTATUS[0]}

		# Capture curl errors
		if [[ $errorcode -ne 0 ]]
		then
			# Omit duplicate urls
			errdupcheck=$(echo ${errorlog[@]} | grep -i "$portalurl")
			if [[ -z $errdupcheck ]]
			then
			echo -e '\033[1;33m' cURL error at $portalurl '\033[0;32m'
			let errorhitcount=$errorhitcount+1
			errorlog+=(code_=_$errorcode portal_url_=_$portalurl\ )
			fi
		else

		# Search for keyword on portal page
		keywordmatch=$(echo "$keywordmatch0" | grep -aiE "$keyword" | cut -c 1-80)

		# Add to checked array
		checkedarr+=($portalurl)

		# If found keyword match
		if [[ -n $keywordmatch ]]
		then

		# If match contains 'description' or 'spec' then append to seperate array
		#omitspec=$(echo "$portalurl" | grep -aie description -aie specs -aie specification)
		#	if [[ -n $omitspec ]]
		#	then
		#	let miscomithitcount=$miscomithitcount+1
		#	miscomiturlarr+=($portalurl)
		#	echo misc url omitted
		#	else

		# Add match to array
		let hitcount=$hitcount+1
		urlarr+=($portalurl)
		echo -e '\033[1;37m' Found item \#$hitcount 
		echo -e $keywordmatch \\n '\033[1;36m' \\t $portalurl \\n\\n '\033[0;32m'
		fi
		fi
	

workingurl=$portalurl

function crawler {
if [[ $funccount -lt $CRAWLLEVELS ]]
then
let funccount=$funccount+1
let abscount=$abscount+1
echo -e start crawl level $funccount of $CRAWLLEVELS \\n abs = $abscount
echo workingurl = $workingurl

	# Search for job word urls but exclude bunk words
	for pagematch in $(curl --max-time 10 --retry 1 -sL "$workingurl" | grep -aie employment -aie job -aie opening -aie exam -aie test -aie postions -aie civil -aie career | grep -ao href=\".*\" | cut -d \" -f2 | grep -ive ^javascript -ive \.pdf$ -ive ^mailto: -ive ^tel: -ive description -ive specs -ive specification -ive guide)
	do	
	echo pagematch = $pagematch
	let totalpages=$totalpages+1
	
		## maybe move this above create working url
		# Exclude previously checked URLs
		dupcheck=$(printf '%s\n' ${checkedarr[@]} | grep -io "$pagematch")
		if [[ -n $dupcheck ]]
		then
		let dupomithitcount=$dupomithitcount+1
		echo dup omitted = $dupcheck
		else

		## necessary?
		# Create the working url
		if [[ -n $pagematch ]]
		then
		echo portal = $portalurl
		domain=$(echo "$portalurl" | cut -d / -f3)
		echo domain = $domain

		# Correct for rel and abs paths
		doublepath=$(echo "$pagematch" | grep -ai "$domain")
			if [[ -n $doublepath ]]
			then
			workingurl=$pagematch
			else
				if [[ $pagematch =~ ^[http].* ]]
				then
				workingurl=$pagematch
				else
				echo corrected \for rel path
				workingurl=$domain/$pagematch

				## better if trailing or leading slash was removed first
				# Remove double slash
					if [[ $workingurl =~ [^https*:].+// ]]
					then
					echo corrected \for double slash
					workingurl=$domain$pagematch
					fi
				fi
			fi
		echo -e workingurl = \"$workingurl\"
			


		# Search for keyword matches on additional pages
		additionalmatch0=$(curl --max-time 10 --retry 1 -sL "$workingurl")
		errorcode=${PIPESTATUS[0]}

			# Capture curl errors
			if [[ $errorcode -ne 0 ]]
			then

				# Omit duplicate error urls
				errdupcheck=$(echo ${errorlog[@]} | grep -i "$workingurl")
				if [[ -z $errdupcheck ]]
				then
				echo -e '\033[1;33m' cURL error at $workingurl '\033[0;32m'
				let errorhitcount=$errorhitcount+1
				errorlog+=(code_=_$errorcode url_=_$workingurl\ )
				fi
			else



			# Add match to array
			additionalmatch=$(echo "$additionalmatch0" | grep -aiE "$keyword" | cut -c 1-80)
				if [[ -n $additionalmatch ]]
				then
				let hitcount=$hitcount+1
				urlarr+=($workingurl)
				echo -e '\033[1;37m' Found additional item \#$hitcount \\n $additionalmatch
				echo -e '\033[1;36m' \\t $workingurl \\n\\n '\033[0;32m'
				fi
			fi

			# Add to checked array
			checkedarr+=($workingurl)
		fi
		fi


		# Check target level of crawling
		if [[ $funccount -lt $CRAWLLEVELS ]]
		then
echo starting crawl
		crawler
		fi
echo end of crawl level $funccount of $CRAWLLEVELS
echo workingurl = $workingurl
	done

fi	
let funccount=$funccount-1
}


	crawler
fi
done


# Write parellelization results and stats
if [[ -n $2 ]]
then
duration=$(( SECONDS - start ))
echo -e \\n\\n block number xxxxxxxxx \\n Total pages searched = $totalpages \\n Total omitted duplicate hits = $dupomithitcount \\n Duration = $duration seconds \\n Total good hits = $hitcount \\n ${urlarr[@]} >> /home/joepers/code/current/civ_crawl/results
else


# Display nonparallel results and stats
duration=$(( SECONDS - start ))
echo -e '\033[1;32m'\\n\\n Total pages searched = $totalpages
echo -e Duration = $duration seconds \\n '\033[1;36m'

printf '%s\n' "${urlarr[@]}"
echo -e '\033[0;32m' \\n Total good hits = $hitcount \\n '\033[1;37m'

# Open good hits in browser
echo -e \\n Open good hits in browser? \\n y/n
read browserresp
echo -e '\033[0;32m'
if [[ $browserresp =~ ^('yes'|'y')$ ]]
then
firefox ${urlarr[@]}
fi

# necessary?
# Duplicate omitted hits
echo -e \\n '\033[1;32m' Total omitted duplicate hits = $dupomithitcount

# Open misc omitted hits in browser
echo -e \\n '\033[1;36m'
printf '%s\n' "${miscomiturlarr[@]}"
echo -e '\033[1;32m' Total omitted miscellaneous hits = $miscomithitcount '\033[1;37m'
if [[ $miscomithitcount -ne 0 ]]
then
	echo -e \\n Open miscellaneous omitted hits in browser? \\n y/n '\033[0;32m'
	read miscomitbrowserresp
	if [[ $miscomitbrowserresp =~ ^('yes'|'y')$ ]]
	then
	firefox ${miscomiturlarr[@]}
	fi

	# Add misc hits to blacklist
	#echo -e '\033[1;37m' \\n Add all miscellaneous hits to the blacklist? \\n y/n
	#read miscaddresp
	#if [[ $miscaddresp =~ ^('yes'|'y')$ ]]
	#then
	#echo ${miscomiturlarr[@]} >> ~/code/current/civ_crawl/blacklist
	#fi
fi

fi

## hit count redundant?
# Error logging 
if [[ $errorhitcount -ne 0 ]]
then
printf '%s\n' "${errorlog[@]} Error_hit_count_=_$errorhitcount" >> ~/code/current/civ_crawl/errorlog
fi














