#!/bin/bash

sudo mkdir -p $GREENBOTS_ROOT
sudo mkdir -p $GREENBOTS_ROOT/logs
sudo mkdir -p $SUPERVISOR_ROOT/conf
sudo mkdir -p $SUPERVISOR_ROOT/logs

sudo touch $GREENBOTS_ROOT/logs/events.log

sudo ln -s $GREENBOTS_ROOT/src/api $API_SERVER_ROOT
sudo ln -s $GREENBOTS_ROOT/src/web $WEB_INTERFACE_ROOT

sudo cp $GREENBOTS_ROOT/src/configs/bot-config.json $API_SERVER_ROOT/bot-config.json

sudo cp $GREENBOTS_ROOT/src/configs/firmware-config.txt /boot/firmware/config.txt

sudo rm $SUPERVISOR_ROOT/conf/supervisord.conf
sudo rm /etc/init.d/greenbots-api.sh
sudo ln -s $GREENBOTS_ROOT/src/configs/supervisord/supervisord.conf $SUPERVISOR_ROOT/conf
sudo ln -s $GREENBOTS_ROOT/src/configs/init_scripts/greenbots-api.sh /etc/init.d/

sudo rm /etc/nginx/nginx.conf
sudo ln -s $GREENBOTS_ROOT/src/configs/nginx/nginx.conf /etc/nginx/
