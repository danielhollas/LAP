#!/usr/bin/env python3
import numpy as np
try:
    import scipy.optimize as opt
except:
    print("Scipy module not found :(")
import argparse
import sys

def read_cmd():
   """A function for reading command line options."""
   desc = "A simple LAP solver."
   parser = argparse.ArgumentParser(description=desc)
   parser.add_argument('input_file',metavar="Input_file",default='cost_matrix.dat',
         help='Text file containing input cost matrix.')
   parser.add_argument('-a','--algoritm',dest='alg',default='scipy',required = False,
         help='LAP algoritm. (scipy or max_heur)')
   return parser.parse_args()


def hungary(cost):
   """Use Hungarian algorithm implemented in scipy."""
   # The scipy function computes minimum, but we want maximum
   cost = -cost
   return opt.linear_sum_assignment(cost)


def solve_matrix_2x2(cost):
   nrow = cost.shape[0]
   ncol = cost.shape[1]
   if nrow != 2 and ncol != 2:
      print("ERROR: solve_matrix_2x2 only work for 2x2 matrices!")
      sys.exit(1)
   sum1 = cost[0][1] + cost[1][0]
   sum2 = cost[0][0] + cost[1][1]
   return (0, 1) if sum1 > sum2 else (1,0)


def get_original_index(row_ind, col_ind, rows, cols):
   """See function max_heuristic to make sense of this"""
   if len(rows) == 0:
      return row_ind, col_ind

   for r in sorted(rows):
      if row_ind >= r:
         row_ind += 1

   for c in sorted(cols):
      if col_ind >= c:
         col_ind += 1

   return row_ind, col_ind


def max_heuristic(cost):
   """Simply go for the maximum values!"""
   nrow = cost.shape[0]
   ncol = cost.shape[1]

   unique_rows = []
   unique_cols = []
   # Could do this recursively, but that would probably fail for large matrices
   for r in range(ncol):
      # Get maximum for each row
      maximums = cost.max(axis=1)
      # Indexes of the maxima, indicating columns
      col_inds = cost.argmax(axis=1)

      # Select the row with the biggest maximum
      # (take the first one if they are the same)
      row_ind = maximums.argmax()
      col_ind = col_inds[row_ind]

#      if len(cost) == 2: # Solve this case exacly
#         row_ind, col_ind = solve_matrix_2x2(cost)

      # We are iteratively slicing the matrix
      # Taking the maximum value at each step
      # Delete row
      cost = np.delete(cost,row_ind, axis=0)
      # Delete column
      cost = np.delete(cost,col_ind, axis=1)

      # Need to reindex, since we are changing the size of the matrix
      row_ind, col_ind = get_original_index(row_ind, col_ind, unique_rows, unique_cols)
      unique_rows.append(row_ind)
      unique_cols.append(col_ind)

      print(cost, len(cost))

   return unique_rows, unique_cols



opts = read_cmd()
cost_file = opts.input_file
algorithm = opts.alg

cost_matrix = np.loadtxt(cost_file)
solution = 0.0

print("Input cost matrix")
print(cost_matrix)

# Sanity check
if len(cost_matrix) == 0:
   print("ERROR: empty matrix")
   sys.exit(1)

if cost_matrix.ndim != 2:
   print("ERROR: non-2d matrix detected")
   sys.exit(1)

nrow = cost_matrix.shape[0]
ncol = cost_matrix.shape[1]
if nrow != ncol:
   print("ERROR: Non-rectagular matrix detected!")
   sys.exit(1)

# Here we go
if algorithm == 'scipy':
   row_ind, col_ind = hungary(cost_matrix)

elif algorithm == 'max_heur':
   row_ind, col_ind = max_heuristic(cost_matrix)

else:
   print("ERROR: Invalid algoritm.")


print("Column indeces:")
print(col_ind)
print("Row indeces:")
print(row_ind)

solution = cost_matrix[row_ind, col_ind].sum()

print("Maximum sum = ", str(solution))
