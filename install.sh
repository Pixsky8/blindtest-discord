#!/bin/sh

docker build -t discord_blindtest .
echo "Starting docker"
sh start.sh
