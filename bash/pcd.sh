#!/usr/bin/env bash

# Description: Probe a video file to see if it's playable on the PS4, convert it if necessary, and mark the original for deletion.
# Works using a directory or a file. Files matching wildcards don't work.
# Takes first vid and all aud and subtitle streams. When converting aud, then only first aud stream.


# To do:
# containers allow diff codecs
# back to 1 pass aud norm?
# compare speed of aac and ac3
# option for force container conversion
# inaccurate target lra
# fatal subtitle error when converting container. check with ubuntu
# sometimes mp4s dont play. fixed with video conversion. why tho?
# sometimes dts will play
# move good codecs to top?
# optional loudnorm? force loudnorm arg?
# mark partially converted dirs? - no just append each file
# -pix_fmt yuv420p - what about it?
# formatting is wrong when displaying multiple aud codecs








## diff containers have diff codecs
: '
MKV
    Video: H.264/MPEG-4 AVC High Profile Level 4.2
    Audio: MP3, AAC LC, AC-3 (Dolby Digital)

AVI
    Video: MPEG4 ASP, H.264/MPEG-4 AVC High Profile Level 4.2
    Audio: MP3, AAC LC, AC-3 (Dolby Digital)

MP4
    Video: H.264/MPEG-4 AVC High Profile Level 4.2, H.264/MPEG-4 AVC High Profile Level 5.2 (PlayStation®4 Pro only)
    Audio: AAC LC, AC-3 (Dolby Digital), ,
'




# Get the vars to use 2 pass volume normalization
function two_pass_f {

    # Redirect file descriptor 5 to stdout. This will allow duplication later
    exec 5>&1

    # First pass loudnorm and extract JSON object. Output to null because I only want the aud stats. Redirect stderr to stdout because ffmpeg uses stderr for its default output. Split the output to stdout (saved as var) and file descriptor 5 (which is redirected to stdout because of exec 5>&1 and therefore actually displayed on console). Select the JSON object by greping the squiggly bracket. Save that as var.
    json_list=$( (ffmpeg -hide_banner -i "$each_file" -map 0:v -map 0:a -map 0:s? -c:v copy -c:a ac3 -b:a 32k -ac 2 -af loudnorm=print_format=json -ar 48k -c:s copy -f null -) 2>&1 | tee /dev/fd/5 | grep -A 11 {)
    
    # Close file descriptor 5
    exec 5>&-

    # Get loudnorm input measurements from first pass
    i_i=$(echo "$json_list" | jq -r '."input_i"')
    i_tp=$(echo "$json_list" | jq -r '."input_tp"')
    i_lra=$(echo "$json_list" | jq -r '."input_lra"')
    i_thr=$(echo "$json_list" | jq -r '."input_thresh"')

    echo -e \\n measured_I=$i_i\\n measured_TP=$i_tp\\n measured_LRA=$i_lra\\n measured_thresh=$i_thr

    # Set TP to -2 or original if lower
    if [[ (($i_tp < -2)) ]]; then
    o_tp=$i_tp
    else
    o_tp=-2.0
    fi
    echo Output TP = $o_tp
}





cd ~/Videos/tors

# Set IFS to newline to help ls output
IFS=$'\n'


# Place converted files into array to check if all convertable files in dir have been converted
converted_files=()

# Set default arg values
force_opt=false
verb_opt=false




## check if any args are present?

# Loop through args using $1 because $i doesn't work with shift
while true; do

    # case is basically an if statment with only one match
    case "$1" in

    # Verbose arg
    -v)
        verb_opt=true
        ;;

    # Force conversion args
    --force)

        # Select next arg to determine what to force convert
        shift

        [[ $1 = 'a' ]] && force_opt=aud
        [[ $1 = 'v' ]] && force_opt=vid
        [[ $1 = 'av' ]] && force_opt=both

        # Catch and exit on invalid force args
        [[ ! $1 =~ ^(a|v|av)$ ]] && {
            echo -e \\n Invalid argument:
            echo -e Must specify \"a\", \"v\", or \"av\" after \"--force\" \\n
            exit 1
        }

        # Suppress prompt when any force option is invoked
        batch_resp=True
        ;;

    # There is always an extra empty arg. Use this to mark end of loop
    '')
        break
        ;;

    # All other args will be treated as file_resp input
    *)
        file_resp=$1
        ;;

    esac

# Select next arg to continue loop using $1 instead of $i. ie: next arg in loop becomes $1
shift

done


