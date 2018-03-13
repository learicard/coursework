#!/usr/bin/env python
"""
Quiz 7 question 4
"""
import numpy as np

def sigma(k):
    return 1/(1+np.exp(-k))

x = [18, 9, -8]
h = [0.2, 0.4, 0.8]
y = [0.05, 0.1, 0.2]
t = [0.1, -0.1, -0.2]

wxh = -0.1
whh = 0.5
why = 0.25

hbias = 0.4
ybias = 0

# forward pass
z0 = wxh*x[0] + hbias
h0 = sigma(z0)

z1 = wxh*x[1] + whh*h0 + hbias
h1 = sigma(z1)

z2 = wxh*x[2] + whh*h1 + hbias
h2 = sigma(z2)
y2 = why*h2 + ybias
E2 = 0.5*(t[2] - y[2])**2
