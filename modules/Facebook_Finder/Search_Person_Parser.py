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

class Search_Person_Parser:
    '''
    {person_link : {'name' : name,
                    'link' : link}}
    '''
    person_lists = {}
    def add_source(self, source):
        bs_ = BeautifulSoup(source, "lxml")
        person_lists = bs_.find_all("div", {'class' : '_4p2o'})

        person_datas = {}
        person_img_link = None
        person_link = None
        person_name = None
        for person in person_lists:
            person_img_link = person.find("img")['src']
            person_link = person.find("a", {'class' : '_32mo'})['href']
            person_name = person.find("a", {'class' : '_32mo'}).get_text()
            person_datas[person_link] = [person_name, person_img_link]

        self.person_lists.update(person_datas)
        return person_datas

    def get_lists(self):
        return self.friend_link_lists
