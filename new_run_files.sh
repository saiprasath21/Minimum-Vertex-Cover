#!/bin/bash
graphFiles=`ls ./DATA/ | grep .graph`
# echo ${graphFiles}
for graph in ${graphFiles}
	do
	echo ${graph}
	for t in {20..100..20}
		do
		for i in {1,2,3,4,5}
			do
			RANDOM=$(date +%s)
			R=$(($RANDOM%10+1))
			echo ${RANDOM}
			python3 ./code/main.py -inst ${graph} -alg LS1 -time $t -seed $R	
			python3 ./code/main.py -inst ${graph} -alg LS2 -time $t -seed $R
			done
		done
	python3 ./code/main.py -inst ${graph} -alg bnb -time 600
	python3 ./code/main.py -inst ${graph} -alg Approx -time 600
	done