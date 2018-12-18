#!/bin/sh
echo "\033[32m--Downloading scapy ...\033[0m";
git clone --recursive https://github.com/secdev/scapy.git $HOME/scapy;
echo "\033[32m--Installing scapy ...\033[0m";
cd $HOME/scapy;
sudo python setup.py install;
sudo python3 setup.py install;
