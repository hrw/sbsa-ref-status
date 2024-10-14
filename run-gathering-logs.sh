#!/bin/bash

boot-sbsa-ref() {

# strip TF-A messages on system poweroff
timeout --foreground 1m ./boot-sbsa-ref.py --cpu $cpu --cmd "$1" | grep -v "Node :"

}

for cpu in cortex-a57 cortex-a72 neoverse-n1 neoverse-v1 neoverse-n2 max
do
        printf "Run tests for %11b: " $cpu

        echo -n "BSA normal"
        boot-sbsa-ref "fs1:bsa.efi"            > logs/bsa-${cpu}.log
        echo -n "/v "
        boot-sbsa-ref "fs1:bsa.efi -v 1"       > logs/bsa-${cpu}-v1.log

        echo -n "BSA -sbsa"
        boot-sbsa-ref "fs1:bsa.efi -sbsa"      > logs/bsa-sbsa-${cpu}.log
        echo -n "/v "
        boot-sbsa-ref "fs1:bsa.efi -sbsa -v 1" > logs/bsa-sbsa-${cpu}-v1.log

        echo -n "SBSA level "
        for level in 3 4 5 6 7
        do
                echo -n $level
                boot-sbsa-ref "fs1:sbsa.efi -only -skip 861 -l ${level}"      > logs/sbsa-${cpu}-${level}.log
                echo -n "/v "
                boot-sbsa-ref "fs1:sbsa.efi -only -skip 861 -l ${level} -v 1" > logs/sbsa-${cpu}-${level}-v1.log
        done

        echo -n "future"
        boot-sbsa-ref "fs1:sbsa.efi -only -skip 861 -fr"      > logs/sbsa-${cpu}-future.log
        echo -n "/v "
        boot-sbsa-ref "fs1:sbsa.efi -only -skip 861 -fr -v 1" > logs/sbsa-${cpu}-future-v1.log

        echo -n "ACPI tables "
        boot-sbsa-ref "acpiview" > logs/acpiview-${cpu}.log

        echo -n "CPU info "
        boot-sbsa-ref "fs1:armcpuinfo.efi" > logs/cpuinfo-${cpu}.log

        echo -n "Linux "
        boot-sbsa-ref "fs1:\efi\debian\linux initrd=\efi\debian\tiny-initrd-show-cpuinfo.img printk.time=0" > logs/linux-${cpu}.log

        echo ""
done

rm disks/virtual/startup.nsh
