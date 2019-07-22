#!/bin/bash

sudo apt update
sudo apt -y upgrade

sudo apt -y install nginx-extras python3-pip wireless-tools build-essential cmake \
    pkg-config libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev \ 
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \ 
    libatlas-base-dev gfortran python3-dev 

sudo apt --auto-remove

sudo pip3 install tornado supervisor wifi

# Enable thegreenbot.local
sudo echo thegreenbot > /etc/hostname
sudo snap refresh core --edge
sudo snap install avahi-client
sudo snap install avahi

# Enabling Camera
echo "start_x=1" >> /boot/firmware/config.txt
echo "gpu_mem=128" >> /boot/firmware/config.txt

# repo is already on the base image
# aliases is also on the base image

# update repo, copy any new aliases and source
cd $GREENBOTS_ROOT/src
git update
cp configs/bash/bash_aliases ~/.bash_aliases
exec $SHELL

# Need to have www-data to be able to run sudo commands
# This is normally a pretty insecure thing to do.
# This is a one user educational bot though, so we think it's ok
# Friendly comments welcome :)
sudo usermod -a -G adm www-data 

sudo chown -R ubuntu:ubuntu $GREENBOTS_ROOT
# sudo chown -R www-data $GREENBOTS_ROOT/web-interface

echo "OpenCV installation"

# OpenCV Installation
OPENCV_ROOT=/opt/opencv
OPENCV_CONTRIB_ROOT=/opt/opencv_contrib

sudo mkdir $OPENCV_ROOT
sudo mkdir $OPENCV_CONTRIB_ROOT
sudo chown -R ubuntu:ubuntu $OPENCV_ROOT
sudo chown -R ubuntu:ubuntu $OPENCV_CONTRIB_ROOT

git clone https://github.com/Itseez/opencv.git $OPENCV_ROOT --depth 1 --branch 3.4.0
git clone https://github.com/Itseez/opencv_contrib.git $OPENCV_CONTRIB_ROOT --depth 1 --branch 3.4.0

cd $OPENCV_ROOT
mkdir build
git checkout 3.4.0

cd $OPENCV_CONTRIB_ROOT
git checkout 3.4.0

cd $OPENCV_ROOT
cmake
make -j4
sudo make install
sudo ldconfig

sudo ifconfig wlan0 up

sudo /etc/init.d/nginx force-reload
sudo /etc/init.d/greenbots-api force-reload
