#!/usr/bin/env python

import numpy as np

w1 = -6.90675478
w2 = 0.40546511

def logistic(x):
    return 1 / (1 + np.exp(-x));

# NB: h1=0, h2=1, v=1

# Q2: what is P(v=1 | h1=0,h2=1)
P = logistic(0*w1 + 1*w2)
print('Q2: P(v=1 | h1=0,h2=1) = {}'.format(P))

# Q3: what is P(h1=0,h2=1,v=1)
# **marginal probability** of h1=0 = h1=1 = h2=0 = 0.5
P = logistic(0*w1 + 1*w2) * 0.5 * 0.5
print('Q3: P(h1=0,h2=1,v=1) = {}'.format(P))

# Q4: what is ∂log⁡P(C011) / ∂w1?
P = 1 * (logistic(w1))
print('Q4: ∂log⁡P(C011) / ∂w1 = {}'.format(P))

# Q5: what is ∂log⁡P(C011) / ∂2?
P = 1 * (1 - logistic(w2))
print('Q5: ∂log⁡P(C011) / ∂w2 = {}'.format(P))

# new weights
w1 = 10
w2 = -4

# Q6: what is P(h2=1 | v=1,h1=0)
# P(v=1|h1=1,h2=1) = P111 = logistic(1*w1+1*w2)
# P(v=1|h1=1,h2=0) = P110 = logistic(1*w1+0*w2)
# P(h1=0) = P(h1=1) = P(h2=1) = 0.5
# P101*P(h1=0)*P(h2=1) / (P101*P(h1=0)*P(h2=1) + P100*P(h1=0)*P(h2=0))

P101 = logistic(0*w1 + 1*w2)
P100 = logistic(0*w1 + 0*w2)
P = (P101 * 0.5 * 0.5 / (P101 * 0.5 * 0.5 + P100 * 0.5 * 0.5))
print('Q6: P(h2=1 | v=1,h1=0) = {}'.format(P))

# Q7: what is P(h2=1 | v=1,h1=1)
P111 = logistic(1*w1+1*w2)
P110 = logistic(1*w1+0*w2)
P = (P111 * 0.5 * 0.5 / (P111 * 0.5 * 0.5 + P110 * 0.5 * 0.5))
print('Q7: P(h2=1 | v=1,h1=1) = {}'.format(P))


