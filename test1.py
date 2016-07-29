# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 00:42:18 2016

@author: Administrator
"""
from beeswarm import beeswarm
import matplotlib.pyplot as plt
import numpy as np

def GetColor(x):
    colors = []
    for item in x:
        if item > 0: colors.append("red")
        else: colors.append("blue")
    return colors
    
d1 = np.random.uniform(low=-3, high=3, size=100)
d2 = np.random.normal(size=100)
print(d1)

fig = plt.figure()
fig.set_size_inches((8,8))
ax1 = plt.subplot(221)
ax2 = plt.subplot(222)
ax3 = plt.subplot(223)
ax4 = plt.subplot(224)
colors = GetColor(d1) + GetColor(d2)
print(colors)
beeswarm([d1,d2], method="swarm", labels=["Uniform","Normal"], col=colors, ax=ax3)
beeswarm([d1,d2], method="swarm", labels=["Uniform","Normal"], col="black", ax=ax1)
print(d1)
beeswarm([d1,d2], method="swarm", labels=["Uniform","Normal"], col=["black","red"], ax=ax2)




#beeswarm([d1,d2], method="swarm", labels=["Uniform","Normal"], col=["red","blue","orange"], ax=ax4)
plt.tight_layout()
plt.show()