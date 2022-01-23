#!/bin/bash

iconv -f ISO-8859-1 -t UTF-8//TRANSLIT textpixoubot.csv -o textpixoubot_u.csv

python ./bot.py

exit 0
