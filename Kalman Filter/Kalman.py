#!/usr/bin/python3
# -*- coding: utf-8 -*-


from pykalman import KalmanFilter
import matplotlib.pyplot as plt
import numpy
import random


N = 3 * 500
sigma = 0.7

# Function to estimate
W = numpy.zeros(N)
W[0    : 500  ] = 1
W[500  : 1000 ] = 3
W[1000 : 1500 ] = 2

# Generate noisy measures
X = numpy.zeros(N)
for i in range(N):
    X[i] = W[i] + random.gauss(0, sigma)


kf = KalmanFilter(initial_state_mean=X[0], n_dim_obs=1)
kf.transition_covariance = 1e-3
Z = kf.em(X).smooth(X)[0]
#Z = kf.smooth(X)[0]


plt.figure(1)
plt.plot( X, 'r:' )
plt.plot( W, 'b-' )
plt.plot( Z, 'g-' )
plt.show()

