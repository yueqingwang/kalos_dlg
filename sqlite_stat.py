# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 08:40:01 2016

@author: wangyueqing
"""
import math


class StdevFunc:
    def __init__(self):
        self.M = 0.0
        self.S = 0.0
        self.k = 0
    
    def step(self, value):
        try:
            # automatically convert text to float, like the rest of SQLite
            val = float(value) # if fails, skips this iteration, which also ignores nulls
            tM = self.M
            self.k += 1
            self.M += ((val - tM) / self.k)
            self.S += ((val - tM) * (val - self.M))
        except:
            pass
    
    def finalize(self):
        if self.k <= 1: # avoid division by zero
            return None
        else:
            return math.sqrt(self.S / (self.k))
            
class sigma_plus(StdevFunc):
    def finalize(self):
        if self.k <= 1: # avoid division by zero
            return None
        else:
            return   self.M + math.sqrt(self.S / (self.k))

class sigma_minus(StdevFunc):
    def finalize(self):
        if self.k <= 1: # avoid division by zero
            return None
        else:
            return self.M - math.sqrt(self.S / (self.k)) 