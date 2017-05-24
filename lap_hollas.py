#!/usr/bin/env python3
import numpy as np
import scipy.optimize as opt

cost_file = 'cost_matrix.dat'

cost_matrix = np.loadtxt(cost_file)

print("Input cost matrix")
print(cost_matrix)

# The scipy function computes minimum, but we want maximum
cost_matrix = -cost_matrix
row_ind, col_ind = opt.linear_sum_assignment(cost_matrix)

solution = cost_matrix[row_ind, col_ind].sum()

print("Column indeces: (corresponding row indeces are in ascending order)")
print(col_ind)

print("Maximum sum = ", str(-solution))
