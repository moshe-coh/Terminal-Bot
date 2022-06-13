#!/bin/bash

# update code upstream
python3 upstream.py

# Install rclone static binary
wget -q https://downloads.rclone.org/v1.58.1/rclone-v1.58.1-linux-amd64.zip
unzip -q rclone-*-linux-amd64.zip
mkdir -p ~/.local/bin
mv rclone-*-linux-amd64/rclone ~/.local/bin/rclone
export PATH=$PWD/.local/bin:$PATH
echo "Rclone installed successfully"
# remove junk
rm -rf rclone-*-linux-amd64 rclone-*-linux-amd64.zip *.txt *yml *.md

# Create rclone.conf file from base64
if [[ -n $RCLONE_CONFIG_BASE64 ]]; then
	echo "Rclone config detected"
	echo "[DRIVE]" > rclone.conf
    mkdir -p $HOME/.config/rclone
	echo "$(echo $RCLONE_CONFIG_BASE64|base64 -d)" >> $HOME/.config/rclone/rclone.conf
        echo "Rclone config placed in position"
fi

# fetch rclone.conf from url

if [[ -n $RCLONE_CONFIG_URL ]]; then
	echo "Fetching rclone.conf from url"
	mkdir -p $HOME/.config/rclone
    curl -o$HOME/.config/rclone/rclone.conf "$RCLONE_CONFIG_URL"

fi

python3 bot.py
