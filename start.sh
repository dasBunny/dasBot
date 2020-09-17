#!/bin/sh

screen -S dasbot -dm python3 bot.py
echo "Discord bot was started in background. Access using 'screen -r dasbot'"
