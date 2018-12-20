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

class Post_Data_Parser:
    '''
    {post_time : {'article' : article_contents,
                  'replys' : [{'name' : post_reply_user_name, 'link' : post_reply_user_link, 'contents' : post_reply_contents, 'time' : post_reply_time}],
                  'img' : {'src' : img_src, 'fb_detect' : fb_detect}}
    '''
    post_data_lists = {}
    def __call__(self, post_time):
        return self.post_data_lists[post_time] if post_time in self.post_data_lists else None

    def add_source(self, source):
        bs_ = BeautifulSoup(source, "lxml")
        post_lists = bs_.find_all("div", {'class' : '_5pcb _4b0l _2q8l'})

        post_datas = {}
        post_time = None
        post_article_source = None
        post_article_contents = ""
        post_reply_source = None
        post_replys = []
        post_imgs = []
        #post_bravo_list = None
        for post_data in post_lists:
            #if post_data.find("abbr") != None:
            try:
                post_time = post_data.find("abbr")['title']
            except:
                pass
            else:
                post_datas[post_time] = {}

            post_article_source = post_data.find("div", {'data-ad-preview' : 'message'})
            if post_article_source != None:
                try:
                    post_article_contents = post_article_source.find("p").get_text()
                    '''
                    post_article_content = ""
                    for c in post_article_contents:
                        if c == "<br>":
                            post_article_content += "\n"
                        elif isinstance(c, str):
                            post_article_content += c
                    '''
                except:
                    pass
                else:
                    post_datas[post_time]['article'] = post_article_contents

            post_reply_source = post_data.find_all("div", {'class' : 'UFICommentContentBlock'})
            if post_reply_source != None:
                post_replys = []
                for r in post_reply_source:
                    post_reply_user_name = r.find("a", {'class' : 'UFICommentActorName'}).text
                    post_reply_user_link = r.find("a", {'class' : 'UFICommentActorName'})['href']
                    post_reply_contents = r.find("span", {'class' : 'UFICommentBody'}).get_text()
                    post_reply_time = r.find("abbr", {'class' : 'UFISutroCommentTimestamp livetimestamp'})['title']
                    post_replys.append({'name' : post_reply_user_name, 'link' : post_reply_user_link, 'content' : post_reply_contents, 'time' : post_reply_time})
                post_datas[post_time]['replys'] = post_replys

            post_img_src_lists = post_data.find_all("img")
            if post_img_src_lists != None:
                post_imgs = []
                for post_img in post_img_src_lists:
                    post_img_src = post_img['src']
                    post_img_fb_detect = post_img.get('aria-label')
                    post_imgs.append({'src' : post_img_src, 'fb_detect' : post_img_fb_detect})
                post_datas[post_time]['img'] = post_imgs

        self.post_data_lists.update(post_datas)
        return post_datas

    def get_lists(self):
        return self.friend_link_lists
