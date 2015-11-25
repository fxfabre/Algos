#!/usr/bin/python3
# -*- coding: utf-8 -*-


import math
import random
import numpy as np
import matplotlib


A = 7
B = 87
NB_TIRAGES = 100*1000

"""
Suppose we can generate a uniform density in [[0, A-1]].
From it, generate a uniform density in [[0, B-1]]
"""

def getUniformA( n ):
    return random.randint(0, n-1)

def getUniformB(a, b):
    """
        Comments with a = 7, b = 83
    """
    ## Generate a random number between 0 and 7**3 = 343
    generated = 0
    nbIter = math.ceil(math.log(b, a))
    for i in range( nbIter ):
        generated = generated * a + getUniformA( a )
    # Here generated is a number between 0 and A**nbIter,
    # nbIter is such that A**nbIter >= B

    # Generate the larger multiple of 83, smaller than 343 :
    # 332 = 4 x 83 = 343 - ( 343 % 11 )
    largerMultipleOfB = a**nbIter - (a**nbIter % b)

    # 2 diffrent cases :
    # 0 < generated number < 332 = 4 x 83 = largerMultipleOfB
    #   => return generated number % 83 = uniform density between 0 and 82
    # generated number > 332 :
    #   => run the algorithm again. ie : recursive call to generate a new number.
    nbGeneration = 0
    if generated >= largerMultipleOfB:
        generated, nbGeneration = getUniformB(a,b)
    return generated % b, nbGeneration+1


# View uniform law between 0 and N:
observations = np.zeros(A)
for i in range(NB_TIRAGES):
    randNbr = getUniformA(A)
    observations[randNbr] += 1
print( observations / observations.mean() )
print( "Standard deviation: {0}".format((observations / observations.mean()).std()) )


# Test uniformity / uniformness ?
observations = np.zeros(B)
nbGenerations = np.zeros(50)
for i in range(NB_TIRAGES):
    randNbr, nbGeneration = getUniformB(A, B)
    observations[randNbr] += 1
    if nbGeneration < 50:
        nbGenerations[ nbGeneration ] += 1
print( observations )
print( "Standard deviation : {0}".format((observations / observations.mean()).std()) )

# TODO : chi-2 test

# Compute esperance : average number of random generation to get a good number :
expectation = 0
for i, x in enumerate(nbGenerations):
    expectation += i * x
print("Average number of random generaton required : {0}".format(expectation/NB_TIRAGES))



