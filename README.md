# LAP
Linear Assignment Problem

Solution to the Linear Assigment Problem as required by a job application, described here:
http://cosmo.epfl.ch/cms/lang/en/pid/127501

To obtain the exact solution using the Hungarian algorithm implemented in SciPy, use:

./lap_hollas.py cost_matrix.py


I have also implemented a very primitive heuristic algorithm,
which recursively takes the maximum value from the matrix.
./lap_hollas.py cost_matrix.py -a max_heur

As it happens, it gives the correct answer for this particular cost matrix.

----------------------
General info about LAP:
https://en.wikipedia.org/wiki/Assignment_problem

Reference implementation of entropy-regularize solution
(see http://papers.nips.cc/paper/4927-sinkhorn-distances-lightspeed-computation-of-optimal-transport.pdf)

http://cosmo.epfl.ch/files/content/sites/cosmo/files/data/lap.zip
