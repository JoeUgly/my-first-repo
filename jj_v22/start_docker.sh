#!/usr/bin/env bash

# Desc: Start Docker in rootless mode and run Splash container


# to do:
# retry loop +
# command='--disable-private-mode --disable-browser-caches --slots 32', detach=True
#--restart on-failure[:max-retries]
#Docker --restart option won’t work without -d.
#--memory
# term_out is still written to after starting new term_out
# make sure this program ends when scraper starts
# kill -9 pid if deactivating





# Necessary for rootless Docker. Cannot be done from Python
echo -e \\n\\nExporting DOCKER_HOST env var ...
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock

# Start Docker as non root
if [ $(systemctl --user is-active docker) == "inactive" ]; then

    echo Starting Docker ...
    systemctl --user start docker

    while true; do
        sleep 1
        if [ $(systemctl --user is-active docker) == "active" ]; then
            break
        fi
        echo ...
        systemctl --user restart docker
    done

# Restart Docker to free memory
else

    echo Restarting Docker ...
    systemctl --user restart docker

    # Kill all child procs
    #pkill -9 python3 # might be overkill
    #pkill -P $$

    while true; do
        sleep 1
        if [ $(systemctl --user is-active docker) == "active" ]; then
            break
        fi
        echo ...
        systemctl --user restart docker
    done

fi


# Remove previous session
docker stop jj_con
docker rm jj_con

# Start Splash container
echo Starting Splash container ...
docker run -d -p 8050:8050 --name jj_con scrapinghub/splash


# Make date dir to put results into
dater_dir=/home/joepers/joes_jorbs/$(date +%m_%d_%y)
mkdir -p $dater_dir


# Start Python scraper if not already running
#if $(pgrep -f jj_scraper22.py > /dev/null); then
#echo jj_scraper22.py is already running
# Use --nostart to start Docker but not jj_scraper
if [[ $1 = "--nostart" ]]; then
    echo Not starting jj_scraper

else

    # Check if log file name already exists
    inc=0
    while true; do
        if [[ -e $dater_dir/term_out$inc ]]; then
            ((inc++))
        else
            break
        fi
    done

# -u is unbuffered output. Redirect stderr to stdout and send them to both console and text file
python3.8 -u /home/joepers/code/jj_v22/jj_scraper22.py 2>&1 | tee $dater_dir/term_out$inc


fi


























