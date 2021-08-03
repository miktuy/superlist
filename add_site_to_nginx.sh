#!/bin/bash
sed "s/SITENAME/$1/g" source/deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/$1
sudo ln -s ../sites-available/$1 /etc/nginx/sites-enabled/$1
sed "s/SITENAME/$1/g" source /deploy_tools/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/$1.service
sudo systemctl daemon-reload
sudo systemctl reload nginx
sudo systemctl enable $1
sudo systemctl start $1