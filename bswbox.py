# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 23:19:09 2016

@author: Administrator
"""


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import beeswarm  as bsw

def GetColor(x):
    colors = []
    q=np.percentile(x,[25,75])
    w1 = q[1]+(q[1]-q[0])*1.5
    w0 = q[0]-(q[1]-q[0])*1.5
    x.sort()
    for item in x:
        if item > w1 or item < w0: colors.append("red")
        else: colors.append("blue")
    return colors

#
## Create data
np.random.seed(10)
collectn_1 = np.random.normal(100, 30, 200)
collectn_2 = np.random.normal(80, 30, 200)
collectn_3 = np.random.normal(90, 20, 200)
collectn_4 = np.random.normal(70, 25, 200)

## combine these different collections into a list    
#data_to_plot = [collectn_1, collectn_2, collectn_3, collectn_4]
data_to_plot = [collectn_1]
# Create a figure instance
fig = plt.figure(1, figsize=(9, 6))

# Create an axes instance
ax = fig.add_subplot(111)
colors = GetColor(collectn_1)
# Create the boxplot
bp = ax.boxplot(data_to_plot,positions = [0])
bsw.beeswarm(data_to_plot,ax=ax,col=colors)