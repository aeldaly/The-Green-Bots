#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

sudo apt update
sudo apt -y upgrade

sudo apt -y install nginx python3-pip wireless-tools build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python3-dev

sudo pip3 install tornado supervisor wifi

sudo bash -c "cat > /etc/nginx/nginx.conf" << EOL
user www-data;
worker_processes auto;
pid /run/nginx.pid;

include /etc/nginx/modules-enabled/*.conf;

error_log /var/log/nginx/error.log;

events {
    worker_connections 1024;
    use epoll;
}

http {
    root    /opt/thegreenbot/interfaces/web/;
    index   index.html;

    upstream frontends {
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
        server 127.0.0.1:8003;
        server 127.0.0.1:8004;
    }

    access_log /var/log/nginx/access.log;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    types_hash_max_size 2048;
    server_tokens off;
    proxy_http_version 1.1;
    proxy_read_timeout 200;
    
    sendfile on;

    tcp_nopush on;
    tcp_nodelay on;

    gzip on;
    gzip_min_length 1000;
    gzip_proxied any;
    gzip_types text/plain text/html text/css text/xml
               application/x-javascript application/xml
               application/atom+xml text/javascript;

  	ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
	ssl_prefer_server_ciphers on;

    # Only retry if there was a communication error, not a timeout
    # on the Tornado server (to avoid propagating "queries of death"
    # to all frontends)
    proxy_next_upstream error;

    server {
        listen 80;
        server_name thegreenbot.local;

        # Allow file uploads
        client_max_body_size 50M;

        location ^~ /assets/ {
            root /opt/thegreenbot/interfaces/web/;
            if (\$query_string) {
                expires max;
            }
        }
        location = /favicon.ico {
            rewrite (.*) /assets/favicon.ico;
        }
        location = /robots.txt {
            rewrite (.*) /assets/robots.txt;
        }

        location /api {
            proxy_pass_header Server;
            proxy_set_header Host \$http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Scheme \$scheme;
            proxy_pass http://frontends;
        }
    }
}
EOL

sudo mkdir -p /var/log/supervisor
sudo mkdir -p /opt/thegreenbot/config
sudo mkdir -p /opt/thegreenbot/logs

echo "{}" | sudo tee -a /opt/thegreenbot/config/config.json
sudo touch /opt/thegreenbot/logs/events.log
sudo chown -R www-data /opt/thegreenbot/config
sudo chown -R www-data /opt/thegreenbot/logs
sudo usermod -a -G adm www-data

sudo bash -c "cat > /etc/supervisord.conf" << EOL
[supervisord]
logfile=/var/log/supervisord.log
logfile_maxbytes=50MB
logfile_backups=3
loglevel=info
pidfile=/var/run/supervisord.pid
nodaemon=false

[supervisorctl]
serverurl = unix://supervisord.sock

[unix_http_server]
file = supervisord.sock

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[group:tornado_cluster]
programs = tornado_web_cluster

[program:tornado_web_cluster]
numprocs = 4
numprocs_start = 1
command = python3 /opt/thegreenbot/interfaces/web/server.py --port=80%(process_num)02d
process_name = %(program_name)s%(process_num)d
redirect_stderr = true
stderr_logfile = /var/log/supervisor/tornado-stderr.log
stdout_logfile = /var/log/supervisor/tornado-stdout.log 
autostart = true
autorestart = true
EOL

sudo supervisord -c /etc/supervisord.conf
sudo service nginx restart

sudo snap refresh core --edge
sudo snap install avahi-client
sudo snap install avahi

sudo ifconfig wlan0 up