# Display options
echo
$verb_opt && echo Verbose option invoked
if [[ ! "$force_opt" == "false" ]]; then echo Force conversion: $force_opt; fi
echo


# Prompt for file if file resp has not yet been set
if [[ -z $file_resp ]]; then

    # Display most recent files
    for i in $(ls -t | head -n 14); do 
    echo -e "$i"
    done

echo -e \\n\\n Enter a file
read file_resp

    # Use most recent file if one is not specified
    if [[ -z "$file_resp" ]]; then
    file_resp=~/Videos/tors/$(ls -t ~/Videos/tors | head -n 1)
    fi


fi


# Exit if file_resp doesn't exist as file or dir
if [[ ! -e "$file_resp" ]]; then
echo -e \\n File not found. Exiting ...
exit 1
fi


# Get parent dir for pcd_delete_these
if [[ -d "$file_resp" ]]; then

    : '
    # Remove trailing slash because it messes up the forward slash split for par_dir. Prefix it with abs path
    last_char=${file_resp:(-1):1}
    if [[ "$last_char" == "/" ]]; then

    ## dont assume this prefix. Sometimes par_dir is inside a dir. eg: par_dir = /Season_1/
    par_dir=~/Videos/tors/$(echo "$file_resp" | rev | cut -c 2- | cut -d / -f1 | rev)

    # Split file_resp by last forward slash to form par_dir and prefix with abs path
    else
    par_dir=~/Videos/tors/$(echo "$file_resp" | rev | cut -d / -f1 | rev)
    fi
    '

    # file resp path is abs if first character is forward slash
    first_char=${file_resp:0:1}
    if [[ "$first_char" == "/" ]]; then
    par_dir="$file_resp"

    # Change from rel to abs path using default location
    else
    par_dir=~/Videos/tors/"$file_resp"
    fi



else
par_dir="$file_resp"
fi

echo -e \\n file_resp: "$file_resp"\\n par_dir: "$par_dir" \\n


## This can cause double slashes. No errors are thrown.
# Prefix path if file_resp is a directory --
if [[ -d "$file_resp" ]]; then
echo -e \\n file_resp is a directory\\n
each_file="$each_file"
fi




# This loop will work on multiple files in a dir or a single file
for each_file in $(find "$file_resp" -type f | sort)
do


## convert to lowercase? extension=$(echo "$a" | tr '[:upper:]' '[:lower:]')
# Get filename without path and extension
filename=$(basename -- "$each_file")
extension="${filename##*.}"

# Replace file extension with .mkv
filename=${filename%.*}.mkv



    ## probably should have listed good extenions instead. - no, then weird file formats won't be converted
    # Skip non-video files
    if [[ "$extension" =~ ^('txt'|'srt'|'jpg'|'sub'|'nfo'|'idx'|'png'|'JPG'|'sfv'|'exe')$ ]]; then

    # Print skip message if verbose
    "$verb_opt" && {
    echo -e \\n\\n "$each_file"
    echo Skipping non A/V file ...

    converted_files+=("$each_file") # Pass thru nonconvertible files

    }

    # Skip to next file
    continue

    # Print file name if in a dir
    else
        if [[ -d "$file_resp" ]]; then
        echo -e \\n\\n\\n ~~~  File found  ~~~
        echo -e "$each_file" \\n
        fi

    fi




# Get video and audio JSON info
probe_v_j=$(ffprobe -v quiet -print_format json -show_format -show_streams -select_streams v "$each_file")
probe_a_j=$(ffprobe -v quiet -print_format json -show_format -show_streams -select_streams a "$each_file")


# Set good containers
#good_containers=("mkv" "mp4" "avi")
good_containers=("matroska,webm" "avi" "mov,mp4,m4a,3gp,3g2,mj2")
con_check=Bad


# Check container
container=$(echo "$probe_v_j" | jq -r '.format.format_name')

for i in ${good_containers[@]}
do
    if [[ "$i" = "$container" ]]; then
    con_check=Good
    fi
done







# Get video codec
v_codec=$(echo "$probe_v_j" | jq -r '.streams[0].codec_name')

# Set good video codecs
good_v_codecs=("h264" "mpeg4")
vid_check=Bad

# Check video codec
for i in ${good_v_codecs[@]}
do
    if [[ $i = "$v_codec" ]]; then
    vid_check=Good
    fi
done

# Get profile level
profile_level=$(echo "$probe_v_j" | jq -r '.streams[0].level')
pro_check=N/A

# Change level 5 to 50
if [[ $profile_level -eq 5 ]]; then
profile_level=50
fi

