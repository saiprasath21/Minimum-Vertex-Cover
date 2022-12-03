#!/bin/bash
graphFiles=`ls ./DATA/ | grep .graph`
# echo ${graphFiles}
for graph in ${graphFiles}
	do
	echo ${graph}
	python ./code/main.py -inst ${graph} -alg BnB -time 300
	python ./code/main.py -inst ${graph} -alg Approx -time 300
	for t in {20..100..20}
		do
		for i in {1,2,3,4,5}
			do
			python ./code/main.py -inst ${graph} -alg LS1 -time ${t} -seed ${i}	
			python ./code/main.py -inst ${graph} -alg LS2 -time ${t} -seed ${i}
			done
		done
	done
