import SS as SS
import numpy as np



# Set parameters
alpha = 0.3
delta = 0.1
A = 1.0
sigma = 1.5
beta = 0.8
b = 0.501
v = 1.554
l_tilde = 1
# Make initial guess for this labor working 50 years
S = 50
chi = np.ones(S)

# Make initial guesses
r_guess = 0.1
b_guess = [0.01]*(S-1)
n_guess = [0.2]*S
bn_guesses = b_guess + n_guess

r, b, success, euler_errors = SS.ss_solver(r_guess, bn_guesses, alpha, delta, A, 
                                         sigma, chi, l_tilde, v, b, beta, S)

print('The SS interest is ', r_ss, 'Did we find the solution? ', success)
print('The Euler errors are ', euler_errors)