#!/bin/bash

graphFiles=`ls ./data/ | grep .graph`

for graph in ${graphFiles}
do
	RANDOM=$(date +%s)
	echo ${graph}
	echo  ${RANDOM}
	
	python ./code/main.py -inst ${graph} -alg Approx -time 600 -seed ${RANDOM}
	for t in {20..100..20}
		do
			python ./code/main.py -inst ${graph} -alg LS1 -time ${t} -seed ${RANDOM}	
			python ./code/main.py -inst ${graph} -alg LS2 -time ${t} -seed ${RANDOM}
		done
	python ./code/main.py -inst ${graph} -alg bnb -time 600
done