# Check profile level
if [[ $profile_level -le 42 ]] && [[ $profile_level -gt 0 ]]; then
pro_check=Good
else
pro_check=Bad
fi






# Get audio codecs as array
a_codecs=$(echo "$probe_a_j" | jq -r '.streams[].codec_name')


# Get audio sample rate for loudnorm
sample_rate=$(echo "$probe_a_j" | jq -r '.streams[0].sample_rate')

# Set sample rate to default if not a number
if [[ ! $sample_rate =~ ^[0-9]+$ ]]; then
sample_rate=48000
echo Invalid sample rate. Using default ...
fi
echo aud sample rate = $sample_rate


# Get audio bitrate
aud_bitrate=$(echo "$probe_a_j" | jq -r '.streams[0].bit_rate')
echo aud bitrate = $aud_bitrate

# Set bitrate to default if not a number
if [[ ! $aud_bitrate =~ ^[0-9]+$ ]]; then
aud_bitrate=448k
echo Invalid bitrate. Using default ...

# Increase bitrate by 20% if less than default to preserve quality
else

    if [[ $aud_bitrate -lt 448000 ]]; then
    aud_bitrate=$(echo "$aud_bitrate * 1.2" | bc)
    fi

fi
echo aud bitrate = $aud_bitrate


# Set good audio codecs
good_a_codecs=("aac" "ac3" "mp3")
aud_check=Bad

# Check audio codec
for i in ${good_a_codecs[@]}; do
    for ii in ${a_codecs[@]}; do
        if [[ "$i" = "$ii" ]]; then
        aud_check=Good
        break
        fi
    done
done


echo -e \\n\\nContainer:\\t "$container" \("$con_check"\)
echo -e Video codec:\\t "$v_codec" \("$vid_check"\)
echo -e Profile level:\\t "$profile_level" \("$pro_check"\)
echo -e Audio codec:\\t "$a_codecs" \("$aud_check"\) \\n


# Piggyback profile check onto vid check to convert vid
if [[ "$pro_check" = Bad ]]; then
vid_check=Bad
fi




# Bad audio
if [[ "$force_opt" = "aud" ]] || { [[ "$force_opt" == "false" ]] && [[ "$aud_check" = "Bad" ]] && [[ "$vid_check" = "Good" ]]; }; then

    # Check and use batch response
    if [[ $batch_resp = "True" ]]; then
    aud_conv_resp=yes
    else

    # Prompt for audio conversion
    echo -e \\n Convert audio with video passthrough?
    read aud_conv_resp
    fi

    # Convert audio with video passthrough
    if [[ $aud_conv_resp =~ ^('yes'|'y'|'yall')$ ]]; then

    # Perform first pass of loudnorm and get aud stats
    two_pass_f

        # Check if volume normalization is necessary
        if [[ (($i_lra > 18)) ]]; then

        # Second pass loudnorm
        ffmpeg -hide_banner -i "$each_file" -map 0:v -map 0:a -map 0:s? -c:v copy -c:a ac3 -b:a $aud_bitrate -ac 2 -af loudnorm=measured_I=$i_i:measured_TP=$i_tp:measured_LRA=$i_lra:measured_thresh=$i_thr:I=$i_i:TP=$o_tp:LRA=10.00:linear=false:print_format=json -ar "$sample_rate" -c:s copy -f matroska ~/Videos/converted_vids/"$filename"
        ff_ec=$?

        # No loudnorm
        else
        ffmpeg -hide_banner -i "$each_file" -map 0:v -map 0:a -map 0:s? -c:v copy -c:a ac3 -b:a $aud_bitrate -ac 2 -c:s copy -f matroska ~/Videos/converted_vids/"$filename"
        ff_ec=$?

        fi

        # Successful conversion
        if [[ "$ff_ec" -eq 0 ]]; then
        converted_files+=("$each_file") # Add converted file to array
        echo -e \\n Conversion complete.
        else
        echo -e \\n\\n ========= Conversion failed. ========= \\n\\n
        fi

    fi



# Bad video
elif [[ "$force_opt" = "vid" ]] || { [[ "$force_opt" == "false" ]] && [[ "$aud_check" = "Good" ]] && [[ "$vid_check" = "Bad" ]]; }; then

    # Check and use batch response
    if [[ $batch_resp = "True" ]]; then
    vid_conv_resp=yes
    else

    # Prompt for video
    echo -e \\n Convert video with audio passthrough?
    read vid_conv_resp
    fi

    # Convert video with audio passthrough
    if [[ $vid_conv_resp =~ ^('yes'|'y'|'yall')$ ]]; then
    ffmpeg -hide_banner -i "$each_file" -map 0:v -map 0:a? -map 0:s? -c:v libx264 -preset slow -crf 19 -profile:v high -level 4.2 -c:a copy -c:s copy -f matroska ~/Videos/converted_vids/"$filename"
    ff_ec=$?
    echo -e \\n Conversion complete.

        if [[ "$ff_ec" -eq 0 ]]; then converted_files+=("$each_file"); fi

    fi




