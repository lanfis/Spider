#!/usr/bin/env python
# license removed for brevity
import requests
from bs4 import BeautifulSoup

import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

from Spider import Spider

spider = Spider()

print("program starting ...")

url = "http://www.ivsky.com/"
url = "http://www.ivsky.com/bizhi/yourname_v39947/"
#url = "https://tw.appledaily.com/headline/daily/20170308/37575304"
#url = "https://www.ptt.cc/bbs/index.html"
url = "https://disp.cc/b/163-9toR"

spider.init()
spider.image_downloader(url, None)
spider.url_downloader(url, "and.html")
#spider.test(url)

