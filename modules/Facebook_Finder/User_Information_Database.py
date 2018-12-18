#!/usr/bin/env python
# license removed for brevity
import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import time
import json
from config.console_formatter import Console_Formatter


class User_Information_Database:
    '''
    {person_link : {
                    'name' : person_name,
                    'posts' : [posts_lists],
                    'friends' : [friends_lists],
                    'photos' : [href_links],
                    'info_type' : info_data,
                    }}
    '''
    #PUBLIC
    data_path = os.path.join(current_folder, "user_info_database.json")
    database = {}
    is_info = True
    #PRIVATE
    program_name_ = __name__
    console_formatter_  = Console_Formatter()

    def add_user(self, user_link, user_name):
        if user_link == None or user_name == None:
            if self.is_info :
                msg = "User link : {} or user name : {} is empty, adding user fail !".format(user_link, user_name)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return False

        if self.is_info :
            msg = "Adding user {} : {} ...".format(user_name, user_link)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.database[user_link] = {'name' : user_name}
        return True

    def add_info(self, user_link, info_type, info_data):
        if not user_link in self.database:
            if self.is_info :
                msg = "Cannot find user ! Adding user first !"
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return False
        if self.is_info :
            msg = "Adding user {} {} infomation : {} ...".format(self.database[user_link]['name'], info_type, info_data)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.database[user_link][info_type] = info_data
        return True

    def get_database(self):
        return self.database

    def set_database(self, database):
        self.database = database

    def load_database(self, data_path=None):
        data_path = self.data_path if data_path == None else data_path
        if not os.path.exists(data_path):
            if self.is_info:
                msg = "Database file : {} not found !".format(data_path)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return False
        else:
            if self.is_info :
                msg = "Loading database : {} ...".format(data_path)
                print(self.console_formatter_.DEBUG(self.program_name_, msg))
            with open(data_path, "r") as f:
                self.database = json.loads(json.load(f))
            return True

    def save_database(self, data_path=None):
        data_path = self.data_path if data_path == None else data_path
        if self.is_info :
            msg = "Saving database : {} ...".format(data_path)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        with open(data_path, "w") as f:
            json.dump(json.dumps(self.database), f)
        return True

    def __init__(self, data_path=None, is_info=True):
        self.is_info = is_info
        if self.is_info :
            msg = "Initializing ..."
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.data_path = data_path if data_path != None else self.data_path
        if self.is_info :
            msg = "Setting database file path : {}".format(self.data_path)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))

    def __del__(self):
        if self.is_info :
            msg = "Closing ..."
            print(self.console_formatter_.WARN(self.program_name_, msg))
