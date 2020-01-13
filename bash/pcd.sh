#!/usr/bin/env bash

# Description: Probe a video file to see if it's playable, convert it if not, and mark the original for deletion.
# Works on directories and files. Files matching wildcards don't work.


# To do:
# containers allow diff codecs
# dont attempt convert dirs +
# check all audio and subtitle files, not just first
# always change to .mkv
# remove copy to USB. leave it. it only asks when the drive is plugged in
# can batch and force conversion be merged?

# dir inside another dir. Sometimes parent dir is not descriptive. eg: /Season_1/. Sometimes need to use parent of parent. eg: /Mr_Robot/Season_1/
# abs path to pcd_delete_these. This will leave empty dirs. I could scan for very small dirs or dirs with no video files and delete them too +
# search every dir in /tor/, check cumulative file size, and delete if less than ~ 20MB
# eg: for i in $(du /home/joepers/Desktop/torrents/); do if [[ $(echo "$i" | awk '// {print $1;}') -lt 20000 ]]; then echo "$i"; fi; done

# client not using file name +
# Delete name of audio and subtitle tracks so client is forced to use filename
# only delete if track contains 'name'?
# mkvpropedit "rep-starwarstheforceawakens.1080p.bluray.x264.mkv" --edit track:3 -d name







## diff containers have diff codec lists
: '
MKV
    Video: H.264/MPEG-4 AVC High Profile Level 4.2
    Audio: MP3, AAC LC, AC-3 (Dolby Digital)

AVI
    Video: MPEG4 ASP, H.264/MPEG-4 AVC High Profile Level 4.2
    Audio: MP3, AAC LC, AC-3 (Dolby Digital)

MP4
    Video: H.264/MPEG-4 AVC High Profile Level 4.2, H.264/MPEG-4 AVC High Profile Level 5.2 (PlayStation®4 Pro only)
    Audio: AAC LC, AC-3 (Dolby Digital), LPCM
'




cd /mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/tors

# Set IFS to newline to help ls output
IFS=$'\n'


# Use this to append filenames to pcd_delete_these
converted_something=False


## can this be merged with batch_resp? I think so
# Force conversion even when conversion is deemed unnecessary
if [[ $1 == '--force' ]]
then

    # Force audio conversion
    if [[ $2 == 'a' ]]
    then
    force_a=True
    batch_resp=True

    # Use third arg as filename
    file_resp=$3
    echo -e \\n Forcing audio conversion

    # Force video conversion
    elif [[ $2 == 'v' ]]
    then
    force_v=True
    batch_resp=True
    file_resp=$3
    echo -e \\n Forcing video conversion

    # Force aud and vid conversion
    elif [[ $2 == 'av' ]]
    then
    force_av=True
    batch_resp=True
    file_resp=$3
    echo -e \\n Forcing audio and video conversion

    # Exit if audio or video is not specified
    else
    echo -e \\n You must specify audio, video, or both when using forced conversions.\\n e.g.: pcd --force v \<input file\>
    exit

    fi

# Use argument if one is present
elif [[ -n $1 ]]
then
file_resp=$1

# Prompt for file if no args are present
else

# Display most recent files
for i in $(ls -t | head -n 10)
do 
echo -e "$i"
done

echo -e \\n\\n Enter file
read file_resp

# Use most recent torrent if one is not specified
if [[ -z "$file_resp" ]]
then
file_resp=$(ls -t /mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/tors | head -n 1)

# Prefix absolute path
file_resp=/mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/tors/"$file_resp"



## this will conflict with multi file. it's only used with empty response
# Use largest file in the dir if file_resp is a directory
: '
if [[ -d "$file_resp" ]]
then
file=$(cd "$file_resp" && ls -S | head -n 1)
file_resp="$file_resp"/"$file"
echo "$file_resp" | cut -d / -f6-
fi
'

fi
fi


