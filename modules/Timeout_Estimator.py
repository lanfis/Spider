#!/usr/bin/env python
# license removed for brevity
import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)
main_folder = os.path.join(current_folder, "..")
sys.path.append(main_folder)
'''
utils_folder = os.path.join(current_folder, "..", "utils")
sys.path.append(utils_folder)
'''
import time
#import numpy as np


class Timeout_Estimator:
    t1_ = 0
    t2_ = 99
    dt_ = -1
    
    timeout_est = 1
    timeout_max = 2
    torlorence = 0.2
    def __init__(self, torlorence=0.2, timeout_max=2):
        self.torlorence = torlorence if torlorence > 0 else 0.2
        self.timeout_max = timeout_max if timeout_max > 0 else 2


    def set_timer(self):
        self.start()

    def get_timer(self):
        self.stop()
        if self.timeout_est < self.eta():
            self.timeout_est = self.eta() + self.torlorence
            self.timeout_est = self.timeout_est if self.timeout_est < self.timeout_max else self.timeout_max
        else:
            self.timeout_est = self.timeout_est - self.torlorence
        return self.timeout_est

    def start(self):
        self.t1_ = time.time()

    def stop(self):
        self.t2_ = time.time()

    def eta(self):
        self.dt_ = self.t2_ - self.t1_
        return self.dt_

    def set_torlorence(self, value):
        self.torlorence = value

    def get_torlorence(self):
        return self.torlorence
