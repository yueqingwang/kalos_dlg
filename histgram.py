# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 15:44:33 2016

@author: wangyueqing
"""


import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


# example data
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution
x = mu + sigma * np.random.randn(10000)

num_bins = 20
# the histogram of the data
n, bins, patches = plt.hist(x, num_bins, facecolor='green', alpha=0.5)
# add a 'best fit' line
y = mlab.normpdf(bins, mu, sigma)*10000*(bins[1]-bins[0])
plt.plot(bins, y, 'r--')

plt.xlabel('Smarts')
plt.ylabel('counts')
plt.title(r'$\mu=100$, $\sigma=15$')

ylimit = plt.ylim()
ylen = ylimit[1] - ylimit[0]
plt.arrow(mu+3*sigma, 0, 0.0, ylen/3, head_width=2, head_length=ylen/50, fc='k', ec='k')
plt.arrow(mu-3*sigma, 0, 0.0, ylen/3, head_width=2, head_length=ylen/50, fc='k', ec='k')
plt.text(mu-3*sigma-4, ylen/2.7, u'-3$\sigma$')
plt.text(mu+3*sigma-4, ylen/2.7, u'+3$\sigma$')
plt.xlim(mu-6*sigma,mu+6*sigma)
# Tweak spacing to prevent clipping of ylabel
plt.subplots_adjust(left=0.15)
plt.show()