# Get parent dir for pcd_delete_these
if [[ -d "$file_resp" ]]
then

    # Remove trailing slash because it messes up the forward slash split for par_dir. Prefix it with abs path
    last_char=${file_resp:(-1):1}
    if [[ "$last_char" == '/' ]]
    then

    ## don't assume this prefix. Sometimes par_dir is inside a dir. eg: par_dir = /Season_1/
    par_dir=/mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/tors/$(echo "$file_resp" | rev | cut -c 2- | cut -d / -f1 | rev)

    # Split file_resp by last forward slash to form par_dir and prefix with abs path
    else
    par_dir=/mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/tors/$(echo "$file_resp" | rev | cut -d / -f1 | rev)
    fi

else
par_dir="$file_resp"
fi

echo -e \\n file_resp: "$file_resp"\\n par_dir: "$par_dir"

# For loop will work on multiple files in a dir or a single file as file_resp
for each_file in $(find "$file_resp" -type f)
do

## This can cause double slashes. No errors are thrown.
# Prefix path if file_resp is a directory --
if [[ -d "$file_resp" ]]
then
echo -e \\n file_resp is a directory.
each_file="$each_file"
fi



# Check if file exists
if [[ -e "$each_file" ]]
then
echo -e \\n\\n ~~~  File found.  ~~~
echo -e "$each_file" \\n

else
echo -e \\n ~~~  Cannot find file.  ~~~
echo -e "$each_file" \\n
exit
fi



# Get container
filename=$(basename -- "$each_file")
extension="${filename##*.}"

## probably should have listed good extenions instead
# Skip non-video files
if [[ $extension = 'txt' ]] || [[ $extension = 'srt' ]] || [[ $extension = 'jpg' ]] || [[ $extension = 'sub' ]] || [[ $extension = 'nfo' ]] || [[ $extension = 'idx' ]] || [[ $extension = 'png' ]] || [[ $extension = 'JPG' ]] || [[ $extension = 'sfv' ]] 
then
echo Skipping "$each_file"
continue
fi

# Set good containers
good_containers=("mkv" "mp4" "avi")
con_check=Bad

# Check container
for i in ${good_containers[@]}
do
    if [[ "$i" = "$extension" ]]
    then
    con_check=Good
    fi
done
echo Container: "$extension" \("$con_check"\)



# Get video codec
v_codec=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name   -of default=noprint_wrappers=1:nokey=1 "$each_file")

# Set good video codecs
good_v_codecs=("h264" "mpeg4")
vid_check=Bad

# Check video codec
for i in ${good_v_codecs[@]}
do
    if [[ $i = "$v_codec" ]]
    then
    vid_check=Good
    fi
done

# Check profile level
if [[ $v_codec = "h264" ]] || [[ $v_codec = "mpeg4" ]]
then
profile_level=$(ffprobe -v error -select_streams v:0 -show_entries stream=level -of default=noprint_wrappers=1 "$each_file" | cut -d = -f2)
    if [[ $profile_level -gt 42 ]] || [[ $profile_level -lt 0 ]]
    then
    vid_check="Bad"
    fi
fi

echo -e Video codec: "$v_codec" \("$vid_check"\) \\nProfile level: "$profile_level"



# Get audio codec
a_codec=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name   -of default=noprint_wrappers=1:nokey=1 "$each_file")

# Set good audio codecs
good_a_codecs=("aac" "ac3" "mp3")
aud_check=Bad

# Check audio codec
for i in ${good_a_codecs[@]}
do
    if [[ $i = "$a_codec" ]]
    then
    aud_check=Good
    fi
done

echo Audio codec: "$a_codec" \("$aud_check"\)





# Bad audio
if [[ "$aud_check" = "Bad" ]] && [[ "$vid_check" = "Good" ]] || [[ "$force_a" = "True" ]]
then

# Check and use batch response
if [[ $batch_resp = "True" ]]
then
aud_conv_resp=yes
else

# Prompt for audio conversion
echo -e \\n Convert audio with video passthrough?
read aud_conv_resp
fi

