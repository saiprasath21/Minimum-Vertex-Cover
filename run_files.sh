#!/bin/bash

graphFiles=`ls ./data/ | grep .graph`

for graph in ${graphFiles}
do
	RANDOM=$(date +%s)
	R=$(($RANDOM%10+1))
	echo ${graph}
	echo ${RANDOM}
	
	python ./code/main.py -inst ${graph} -alg Approx -time 600 -seed $R
	for t in {20..100..20}
		do
			python ./code/main.py -inst ${graph} -alg LS1 -time $t -seed $R	
			python ./code/main.py -inst ${graph} -alg LS2 -time $t -seed $R
		done
	python ./code/main.py -inst ${graph} -alg bnb -time 600
done
