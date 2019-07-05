#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

sudo apt update
sudo apt -y upgrade

sudo apt -y install nginx python3-pip

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
    root    /var/www/html;
    index   index.html;

    upstream frontends {
        server 127.0.0.1:8000;
        server 127.0.0.1:8001;
    }

    access_log /var/log/nginx/access.log;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    keepalive_timeout 65;
    types_hash_max_size 2048;
	  server_tokens off;
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

        # Allow file uploads
        client_max_body_size 50M;

        location ^~ /assets/ {
            root /var/www/html;
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

        location /server {
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
sudo mkdir -p /var/www/config
sudo mkdir -p /var/www/logs

echo "{}" | sudo tee -a /var/www/config/config.json
sudo touch /var/www/logs/events.log
sudo chown -R www-data /var/www/config
sudo chown -R www-data /var/www/logs
sudo usermod -a -G adm www-data

sudo bash -c "cat > /etc/supervisord.conf" << EOL
[supervisord]
logfile=/var/log/supervisord.log
logfile_maxbytes=50MB
logfile_backups=3
loglevel=info
pidfile=/var/run/supervisord.pid
nodaemon=false

[program:tornado-8000]
command = python3 /var/www/server.py --port=8000
stderr_logfile = /var/log/supervisor/tornado-stderr.log
stdout_logfile = /var/log/supervisor/tornado-stdout.log 
autostart = true
autorestart = true

[program:tornado-8001]
command = python3 /var/www/server.py --port=8001
stderr_logfile = /var/log/supervisor/tornado-stderr.log
stdout_logfile = /var/log/supervisor/tornado-stdout.log 
autostart = true
autorestart = true
EOL

sudo supervisord -c /etc/supervisord.conf
sudo service nginx restart
