#!/usr/bin/env python
# license removed for brevity
import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)
modules_folder = os.path.join(current_folder, "..")
sys.path.append(modules_folder)
main_folder = os.path.join(modules_folder, "..")
sys.path.append(main_folder)

import time
import json
from config.console_formatter import Console_Formatter

from bs4 import BeautifulSoup
from Web_Browser_Driver import Web_Browser_Driver
from Web_Browser_Driver_Keys import Web_Browser_Driver_Keys
from Auto_Browser import Auto_Browser
from Login_Breaker import Login_Breaker

from Friend_Link_Parser import Friend_Link_Parser
from Post_Data_Parser import Post_Data_Parser
from Search_Person_Parser import Search_Person_Parser
from User_Information_Database import User_Information_Database


class Facebook_Finder:
    ##PUBLIC
    version = "1.0"
    agent_header = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"

    user_infomation_database = User_Information_Database()

    post_data_parser = Post_Data_Parser()
    friend_link_parser = Friend_Link_Parser()
    search_person_parser = Search_Person_Parser()
    cookies_path = os.path.join(current_folder, "cookies.json")
    is_info = True

    banner_personal_profile_locate = '個人檔案'
    banner_personal_profile_main_page_locate = '首頁'
    headline_post_locate = '動態時報'
    headline_about_locate = '關於'
    headline_friends_locate = '朋友'
    headline_photos_locate = '相片'

    search_headline_posts = '貼文'
    search_headline_persons = '人物'
    search_headline_photos = '相片'
    search_headline_videos = '影片'
    ##PRIVATE
    program_name_ = __name__
    console_formatter_  = Console_Formatter()
    parser_ = None

    page_links = {}

    browser = None
    auto_browser = None
    cookies = None
    is_login = False

    def link(self, address):
        self.browser.access_website(address)

    def login(self, account, passwd, wait_time=10):
        if self.is_info :
            msg = "Starting login as {} ...".format(account)
            print(self.console_formatter_.NOTIFY(self.program_name_, msg))

        self.is_login = Login_Breaker(self.browser, self.is_info)(account, passwd, seperate=False, wait_time=wait_time)

        if self.is_login == False:
            if self.is_info :
                msg = "Returning back ..."
                print(self.console_formatter_.FATAL(self.program_name_, msg))
            self.browser.backward()
        else:
            if self.is_info :
                msg = "Login successfully !"
                print(self.console_formatter_.INFO(self.program_name_, msg))
        return self.is_login
    '''
    def person_parser(self):
        if self.is_info :
            msg = "Personal infomation parsing ..."
            print(self.console_formatter_.INFO(self.program_name_, msg))
        links = BeautifulSoup(self.browser.get_source(), "lxml").find_all('a')
        person_name = None
        is_name_find = False
        for link in links:
            if 'title' in link.attrs:
                if link.get('title') == "{}".format(self.banner_personal_profile_locate):
                    self.person_profile.add_person(link.text)
                    self.person_profile.add_info(link.text, 'href', link.get('href'))
                    person_name = link.text
                    is_name_find = True
                    break
        if not is_name_find:
            if self.is_info :
                msg = "Personal infomation parsing fail ! Cannot find personal infomation link !"
                print(self.console_formatter_.FATAL(self.program_name_, msg))
            return False

        if self.is_info :
            msg = "Entering personal infomation page : {} ...".format(person_name)
            print(self.console_formatter_.INFO(self.program_name_, msg))
        self.link(self.person_profile.profile[person_name]['href'])

        self.parse_personal_page()
        return True
    '''
    def parse_personal_page(self):
        if self.is_info :
            msg = "Parsing page ..."
            print(self.console_formatter_.INFO(self.program_name_, msg))
        bs_ = BeautifulSoup(self.browser.get_source(), "lxml")

        user_name = bs_.find("a", {'class' : '_2nlw _2nlv'}).text
        user_link = bs_.find("a", {'class' : '_2nlw _2nlv'})['href']
        self.user_infomation_database.add_user(user_link, user_name)

        headline = bs_.find("div", id='fbTimelineHeadline')
        headline_post = headline.find(text=self.headline_post_locate).find_parent("a")
        headline_about = headline.find(text=self.headline_about_locate).find_parent("a")
        headline_friends = headline.find(text=self.headline_friends_locate).find_parent("a")
        headline_photos = headline.find(text=self.headline_photos_locate).find_parent("a")

        self.page_links['headline'] = [headline]
        if headline_post != None:
            self.page_links['headline'].append([self.headline_post_locate, headline_post])
            self.page_links[self.headline_post_locate] = headline_post
        if headline_about != None:
            self.page_links['headline'].append([self.headline_about_locate, headline_about])
            self.page_links[self.headline_about_locate] = headline_about
        if headline_friends != None:
            self.page_links['headline'].append([self.headline_friends_locate, headline_friends])
            self.page_links[self.headline_friends_locate] = headline_friends
        if headline_photos != None:
            self.page_links['headline'].append([self.headline_photos_locate, headline_photos])
            self.page_links[self.headline_photos_locate] = headline_photos

        if headline_friends != None:
            friends_lists = self.friend_parser()
            self.user_infomation_database.add_info(user_link, 'friends', friends_lists)
        if headline_post != None:
            posts_lists = self.post_parser()
            self.user_infomation_database.add_info(user_link, 'posts', posts_lists)
        return self.page_links

    def post_parser(self, browse_counts=64):
        if self.is_info :
            msg = "Parsing posts ..."
            print(self.console_formatter_.INFO(self.program_name_, msg))
        if not self.headline_post_locate in self.page_links:
            if self.is_info :
                msg = "Cannot find posts link !"
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return None
        self.link(self.page_links[self.headline_post_locate]['href'])
        self.auto_browser.auto_page_down(browse_counts)
        post_lists = self.post_data_parser.add_source(self.browser.get_source())

        for post_list in post_lists:
            self.page_links[self.headline_post_locate].append(post_list)
            if self.is_info :
                msg = "Posts found : {} : {} ".format(post_list, post_lists[post_list]['article'] if 'article' in post_lists[post_list] else "")
                print(self.console_formatter_.NOTIFY(self.program_name_, msg))
                for reply in post_lists[post_list]['replys']:
                    msg = "---- {}".format(reply)
                    print(self.console_formatter_.NOTIFY(self.program_name_, msg))

        if self.is_info :
            msg = "Parsing posts done !"
            print(self.console_formatter_.INFO(self.program_name_, msg))
        return post_lists

    def friend_parser(self, browse_counts=64):
        if self.is_info :
            msg = "Parsing friends ..."
            print(self.console_formatter_.INFO(self.program_name_, msg))
        if not self.headline_friends_locate in self.page_links:
            if self.is_info :
                msg = "Cannot find friends link !"
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return None
        self.link(self.page_links[self.headline_friends_locate]['href'])
        self.auto_browser.auto_page_down(browse_counts)
        friends_lists = self.friend_link_parser.add_source(self.browser.get_source())

        for href_link in friends_lists:
            #self.page_links[self.headline_friends_locate].append([friends_lists[href_link], href_link])
            if self.is_info :
                msg = "Friends : {} {}".format(friends_lists[href_link], href_link)
                print(self.console_formatter_.NOTIFY(self.program_name_, msg))
        if self.is_info :
            msg = "Parsing friends done !"
            print(self.console_formatter_.INFO(self.program_name_, msg))
        return friends_lists

    def enter_personal_information(self, link_name=None):
        link_name = self.banner_personal_profile_locate if link_name == None else link_name
        if self.is_info :
            msg = "Entering personal profile information ..."
            print(self.console_formatter_.INFO(self.program_name_, msg))

        if self.browser.find_xpath("//a[@title='{}']".format(link_name)):
            self.browser.click()
            return True
        else:
            if self.is_info :
                msg = "Cannot find personal profile information link !"
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return False

    def enter_personal_main_page(self, link_name=None):
        link_name = self.banner_personal_profile_main_page_locate if link_name == None else link_name
        if self.is_info :
            msg = "Entering personal profile main page links : {} ...".format(link_name)
            print(self.console_formatter_.INFO(self.program_name_, msg))

        if self.browser.find_link_text("{}".format(link_name)):
            self.browser.click()
            return True
        else:
            if self.is_info :
                msg = "Cannot find personal profile main page links !".format(link_name)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return False

    def user_search(self, user_name, browse_counts=64):
        if self.is_info :
            msg = "Searching users ..."
            print(self.console_formatter_.INFO(self.program_name_, msg))
        if not self.search(user_name):
            if self.is_info :
                msg = "Searching fail !"
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return None
        self.browser.click_link(self.search_headline_persons)
        self.auto_browser.auto_page_down(browse_counts)
        search_person_lists = self.search_person_parser.add_source(self.browser.get_source())

        for search_person in search_person_lists:
            if self.is_info :
                msg = "User : {} link={}".format(search_person_lists[search_person][0], search_person)
                print(self.console_formatter_.NOTIFY(self.program_name_, msg))
        if self.is_info :
            msg = "Searching users done !"
            print(self.console_formatter_.INFO(self.program_name_, msg))

        return search_person_lists

    def search(self, text):
        if self.is_info :
            msg = "Searching {} ...".format(text)
            print(self.console_formatter_.INFO(self.program_name_, msg))
        if not self.browser.search(text):
            if self.is_info :
                msg = "Searching {} fail !".format(text)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return False
        else:
            return True

    def screenshot(self, file_name):
        self.browser.screenshot(file_name)

    def wait(self, tm):
        self.browser.wait(tm)

    def get_source(self):
        return self.browser.get_source()

    def get_cookies(self):
        self.cookies = self.browser.get_cookies()
        return self.cookies

    def save_cookies(self, path):
        if self.is_info :
            msg = "Saving cookies : {} ...".format(path)
            print(self.console_formatter_.INFO(self.program_name_, msg))
        with open(path, "w") as f:
            json.dump(json.dumps(self.cookies), f)
        return

    def load_cookies(self, path):
        if self.is_info :
            msg = "Checking cookies : {} ...".format(path)
            print(self.console_formatter_.INFO(self.program_name_, msg))
        if not self.check_path(path):
            if self.is_info:
                msg = "Cookies : {} not found !".format(self.cookies_path)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return False
        else:
            if self.is_info :
                msg = "Loading cookies : {} ...".format(path)
                print(self.console_formatter_.INFO(self.program_name_, msg))
            with open(path,"r") as f:
                self.cookies = json.loads(json.load(f))
                for cookie in self.cookies:
                    self.browser.add_cookie(cookie)
            return True

    def set_browser(self, browser):
        self.browser = browser
        self.auto_browser = Auto_Browser(self.browser)

    def get_browser(self):
        return self.browser

    def check_path(self, path):
        return os.path.exists(path)

    def __init__(self, browser=None, is_cookies_clear=True, is_notifications=False, is_window=True, is_info=True, is_debug=True, **kwargs):
        self.is_info = is_info
        if self.is_info :
            msg = "Initializing ..."
            print(self.console_formatter_.INFO(self.program_name_, msg))
        self.browser = Web_Browser_Driver(is_cookies_clear=is_cookies_clear, is_notifications=is_notifications,
                                          is_window=is_window, is_info=is_debug,
                                          **kwargs) if browser == None else browser
        self.auto_browser = Auto_Browser(self.browser, is_info=is_debug)
        self.user_infomation_database.load_database()
        if not is_cookies_clear:
            self.load_cookies(self.cookies_path)
        self.link("http://www.facebook.com")

    def __del__(self):
        self.get_cookies()
        self.save_cookies(self.cookies_path)
        self.user_infomation_database.save_database()
        if self.is_info :
            msg = "Closing ..."
            print(self.console_formatter_.WARN(self.program_name_, msg))


