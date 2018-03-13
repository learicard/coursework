# ml exam

# q10:

w1 = 1
w2= -1.5
b = -0.5

# what is P(h=1 | v1=0,v2=1)

# P(h=1|v1=1,v2=1) = P111 = logistic(1*w1+1*w2)
# P(h=1|v1=1,v2=0) = P110 = logistic(1*w1+0*w2)
# P(h1=0) = P(h1=1) = P(h2=1) = 0.5
# P101*P(h1=0)*P(h2=1) / (P101*P(h1=0)*P(h2=1) + P100*P(h1=0)*P(h2=0))

P101 = logistic(0*w1 + 1*w2)
P100 = logistic(0*w1 + 0*w2)
P = (P101 * 0.5 * 0.5 / (P101 * 0.5 * 0.5 + P100 * 0.5 * 0.5))
print('Q10: P(h2=1 | v1=0,v2=1) = {}'.format(P))


# q 11:

# input x=1, target t=5, input-to-hidden weight w1=1.0986123, 
# hidden-to-output weight w2=4, no bias. 
# Calculate squared error cost=1/2(y−t)**2. 
# hidden neuron is logistic

def logistic(x):
    return 1 / (1 + np.exp(-x))

w1 = 1.0986123
w2 = 4
t = 5
x = 1

y = logistic(1*w1)*4

error = 1.0/2*(y-t)**2

error_deriv = x*4*y*(1-y)*(y-t)

print('Q11: ')