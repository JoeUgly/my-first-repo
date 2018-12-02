#!/usr/bin/env bash
# Description: Prepare civ_crawl for parallel operation

# to do: 
# dont write blocks to disk -
# additional arg options
	# AND search - curl the domain from each hit and use as portals for second keyword search
# smart way of sorting multiple url results from a domain based on quality
# remove .doc results


# Estimated time to completion
prevduration=$(cat ~/code/current/civ_crawl/duration)
prevshellnum=$(cat ~/code/current/civ_crawl/shellnum)
prevnumofpages=$(cat ~/code/current/civ_crawl/numberofpages)
prevdupomithitcount=$(cat ~/code/current/civ_crawl/dupomithitcount)
ppspsprev=$(cat ~/code/current/civ_crawl/ppsps)
shelltime=$(bc <<< "$prevduration * $prevshellnum" | cut -d \. -f1)




echo -e \\n Enter the State \"-s\" \for multiple States, or \"-f\" \for local NY file. #Use an underscore instead of a space. eg new_york
read state

# Multiple states
if [[ $state =~ "-s" ]]
then
	while [[ $state != "end" ]]
	do
		if [[ -z ${statearr[@]} ]]
		then
		echo -e \\n Enter first State
		read state
			if [[ $state != "end" ]]
			then
			statearr+=($state)
			fi
		else
		echo -e \\n Enter next State or \"end\"
		read state
			if [[ $state != "end" ]]
			then
			statearr+=($state)
			fi
		fi
	done
elif [[ $state =~ "-f" ]]
then
statearr=$(cat ~/code/current/civ_crawl/civil_ny)
else
statearr+=("$state")
fi

# Use local file to get county urls
if [[ $state =~ "-f" ]]
then
countyurlarr="$statearr"

# Use internet to get county urls
else
echo -e \\n Retrieving county websites ... \\n