def main(**kwargs):
    ff  = Facebook_Finder(is_cookies_clear=True, is_debug=True, **kwargs)
    #ff.login("asdas@hotmail.com", "123")
    ff.login("navida2341@gmail.com", "f2mPqDDG")
    search_user_list = ff.user_search("吳音寧")
    #ff.link("https://www.facebook.com/profile.php?id=100001277912128&__tn__=%2Cd-]-h-R&eid=ARBo_xeaJ8T0r8X6IQFxWM99sqIXjOpxCdTxL9g5s1dVhTKT1kJj44yQKvXMy1QNnx7pNQ6mK57MzBdk")
    #ff.link("https://www.facebook.com/profile.php?id=100022934512189")
    ##ff.link("https://www.facebook.com/chen0817")
    #ff.link("https://www.facebook.com/groups/451357468329757/?jazoest=2651001208210110412052665652120821001147665108731081051021078111868715776110715210810852651197711411010566768910065586510012079120113814597119578010410472116896948114861065253116104979811212210612210649121104102881201047611210511111065")
    #ff.parse_personal_page()
    #ff.enter_personal_main_page()
    #ff.enter_personal_main_page_links("關於")
    #ff.search("Kelly")
    #if ff.get_browser().find_tag_name("a"):
        #ff.get_browser().click()
    #ff.find_link_text("天氣預報", is_contact=False)
    #wb.access_website("https://world.taobao.com/product/%E6%B7%98%E5%AF%B6%E5%A4%A7%E9%99%B8.htm")
    #wb.find_link_text("淘寶網首頁", is_contact=False)
    #ff.click()

    #print(wb.get_source())
    time.sleep(23)

if __name__ == "__main__":
    args =  sys.argv[1:]
    kwargs  = {}
    for i in range(0, len(args),2):
        kwargs[args[i]] =   args[i+1]
    main(**kwargs)
