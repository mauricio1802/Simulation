from random import random
from math import log

def get_exp(c):
    u = random()
    return -c*log(u)

def get_uniform(a=0, b = 1):
    return (b-a)*random()+a