#!/bin/bash

for cpu in cortex-a57 cortex-a72 neoverse-n1 neoverse-v1 max
do
	python3 parse-bsa-log.py  logs/bsa-${cpu}-v1.log $cpu
	python3 parse-bsa-log.py  logs/bsa-sbsa-${cpu}-v1.log $cpu

	for level in 3 4 5 6 7
	do
		python3 parse-sbsa-log.py logs/sbsa-${cpu}-${level}-v1.log $cpu $level
	done
done
