#!/bin/bash

graphFiles=`ls ./data/ | grep .graph`

for graph in ${graphFiles}
do
	echo ${graph}
	python ./src/main.py -inst ${graph} -alg Approx -time 20 -seed 10
	python ./src/main.py -inst ${graph} -alg LS2 -time 20 -seed 10
done

