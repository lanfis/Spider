#!/usr/bin/env python
# license removed for brevity
import requests
from bs4 import BeautifulSoup

import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)
import time

from modules.Facebook_Finder import Facebook_Finder

ff  = Facebook_Finder(is_cookies_clear=True, is_debug=True, is_window=True)
ff.login("navida2341@gmail.com", "f2mPqDDG")
ff.link("https://www.facebook.com/sukuze?__tn__=%2Cd-]-h-R&eid=ARCKyYNC5j4oE78j13w8HaycmOJLSU_TQUlAHl50Yfl2jW9KB65c3Nf4Xjp9vwJNaZWUModv5YkidnO5")
ff.parse_personal_page()
#search_user_list = ff.user_search("吳音寧")
#for search_user in search_user_list:
    #ff.link(search_user)
    #ff.parse_personal_page()
#ff.link("https://www.facebook.com/groups/WuYinlingFanGroup/")
#ff.post_parser()
#ff.link("https://www.facebook.com/profile.php?id=100001277912128&__tn__=%2Cd-]-h-R&eid=ARBo_xeaJ8T0r8X6IQFxWM99sqIXjOpxCdTxL9g5s1dVhTKT1kJj44yQKvXMy1QNnx7pNQ6mK57MzBdk")
#ff.link("https://www.facebook.com/profile.php?id=100022934512189")
#ff.link("https://www.facebook.com/groups/451357468329757/?jazoest=2651001208210110412052665652120821001147665108731081051021078111868715776110715210810852651197711411010566768910065586510012079120113814597119578010410472116896948114861065253116104979811212210612210649121104102881201047611210511111065")
#ff.parse_personal_page()
time.sleep(20)
