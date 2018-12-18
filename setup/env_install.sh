#!/bin/sh
FILE_GECKODRIVER="geckodriver-v0.23.0-linux64.tar.gz";
FILE_CHROMEDRIVER="chromedriver_linux64.zip";
FILE_PHANTOMJS="phantomjs-2.1.1-linux-x86_64.tar.bz2";

echo "\033[32m--Updating ...\033[0m";
sudo apt-get -y update;
sudo apt-get install -y git;
sudo apt-get install -y python-pip;
sudo apt-get install -y python3-pip;
sudo -H pip3 install --upgrade pip;
sudo -H pip3 install --upgrade setuptools
echo "\033[32m--Installing Google Chrome ...\033[0m";
sudo dpkg -i google-chrome-stable_current_amd64.deb;
echo "\033[32m--Installing request ...\033[0m";
sudo -H pip3 install requests;
echo "\033[32m--Installing Selenium ...\033[0m";
sudo -H pip3 install Selenium;
echo "\033[32m--Installing pyvirtualdisplay ...\033[0m";
sudo -H pip3 install pyvirtualdisplay;
sudo apt-get install -y xvfb xserver-xephyr vnc4server python-pil scrot;
echo "\033[32m--Installing BeautifulSoup4 ...\033[0m";
sudo -H pip3 install BeautifulSoup4;
echo "\033[32m--Installing pyquery ...\033[0m";
sudo -H pip3 install pyquery;
echo "\033[32m--Installing Tesserocr ...\033[0m";
sudo apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev;
echo "\033[32m--Installing lxml ...\033[0m";
sudo apt-get install -y python3-lxml;
sudo apt-get install -y libxml2-dev libxslt-dev python-dev;
sudo -H pip install lxml;
echo "\033[32m--Installing aiohttp ...\033[0m";
sudo -H pip3 install aiohttp;
echo "\033[32m--Installing cchardet aiodns ...\033[0m";
sudo -H pip3 install cchardet aiodns;

#echo "\033[32m--Installing pyspider ...\033[0m";
#sudo -H pip3 install pyspider;
echo "\033[32m--Installing scrapy ...\033[0m";
sudo -H pip3 install scrapy;
sudo -H pip3 install scrapy-splash;
sudo -H pip3 install scrapy-redis;
sudo -H pip3 install scrapyd;
sudo -H pip3 install scrapyd-client;
sudo -H pip3 install python-scrapyd-api;
sudo -H pip3 install scrapyrt;
sudo -H pip3 install gerapy;
echo "\033[32m--Installing scapy ...\033[0m";
#sudo apt-get install -y python-scapy python-pyx python-gnuplot;
sudo sh scapy_install.sh;

echo "\033[32m--Installing geckodriver ...\033[0m";
sudo wget "https://github.com/mozilla/geckodriver/releases/download/v0.23.0/"$FILE_GECKODRIVER;
sudo tar zxvf $FILE_GECKODRIVER;
sudo rm $FILE_GECKODRIVER;
sudo cp geckodriver /usr/bin;
sudo echo "export PATH=\"\$PATH:/usr/local/geckodriver\"" >> ~/.profile;
source ~/.profile;

echo "\033[32m--Installing chromedriver ...\033[0m";
sudo wget "https://chromedriver.storage.googleapis.com/2.44/"$FILE_CHROMEDRIVER;
sudo unzip $FILE_CHROMEDRIVER;
sudo rm $FILE_CHROMEDRIVER;
sudo cp chromedriver /usr/bin;
sudo echo "export PATH=\"\$PATH:/usr/local/chromedriver\"" >> ~/.profile;
source ~/.profile;
'''
echo "\033[32m--Installing chromedriver ...\033[0m";
sudo wget "https://bitbucket.org/ariya/phantomjs/downloads/"$FILE_PHANTOMJS;
sudo tar jxvf $FILE_PHANTOMJS;
sudo rm $FILE_PHANTOMJS;
sudo cp chromedriver /usr/bin;
sudo echo "export PATH=\"\$PATH:/usr/local/chromedriver\"" >> ~/.profile;
source ~/.profile;
'''



