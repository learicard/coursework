#!/usr/bin/env python
"""
Quiz 7 question 3
"""
import numpy as np

def sigma(k):
    return 1/(1+np.exp(-k))

x = [9, 4, -2]

wxh = 0.5
whh = -1.0
why = -0.7

hbias = -1.0
ybias = 0

# forward pass
z0 = wxh*x[0] + hbias
h0 = sigma(z0)
z1 = wxh*x[1] + whh*h0 + hbias
h1 = sigma(z1)
z2 = wxh*x[2] + whh*h1 + hbias
h2 = sigma(z2)
