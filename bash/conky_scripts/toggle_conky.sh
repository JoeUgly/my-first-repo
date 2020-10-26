#!/usr/bin/env bash

pidder=$(pgrep conky)

if [[ $pidder ]]
then
kill $pidder
else
conky &
fi
exit



