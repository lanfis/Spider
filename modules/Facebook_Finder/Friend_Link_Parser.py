#!/usr/bin/env python
# license removed for brevity
import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import time
import json
from config.console_formatter import Console_Formatter

from bs4 import BeautifulSoup

class Friend_Link_Parser:
    #{link : name}
    friend_link_lists = {}
    def __call__(self, href_link):
        return self.friend_link_lists[href_link] if href_link in self.friend_link_lists else None

    def add_source(self, source):
        bs_ = BeautifulSoup(source, "lxml")
        friends_regions = bs_.find("div", {'id' : 'pagelet_timeline_medley_friends'})
        friends_lists = friends_regions.find_all("div", {'class' : 'uiProfileBlockContent'})

        friends = {}
        friend_name = None
        href_link = None
        for friend in friends_lists:
            friend_name = friend.find('a').text
            href_link = friend.find('a').get('href')
            friends[href_link] = friend_name
        self.friend_link_lists.update(friends)
        return friends

    def get_lists(self):
        return self.friend_link_lists