# Get relative wiki county url
for eachstate in ${statearr[@]}
do
relwikicountyurlarr+=$(curl -s https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents | grep -ioe href=\"/wiki/.*,_$eachstate\" | cut -d \" -f2)

# Get absolute wiki county url
for eachcountyurl in $relwikicountyurlarr
do
abswikicountyurl=https://en.wikipedia.org$eachcountyurl

# Get county url
countyurl=$(curl -s $abswikicountyurl | grep -A 1 Website | grep -o \"http.* | head -n 1 | cut -d \" -f2- | cut -d \" -f1)

#countyurlarr=$(grep -ao https*.* $portallocation | cut -d \" -f1 | cut -f1 -d$'\t') 
countyurlarr+=($countyurl)

echo $countyurl

done
done
fi



# Enter keyword
echo -e \\n Enter search string or \"-m\" \for multiple search strings
read keyword

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

# Set number of subshells
echo -e \\n Estimated number of pages to search = $prevnumofpages
echo -e \ Estimated number of pages searched per second per subshell = $ppspsprev \\n
echo -e \\n Enter number of subshells to run
read shellnum

urlnum=$(printf '%s\n' ${countyurlarr[@]} | wc -l)
BLOCKSIZE=$(expr $urlnum / $shellnum + 1)
echo -e \\n Number of portal URLs per subshell = $BLOCKSIZE
echo \ Estimated time to completion = $(bc <<< "$prevnumofpages/($ppspsprev*$shellnum)") seconds

# Set number of levels to crawl
echo -e \\n\\n Enter number of levels to crawl
read CRAWLLEVELS







blockcount=0
parallelcount0=1
parallelcount1=$BLOCKSIZE
parallelblock=x

# Remove previous results
rm /home/joepers/code/current/civ_crawl/results 
if [ -f ~/code/current/civ_crawl/errorlog ]; then
rm ~/code/current/civ_crawl/errorlog
fi

# Create blocks of portal URLs 
while [[ -n $parallelblock ]]
do
parallelblock=$(printf '%s\n' ${countyurlarr[@]} | sed -n ${parallelcount0},${parallelcount1}p)
#printf '%s\n' pb = ${parallelblock[@]}

#echo "$parallelblock" > ~/code/current/civ_crawl/block$blockcount

# Call subshells to run each block until all blocks are assigned
export BLOCKSIZE
export CRAWLLEVELS

	if [[ -n $parallelblock ]]
	then
	x-terminal-emulator -e ~/code/2civ_crawl.sh "$keyword" "$parallelblock"
	let blockcount=$blockcount+1
	let parallelcount0=$parallelcount0+$BLOCKSIZE
	let parallelcount1=$parallelcount1+$BLOCKSIZE
	fi
done

# Wait for all subshell results to be posted
alldone=0
echo -e \\n\\n Waiting \for subshells to finish... \\n
echo a > /home/joepers/code/current/civ_crawl/results

while [[ $alldone1 -ne $blockcount ]]
do
	if [[ $alldone0 -ne $alldone1 ]]
	then
	alldone0=$alldone1
	echo Progress = $alldone0 of $blockcount
	fi
sleep 2
alldone1=$(cat /home/joepers/code/current/civ_crawl/results | grep -o "block number xxxxxxxxx" | uniq -c | awk '// {print $1;}')
done
echo -e ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '\033[1;36m' \\n

# Collect results
totpagesearch=$(cat /home/joepers/code/current/civ_crawl/results | awk '/Total pages searched = / {print $5;}' | paste -sd+ | bc)
totdupomithitcount=$(cat /home/joepers/code/current/civ_crawl/results | awk '/Total omitted duplicate hits = / {print $6;}' | paste -sd+ | bc)
longduration=$(cat /home/joepers/code/current/civ_crawl/results | awk '/Duration = [0-9]* / {print $3;}' | sort | tail -n 1)
tothits=$(cat /home/joepers/code/current/civ_crawl/results | awk '/Total good hits = [0-9]* / {print$5;}' | paste -sd+ | bc)
toturls=$(cat /home/joepers/code/current/civ_crawl/results | grep '\.')

# Display and write results and stats
printf '%s\n' $toturls | sort

echo -e \\n '\033[1;32m'Total good hits \for \"$keyword\" = $tothits

echo -e \ Total pages searched = $totpagesearch
bc <<< "scale=2; ($prevnumofpages + $totpagesearch) / 2" > ~/code/current/civ_crawl/numberofpages

echo -e \ Total omitted duplicate hits = $totdupomithitcount
bc <<< "scale=2; ($prevnumofpages+$totdupomithitcount)/2" > ~/code/current/civ_crawl/dupomithitcount

echo -e \ Duration = $longduration seconds
bc <<< "scale=2; ($longduration + $prevduration) / 2" > ~/code/current/civ_crawl/duration

ppspsnew=$(bc <<< "scale=2; ($totpagesearch / $longduration) / $shellnum")

bc <<< "scale=2; ($ppspsnew + $ppspsprev) / 2" > ~/code/current/civ_crawl/ppsps

echo -e \ Average PPSPS = $ppspsprev \\n This PPSPS = $ppspsnew

echo $shellnum > ~/code/current/civ_crawl/shellnum

errorlognum=$(grep -o Error_hit_count_=_[0-9]* ~/code/current/civ_crawl/errorlog | cut -d _ -f5 | paste -sd+ | bc)
echo -e \ Number of cURL errors = $errorlognum \\n

# Open hits in browser
if [[ $tothits -ne 0 ]]
then
	echo -e '\033[1;37m' \\n Open $tothits good hits in browser? \\n y/n
	read resp0
	echo -e '\033[0;32m'
	if [[ $resp0 =~ ^('yes'|'y')$ ]]
	then
	firefox $toturls
	fi
fi

# Collect and display error results
errorlogresults=$(grep -o url_=_.* ~/code/current/civ_crawl/errorlog | cut -d _ -f3- | cut -d ' ' -f1)

echo -e '\033[1;32m'
printf '%s\n' "$errorlogresults" | sort | uniq
echo -e \\n ~~~ cURL errors ~~~
echo -e \ \ Freq \| Exit code
grep -o code_=_[0-9]* ~/code/current/civ_crawl/errorlog | cut -d _ -f3 | sort -g | uniq -c | sort -gr

# Open error URLs in browser
echo -e '\033[1;37m' \\n Open $errorlognum error URLs in browser? \\n y/n
read resp0
echo -e '\033[0;32m'
if [[ $resp0 =~ ^('yes'|'y')$ ]]
then
firefox $errorlogresults
fi
















