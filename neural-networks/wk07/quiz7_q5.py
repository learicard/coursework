#!/usr/bin/env python
"""
Quiz 7 question 5
"""
import numpy as np

def sigma(k):
    return 1/(1+np.exp(-k))

x = [1, 0, 0, 0]
t = [0, 0, 0, 0.5]

wxh = 1
whh = -2
why = 1

hbias = 0
ybias = 0

# forward pass
z0 = wxh*x[0] + hbias
h0 = sigma(z0)
z1 = wxh*x[1] + whh*h0 + hbias
h1 = sigma(z1)
z2 = wxh*x[2] + whh*h1 + hbias
h2 = sigma(z2)
z3 = wxh*x[3] + whh*h2 + hbias
h3 = sigma(z3)
y3 = why*h3 + ybias
E3 = 0.5*(t[3] - y3)**2
