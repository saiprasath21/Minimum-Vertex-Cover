# CSE 6140 Group Project - Minimum Vertex Cover

## Dir/Files in the Repo:

1. **code** - Contains the python codes for the four algorithms: BnB, Approx, LS1 (Simuated Annealing), and LS2 (Hill Climbing)

2. **output** - contains the solution and trace files for the four algorithms across 11 graphs from the 10th DIMACS challenge

3. **run_files.sh** - Bash file to execute the algorithms with different graphs and input parameters

## Additional Packages:

Our code uses Python 3.7

For running the codes, you will need to install the following libraries:
* networkx
* time
* random
* numpy

## Executing the files:

Run specific files and input parameters:
```
$ main.py -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>
```
Run all the files using the bash file:
```
$ bash run_files.sh
```
