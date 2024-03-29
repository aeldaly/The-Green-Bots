#!/usr/bin/env bash

sudo apt update
sudo apt -y upgrade

sudo apt -y install nginx python3-pip wireless-tools pkg-config python-dev \
    libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev \
    libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg \
    libswscale-dev libavformat-dev libavcodec-dev netdata

sudo apt -y auto-remove

# Enable thegreenbot.local
sudo -E bash -c "echo thegreenbot > /etc/hostname"
sudo snap refresh core --edge
sudo snap install avahi-client
sudo snap install avahi

# repo is already on the base image
# aliases is also on the base image

# update repo, copy any new aliases and source
cd $GREENBOTS_ROOT/src
git pull
sudo cp configs/bash/bash_aliases /etc/profile.d/bash_aliases.sh
source /etc/profile

sudo pip3 install -r $GREENBOTS_ROOT/src/requirements.txt
sudo pip2 install -r $GREENBOTS_ROOT/src/requirements-python2.txt

$GREENBOTS_ROOT/src/scripts/folders_and_links.sh

# Need to have www-data to be able to run sudo commands
# This is normally a pretty insecure thing to do.
# This is a one user educational bot though, so we think it's ok
# Friendly comments welcome :)
sudo usermod -a -G adm www-data 

sudo chown -R ubuntu:ubuntu $GREENBOTS_ROOT
# sudo chown -R www-data $GREENBOTS_ROOT/web-interface

sudo ifconfig wlan0 up

sudo /etc/init.d/nginx force-reload
sudo /etc/init.d/greenbots-api.sh force-reload
sudo /etc/init.d/netdata force-reload

sudo update-rc.d greenbots-api.sh defaults
