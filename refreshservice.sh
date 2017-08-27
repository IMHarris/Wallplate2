#!/bin/bash

sudo cp /home/pi/piproj/wallplate/wallplate.service /lib/systemd/system/wallplate.service
sudo systemctl daemon-reload
echo "Wallplate service executable reloaded"
