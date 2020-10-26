#!/usr/bin/env bash

# Desc: Learn how to parse long and short args using shift and case




# Set default values
force_opt=False
verb_opt=False




# Loop through args using $1 because $i doesn't work with shift
while true; do

    # case is basically an if statemnt with only one match
    case "$1" in

    # Verbose arg
    -v)
        verb_opt=True
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


echo $force_opt
echo $verb_opt


















