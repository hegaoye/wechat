#!/usr/bin/env bash
yes|apt-get update
yes|apt-get install adb
yes|apt-get install supervisor
systemctl enable supervisor
systemctl start supervisor