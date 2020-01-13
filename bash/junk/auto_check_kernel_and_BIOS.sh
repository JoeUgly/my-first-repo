#!/usr/bin/env bash
# Description: Check the current and latest kernel, BIOS, and Nano node versions.

kercur=$(uname -r | cut -d \. -f1-2)
kernew=$(curl -s -N https://www.kernel.org/ | awk '/stable/{print$2;}' | sed -n 2p | cut -d v -f2-)
kerres=$(echo $kernew | grep $kercur)

if [[ -z $kerres ]]
then
echo " ---KERNEL---
 --OUTDATED-- Your kernel version = $kercur
 The latest stable kernel version = $kernew
 Download here = http://kernel.ubuntu.com/~kernel-ppa/mainline/" > /home/joe/Desktop/KERNEL_OUTDATED.txt
fi


biocur=$(sudo dmidecode -t bios | awk '/Version/{print $2;}' | cut -c 2-5)
bionew=$(curl -s -N https://www.asrock.com/support/index.asp?cat=BIOS | grep -o 'AB350 Pro4</a></td><td>.....' | cut -d '>' -f4 | cut -c 1-4)
biores=$(echo $bionew | grep $biocur)

if [[ -z $biores ]] && [[ -n $bionew ]]
then
echo " ------BIOS------
 ----OUTDATED---- Your BIOS version = $biocur
 The latest AB350 Pro4 BIOS version = $bionew
 Download here = https://www.asrock.com/mb/AMD/AB350%20Pro4/#BIOS" > /home/joe/Desktop/BIOS_OUTDATED.txt
fi


nodecur=$(ls /home/joe/Downloads/nano | grep rai | cut -c 5-8 | sort -nr | head -n1)
nodenew=$(curl -sL -N https://github.com/nanocurrency/raiblocks/releases/ | grep -o V[0-9][0-9]\.[0-9]*[R]*[C]*[0-9]* | sort | tail -n 1)
noderes=$(echo $nodenew | grep $nodecur)

if [[ -z $noderes ]]
then
echo "------NODE------
 ----OUTDATED---- Your node version = $nodecur
 The latest Nano node version = $nodenew
 Download here = https://github.com/nanocurrency/raiblocks/releases/latest" > /home/joe/Desktop/NANO_OUTDATED.txt
fi
exit
