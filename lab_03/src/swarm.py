import numpy as np
import pyswarms as ps
from pyswarms.utils.functions import single_obj as f
from pyswarms.utils.search import RandomSearch
import logging
x = []
y = []
def fitness_func(values):
    res = [np.mean(np.abs(np.polyval(coeffs, x) - y)) for coeffs in values]
    return res

def RunSwarm(xv, yv, dimension, iters = 100):
    global x
    global y
    x = list(xv)
    y = list(yv)
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}           
    optimizer = ps.single.GlobalBestPSO(n_particles=100, dimensions=dimension, options=options)

    cost, pos = optimizer.optimize(fitness_func, iters=iters, verbose= False)
    return pos
