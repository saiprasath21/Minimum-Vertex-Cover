#!/bin/bash

graphFiles=`ls ./data/ | grep .graph`

for graph in ${graphFiles}
do
	echo ${graph}
	python ./code/main.py -inst ${graph} -alg Approx -time 600 -seed 10
	for t in {20..100..20}
		do
			python ./code/main.py -inst ${graph} -alg LS1 -time ${t} -seed 10	
			python ./code/main.py -inst ${graph} -alg LS2 -time ${t} -seed 10
		done
	python ./code/main.py -inst ${graph} -alg bnb -time 600
done
