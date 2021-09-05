##calculator
import math as mt
##sum of two
def sum_of_two(x,y):
    num_of_two1 = [x,y]
    return sum(num_of_two1)

##product of two
def pro_of_two(x,y):
    return x*y

##sqrt
def sqrt_of_sum(x):
    return mt.sqrt(x)

if __name__== "__main__":
    print(sum_of_two(1,3))
    pro_of_two(5,6)
    sqrt_of_sum(6)