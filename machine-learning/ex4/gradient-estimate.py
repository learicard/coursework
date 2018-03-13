#!/usr/bin/env python

# gradient estimation:
# j(theta) == theta**3
theta = 1
epsilon = 0.01

((theta+epsilon)**3 - (theta-epsilon)**3) / (2*epsilon)

# approximation = 3.0001
