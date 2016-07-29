# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 09:49:45 2016

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
#n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
# add a 'best fit' line

(n, bins) = np.histogram(x, bins=500,normed=True,density=True)
bins = (bins[:-1] + bins[1:])/2
plt.plot(bins, np.add.accumulate(n)*(bins[1]-bins[0])*100,'o-',lw=0.5)

plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title(r'$\mu=100$, $\sigma=15$')

#plt.arrow(mu+3*sigma, 0, 0.0, 0.01, head_width=2, head_length=0.002, fc='k', ec='k')
#plt.arrow(mu-3*sigma, 0, 0.0, 0.01, head_width=2, head_length=0.002, fc='k', ec='k')
#plt.text(mu-3*sigma-4, 0.0125, u'-3$\sigma$')
#plt.text(mu+3*sigma-4, 0.0125, u'+3$\sigma$')
#plt.xlim(mu-6*sigma,mu+6*sigma)
# Tweak spacing to prevent clipping of ylabel
plt.ylim(-10,110)
plt.subplots_adjust(left=0.15)
plt.show()