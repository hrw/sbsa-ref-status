#!/bin/bash

for cpu in cortex-a57 cortex-a72 neoverse-n1 max
do
	printf "Run tests for %11b: " $cpu

	echo -n "BSA normal"
	./boot-sbsa-ref.sh $cpu nogfx "fs0:bsa.efi" 2>&1 |grep -v " Node :" > logs/bsa-${cpu}.log
	echo -n "/v "
	./boot-sbsa-ref.sh $cpu nogfx "fs0:bsa.efi -v 1" 2>&1 |grep -v " Node :" > logs/bsa-${cpu}-v1.log

	echo -n "BSA -sbsa"
	./boot-sbsa-ref.sh $cpu nogfx "fs0:bsa.efi -sbsa" 2>&1 |grep -v " Node :" > logs/bsa-sbsa-${cpu}.log
	echo -n "/v "
	./boot-sbsa-ref.sh $cpu nogfx "fs0:bsa.efi -sbsa -v 1" 2>&1 |grep -v " Node :" > logs/bsa-sbsa-${cpu}-v1.log

	echo -n "SBSA level "
	for level in 3 4 5 6 7
	do
		echo -n $level
		./boot-sbsa-ref.sh $cpu nogfx "fs0:sbsa.efi -skip 861 -l ${level}" 2>&1 |grep -v " Node :" > logs/sbsa-${cpu}-${level}.log
		echo -n "/v "
		./boot-sbsa-ref.sh $cpu nogfx "fs0:sbsa.efi -skip 861 -l ${level} -v 1" 2>&1 |grep -v " Node :" > logs/sbsa-${cpu}-${level}-v1.log
	done

	echo "ACPI tables"
	./boot-sbsa-ref.sh $cpu nogfx "acpiview" 2>&1 |grep -v " Node :" > logs/acpiview-${cpu}.log
done