# Convert audio with video passthrough
if [[ $aud_conv_resp =~ ^('yes'|'y'|'yall'|'yesall')$ ]]
then
ffmpeg -i "$each_file" -c:v copy -c:a ac3 -b:a 512k -ac 2 -c:s copy /mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/converted_vids/"$filename"

echo -e \\n Conversion complete.
converted_something=True
fi




# Bad video
elif [[ "$aud_check" = "Good" ]] && [[ "$vid_check" = "Bad" ]] || [[ "$force_v" = "True" ]]
then

# Check and use batch response
if [[ $batch_resp = "True" ]]
then
vid_conv_resp=yes
else

# Prompt for video
echo -e \\n Convert video with audio passthrough?
read vid_conv_resp
fi

# Convert video with audio passthrough
if [[ $vid_conv_resp =~ ^('yes'|'y'|'yall'|'yesall')$ ]]
then
ffmpeg -i "$each_file" -c:v libx264 -profile:v high -level 4.2 -c:a copy -c:s copy /mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/converted_vids/"$filename"

echo -e \\n Conversion complete.
converted_something=True
fi




# Bad audio and video
elif [[ "$aud_check" = "Bad" ]] && [[ "$vid_check" = "Bad" ]] || [[ "$force_av" = "True" ]]
then

# Check and use batch response
if [[ $batch_resp = "True" ]]
then
av_conv_resp=yes
else

# Prompt for audio and video
echo -e \\n Convert audio and video?
read av_conv_resp
fi

# Convert video and audio
if [[ $av_conv_resp =~ ^('yes'|'y'|'yall'|'yesall')$ ]]
then
ffmpeg -i "$each_file" -c:v libx264 -profile:v high -level 4.2 -c:a ac3 -b:a 512k -ac 2 -c:s copy /mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/converted_vids/"$filename"

echo -e \\n Conversion complete.
converted_something=True
fi





# Bad container
elif [[ "$aud_check" = "Good" ]] && [[ "$vid_check" = "Good" ]] && [[ "$con_check" = "Bad" ]]
then

# Check and use batch response
if [[ $batch_resp = "True" ]]
then
con_conv_resp=yes
else

# Prompt for container
echo -e \\n Convert to .mkv container?
read con_conv_resp
fi

# Just change the container
if [[ $con_conv_resp =~ ^('yes'|'y'|'yall'|'yesall')$ ]]
then

## this didn't work with: -ac 2 -c:s copy
## extension?
ffmpeg -i "$each_file" -c:v copy -c:a copy -ac 2 -c:s copy /mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/converted_vids/"$filename".mkv
echo -e \\n Conversion complete.
converted_something=True
fi


fi


# Set batch response
if [[ $aud_conv_resp =~ ^('yall'|'yesall')$ ]] || [[ $vid_conv_resp =~ ^('yall'|'yesall')$ ]] || [[ $av_conv_resp =~ ^('yall'|'yesall')$ ]] || [[ $con_conv_resp =~ ^('yall'|'yesall')$ ]]
then
batch_resp=True
echo -e \\n Batch response is being used. \\n
fi

echo -e \\n\\n




# Delete name of audio and subtitle tracks in metadata so client is forced to use filename
mkvpropedit -q "$each_file" --edit track:2
mkvpropedit -q "$each_file" --edit track:3

# Sometimes the client will read segment info, not track info
mkvpropedit -q "$each_file" --edit info --delete "title"


done



# Append parent dir to text file so I know to delete the original later
if [[ $converted_something = True ]]
then
echo "$par_dir" >> ~/code/bash/pcd_delete_these
echo -e \\n Added to pcd_delete_these:\\n "$par_dir"







# Check if Corsair drive is present
if [[ -d /media/joepers/Corsair_128/Video/ ]]
then

# Prompt to copy
echo -e \\n\\n Copy to /media/joepers/Corsair_128/Video/ ?
read copy_resp

# Copy to USB
if [[ $copy_resp =~ ^('yes'|'y')$ ]]
then
rsync --progress -ruv "/mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/converted_vids/$filename" /media/joepers/Corsair_128/Video/
fi

fi

fi






















