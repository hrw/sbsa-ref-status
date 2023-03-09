#!/bin/bash

for cpu in cortex-a57 cortex-a72 neoverse-n1 max
do
	./boot-sbsa-ref.sh $cpu nogfx "fs0:bsa.efi" 2>&1 |grep -v " Node :" | tee logs/bsa-${cpu}.log
	./boot-sbsa-ref.sh $cpu nogfx "fs0:bsa.efi -v 1" 2>&1 |grep -v " Node :" | tee logs/bsa-${cpu}-v1.log

	./boot-sbsa-ref.sh $cpu nogfx "fs0:bsa.efi -sbsa" 2>&1 |grep -v " Node :" | tee logs/bsa-sbsa-${cpu}.log
	./boot-sbsa-ref.sh $cpu nogfx "fs0:bsa.efi -sbsa -v 1" 2>&1 |grep -v " Node :" | tee logs/bsa-sbsa-${cpu}-v1.log

	for level in 3 4 5 6 7
	do
		./boot-sbsa-ref.sh $cpu nogfx "fs0:sbsa.efi -l ${level}" 2>&1 |grep -v " Node :" | tee logs/sbsa-${cpu}-${level}.log
		./boot-sbsa-ref.sh $cpu nogfx "fs0:sbsa.efi -l ${level} -v 1" 2>&1 |grep -v " Node :" | tee logs/sbsa-${cpu}-${level}-v1.log
	done

	./boot-sbsa-ref.sh $cpu nogfx "acpiview" 2>&1 |grep -v " Node :" | tee logs/acpiview-${cpu}.log
done
