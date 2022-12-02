#!/bin/bash

graphFiles=`ls ./data/ | grep .graph`

for graph in ${graphFiles}
do
	echo ${graph}
	python ./Code/main.py -inst ${graph} -alg Approx -time 600 -seed 10
	for t in {20..101..20}
		do
			python ./Code/main.py -inst ${graph} -alg LS1 -time 20 -seed 10	
			python ./Code/main.py -inst ${graph} -alg LS2 -time 20 -seed 10
		done
	python ./Code/main.py -inst ${graph} -alg bnb -time 600
done