# Bad audio and video
elif [[ "$force_opt" = "both" ]] || { [[ "$force_opt" == "false" ]] && [[ "$aud_check" = "Bad" ]] && [[ "$vid_check" = "Bad" ]]; }; then

    # Check and use batch response
    if [[ $batch_resp = "True" ]]; then
    av_conv_resp=yes
    else

    # Prompt for audio and video
    echo -e \\n Convert audio and video?
    read av_conv_resp
    fi

    # Convert video and audio
    if [[ $av_conv_resp =~ ^('yes'|'y'|'yall')$ ]]; then

    # Perform first pass of loudnorm and get aud stats
    two_pass_f

        # Check if volume normalization is necessary
        if [[ (($i_lra > 18)) ]]; then

        ffmpeg -hide_banner -i "$each_file" -map 0:v -map 0:a -map 0:s? -c:v libx264 -preset medium -crf 19 -profile:v high -level 4.2 -c:a aac -b:a 448k -ac 2 -af loudnorm=measured_I=$i_i:measured_TP=$i_tp:measured_LRA=$i_lra:measured_thresh=$i_thr:I=$i_i:TP=$o_tp:LRA=10.00:linear=false:print_format=json -ar "$sample_rate" -f matroska ~/Videos/converted_vids/"$filename"
        ff_ec=$?
        echo -e \\n Conversion complete.

        if [[ "$ff_ec" -eq 0 ]]; then converted_files+=("$each_file"); fi
        
        # No loudnorm
        else
        ffmpeg -hide_banner -i "$each_file" -map 0:v -map 0:a -map 0:s? -c:v libx264 -preset medium -crf 19 -profile:v high -level 4.2 -c:a aac -b:a 448k -ac 2 -f matroska ~/Videos/converted_vids/"$filename"
        ff_ec=$?
        echo -e \\n Conversion complete.

        if [[ "$ff_ec" -eq 0 ]]; then converted_files+=("$each_file"); fi
        
        fi

    fi




# Bad container
elif [[ "$aud_check" = "Good" ]] && [[ "$vid_check" = "Good" ]] && [[ "$con_check" = "Bad" ]]; then

    # Check and use batch response
    if [[ $batch_resp = "True" ]]; then
    con_conv_resp=yes
    else

    # Prompt for container
    echo -e \\n Convert to .mkv container?
    read con_conv_resp
    fi

    # Just change the container
    if [[ $con_conv_resp =~ ^('yes'|'y'|'yall')$ ]]; then

    ## this didn't work with -c:s copy
    ffmpeg -hide_banner -i "$each_file" -map 0:v -map 0:a? -map 0:s? -c:v copy -c:a copy -f matroska ~/Videos/converted_vids/"$filename"
    ff_ec=$?
    echo -e \\n Conversion complete.

        if [[ "$ff_ec" -eq 0 ]]; then converted_files+=("$each_file"); fi

    fi


fi


# Set batch response
if [[ 'yall' =~ ^($aud_conv_resp|$vid_conv_resp|$av_conv_resp|$con_conv_resp)$ ]]; then
batch_resp=True
echo -e \\n Batch response is being used. \\n
fi


done




# Count all files in par dir
file_count=$(ls "$par_dir" | wc -l)


# Check if anything has been converted
if [[ ${#converted_files[@]} -gt 0 ]]; then
    
    # Mark par dir for deletion if all files have been converted
    if [[ ${#converted_files[@]} -eq $file_count ]]; then
    echo -e \\n All A/V files in dir have been converted.

        # Check for dups in pcd_delete_these
        if grep -Fqx "$par_dir" ~/code/bash/pcd_delete_these; then
        echo -e \\n "$par_dir" already in pcd_delete_these
        else
        echo "$par_dir" >> ~/code/bash/pcd_delete_these
        echo -e \\n Added to pcd_delete_these:\\n "$par_dir"
        fi
    
    # Mark individual files for deletion
    else
        for i in ${converted_files[@]}; do
        echo "$i" >> ~/code/bash/pcd_delete_these
        done
    
    fi
        


fi






















