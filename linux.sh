#!/bin/bash
# Build script for wpmaker for linux

rm -rf linux2
python pyinstaller.py -F -o linux2 -n wpmaker wpmaker.py
rm plugins/*.pyc
cp -r plugins linux2/dist
cp LICENSE linux2/dist
cp monitor-wallpaper-icon.png linux2/dist
