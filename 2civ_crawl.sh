#!/usr/bin/env bash
# Description: Searches the provided webpages for keyword and attempts one level of crawling.

# things to do:
# allow for different options with args eg -m or -x keyword portallocation -
# select states and counties
# internet-derived civil service portals
# AND search
# good hits in real time in parent shell
# new easy means of appending to the blacklist

#set -x

function crawler {

let funccount=$funccount+1
#let abscount=$abscount+1
echo -e start crawl level $funccount of $CRAWLLEVELS #\\n abs = $abscount
echo workingurl = $workingurl

## move 'specs' and others earlier in pipe so as to apply to tags also
## can append "cut -d \' -f2" at end to prevent some rare errors. keep eye on this
# Search for job word urls but exclude bunk words
jobwordurlsarr=$(echo "$workingurlcontent" | grep -Po '<a href=.*?</a>' | grep -ie employment -ie job -ie opening -ie exam -ie test -ie postions -ie civil -ie career -ie human -ie personnel | grep -ive ^javascript -ive \.pdf$ -ive \.jpg$ -ive \.ico$ -ive \.doc$ -ive ^mailto: -ive ^tel: -ive description -ive specs -ive specification -ive guide -ive images | cut -d \" -f2 | cut -d \' -f2)

for jobwordurl in ${jobwordurlsarr[@]}
do
#printf '%s\n' jobwordurlsarr_= $jobwordurlsarr

	# Exclude previously checked URLs
	dupcheck=$(printf '%s\n' ${checkedarr[@]} | grep -i "$jobwordurl")
	if [[ -n $dupcheck ]]
	then
	let dupomithitcount=$dupomithitcount+1
	echo dup omitted = $dupcheck
	else

	echo jobwordurl = $jobwordurl
	let totalpages=$totalpages+1

	# Add url to checked array
	#checkedarr+=($jobwordurl)

		## necessary. yes.
		# Create the working url
		if [[ -n $jobwordurl ]]
		then
		echo portal = $portalurl
		domain=$(echo "$portalurl" | cut -d / -f3)
		echo domain = $domain

		# Correct for rel and abs paths
		doublepath=$(echo "$jobwordurl" | grep -i "$domain")

			# If url contains domain then keep orignal
			if [[ -n $doublepath ]]
			then
			workingurl=$jobwordurl
			else
				# If url starts with http then keep the original
				if [[ $jobwordurl =~ ^http ]]
				then
				workingurl=$jobwordurl
				else
				echo corrected \for rel path

					# Prevent triple slash
					if [[ $jobwordurl =~ ^/ ]] && [[ $domain =~ /$ ]]
					then
					echo prevented triple slash
					workingurl0=$(echo $jobwordurl | cut -d / -f2-)
					workingurl=$domain$workingurl0

					# Prevent double slash
					elif [[ $jobwordurl =~ ^/ ]] || [[ $domain =~ /$ ]]
					then
					echo prevented double slash
					workingurl=$domain$jobwordurl

					# Prevent no slashes
					else
					echo prevented no slash
					workingurl=$domain/$jobwordurl
					fi
				fi
			fi
		echo -e workingurl = \"$workingurl\"

		# Exclude previously checked URLs
		dupcheck=$(printf '%s\n' ${checkedarr[@]} | grep -i "$workingurl")
		if [[ -n $dupcheck ]]
		then
		let dupomithitcount=$dupomithitcount+1
		echo dup omitted = $dupcheck
		else

		# Add to checked array
		checkedarr+=($workingurl)

		# Get page contents
		workingurlcontent=$(curl --max-time 10 --retry 1 -sL "$workingurl")
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
				errorlog+=(domain_=_$domain url_=_$workingurl code_=_$errorcode \  )
				fi
			else

			# Add keyword match to array
			additionalmatch=$(echo "$workingurlcontent" | grep -i "$keyword" | cut -c 1-80)
				if [[ -n $additionalmatch ]]
				then
				let hitcount=$hitcount+1
				urlarr+=($workingurl)
				echo -e '\033[1;37m' Found additional item \#$hitcount \\n $additionalmatch
				echo -e '\033[1;36m' \\t $workingurl \\n\\n '\033[0;32m'
				fi
			fi
		fi
		fi

		# Check target level of crawling
		if [[ $funccount -lt $CRAWLLEVELS ]]
		then
		echo starting crawl
		crawler
		fi
	fi
done
echo end of crawl level $funccount of $CRAWLLEVELS
let funccount=$funccount-1

}




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
#abscount=0

# Set args
# Set portal location
#if [[ -n "$2" ]]
#then
portallocation+=$2
echo 1= $1
#else
#portallocation+=~/code/current/civ_crawl/Civil222

echo 2 = $2
echo pl = ${portallocation[@]}
#fi

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
for portalurl in ${portallocation[@]}
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
dupcheck=$(printf '%s\n' "${checkedarr[@]}" | grep -i "$portalurl")
	if [[ -n $dupcheck ]]
	then
	let dupomithitcount=$dupomithitcount+1
	echo dup omitted = $dupcheck
	else
	
	# Curl portal page
	portalurlcontent=$(curl --max-time 10 --retry 1 -sL "$portalurl")
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
			errorlog+=(portal_url_=_"$portalurl" code_=_$errorcode \  )
			fi
		else

		# Search for keyword on portal page
		keywordmatch=$(echo "$portalurlcontent" | grep -ie "$keyword" | cut -c 1-80)

		# Add to checked array
		checkedarr+=($portalurl)

			# If found keyword match
			if [[ -n $keywordmatch ]]
			then

			# Add match to array
			let hitcount=$hitcount+1
			urlarr+=($portalurl)
			echo -e '\033[1;37m' Found item \#$hitcount 
			echo -e $keywordmatch \\n '\033[1;36m' \\t $portalurl \\n\\n '\033[0;32m'
			fi
		fi
	
workingurl="$portalurl"
workingurlcontent="$portalurlcontent"

		# Check target level of crawling
		if [[ $funccount -lt $CRAWLLEVELS ]]
		then
		echo starting crawl
		crawler
		fi
	fi
done


# Write parellelization results and stats
#if [[ -n $2 ]]
#then
duration=$(( SECONDS - start ))
echo -e \\n\\n block number xxxxxxxxx \\n Total pages searched = $totalpages \\n Total omitted duplicate hits = $dupomithitcount \\n Duration = $duration seconds \\n Total good hits = $hitcount \\n ${urlarr[@]} >> /home/joepers/code/current/civ_crawl/results



# Error logging 
if [[ $errorhitcount -ne 0 ]]
then
printf '%s\n' "${errorlog[@]} Error_hit_count_=_$errorhitcount" >> ~/code/current/civ_crawl/errorlog
fi










