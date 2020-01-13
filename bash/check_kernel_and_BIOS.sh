#!/usr/bin/env bash

# Description: Checks if kernel, BIOS, and Nano node are up to date.

kercurstrict=$(uname -r | cut -d - -f1)
kercurloose=$(uname -r | cut -d \. -f1-2)
kernew=$(curl -s -N https://www.kernel.org/ | awk '/stable/{print$2;}' | sed -n 2p | cut -d v -f2-)
kerresstrict=$(echo $kernew | grep -w $kercurstrict)
kerresloose=$(echo $kernew | grep -w $kercurloose)
echo
if [[ -n $kerresstrict ]]
then
echo -e '\033[1;36m'--- KERNEL ---
echo Your kernel version = $kercurstrict
echo and it is the latest version
elif [[ -n $kerresloose ]]
then
echo -e '\033[1;33m'----- KERNEL -----
echo --- SLIGHTLY OUTDATED --- Your kernel version = $kercurstrict
echo The latest stable kernel version = $kernew
echo Download here = http://kernel.ubuntu.com/~kernel-ppa/mainline/
elif [[ -z $kerresstrict ]]
then
echo -e '\033[1;31m'--- KERNEL ---
echo -- OUTDATED -- Your kernel version = $kercurstrict
echo The latest stable kernel version = $kernew
echo Download here = http://kernel.ubuntu.com/~kernel-ppa/mainline/
fi
echo
echo -e '\033[1;37m' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo
biocur=$(dmesg | awk '/DMI:/{print $16;}' | cut -c 2-5)
bionew=$(curl -s -N https://www.asrock.com/support/index.asp?cat=BIOS | grep -o 'AB350 Pro4</a></td><td>.....' | cut -d '>' -f4 | cut -c 1-4)
biores=$(echo $bionew | grep $biocur)

if [[ -z $biocur ]]
then
echo -e \\n dmesg failed to yield results. Using dmidecode...
biocur=$(sudo dmidecode -t bios | awk '/Version/{print $2;}' | cut -c 2-5)
biores=$(echo $bionew | grep $biocur)
fi
if [[ -n $biores ]]
then
echo -e '\033[1;36m'------ BIOS ------
echo Your BIOS version = $biocur
echo and it is the latest version 
elif [[ -z $biores ]]
then
echo -e '\033[1;31m'------ BIOS ------
echo ---- OUTDATED ---- Your BIOS version = $biocur
echo The latest AB350 Pro4 BIOS version = $bionew
echo Download here = https://www.asrock.com/mb/AMD/AB350%20Pro4/#BIOS
fi
echo

echo -e '\033[1;37m' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo
nodecur=$(ls ~/Downloads/nano/ | grep nano-node | cut -c 11-14 | sort -nr | head -n1)
nodenew=$(curl -sL -N https://github.com/nanocurrency/raiblocks/releases/ | grep -o V[0-9][0-9][.][0-9]R*C*[0-9]* | sort | tail -n 1)


noderes=$(echo $nodenew | grep $nodecur)

if [[ -n $noderes ]]
then
echo -e '\033[1;36m'----- NODE ------
echo Your Nano node version = $nodecur
echo and it is the latest version 
elif [[ -z $noderes ]]
then
echo -e '\033[1;31m'------ NODE ------
echo ---- OUTDATED ---- Your node version = $nodecur
echo The latest Nano node version = $nodenew
echo Download here = https://github.com/nanocurrency/raiblocks/releases/latest
fi
echo -e '\033[1;32m'


















