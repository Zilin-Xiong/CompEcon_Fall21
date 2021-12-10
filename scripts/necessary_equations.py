import numpy as np


def get_L(n): 
    
    '''
    Function to compute aggregate
    labor supplied
    '''
    L = n.sum()
    return L

def get_K(b): 
    
    '''
    Function to compute aggregate
    capital supplied
    '''
    K = b.sum()
    return K

#Firms
def get_r(K, L, params):
    '''
    Compute the interest rate from
    the firm's FOC
    '''
    alpha, delta, A = params

    r = alpha * A * (L / K) ** (1 - alpha) - delta
    return r

def get_w(r, params):
    '''
    Solve for the w that is consistent
    with r from the firm's FOC
    '''
    alpha, delta, A = params
    w = (1 - alpha) * A * ((alpha * A) / (r + delta)) ** (alpha / (1 - alpha))
    return w


# Household
def get_c(r, w, b_s, b_sp1, n_s):
    '''
    Find consumption using the budget constraint
    and the choice of savings (b_sp1) -- for equation (4.6)
    '''
    c= np.dot(r+1,b_s) + np.dot(w, n_s) - b_sp1
    # c = ((1 + r) * b_s) + (w * n_s) - b_sp1
    return c

def mu_c_func(c, sigma):
    '''
    Marginal utility of consumption
    '''
    mu_c = c ** -sigma
    
    
    return mu_c

def mu_n_func(n, chi, b, l_tilde, v):
    '''
    Marginal disutility of labor supply -- for equation (4.9)
    '''
    mu_n = chi * (b / l_tilde) * ((n / l_tilde) ** (v - 1)) * (1 - ((n/l_tilde) ** v)) ** ((1 - v) / v)
    return mu_n


def hh_foc(bn_list, r, w, params):
    '''
    Define the household first order conditions
    '''
    sigma, v, S, chi, b, l_tilde, beta = params

    # bn_list = np.zeros((2 * S -1), dtype=int)
    b_s = bn_list[0:S] # from period 0 to 50
    b_s[0] = 0
    b_sp1 = bn_list[1:S+1] # from period 1 to 50
    b_sp1[-1] = 0
    n_s = bn_list[S+1:2*S+1]
    c = get_c(r, w, b_s, b_sp1, n_s)
    mu_c = mu_c_func(c, sigma)
    mu_n = mu_n_func(chi, b, l_tilde, n_s, nu)
    euler_error_c = mu_c[:-1] - beta * (1+r) * mu_c[1:]
    euler_error_n = w * mu_c - mu_n
    return euler_error_c, euler_error_n