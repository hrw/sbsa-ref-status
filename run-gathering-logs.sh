#!/bin/bash

boot-sbsa-ref() {

qemu_args=(

-machine sbsa-ref
-m 4096
-smp 2
-cpu $cpu

# firmware
-drive if=pflash,file=firmware/SBSA_FLASH0.fd,format=raw
-drive if=pflash,file=firmware/SBSA_FLASH1.fd,format=raw

# basic disk with EFI apps and generic Debian d-i
-drive file=fat:rw:$PWD/disks/virtual/,format=raw

# usb for graphical console
-usb
-device usb-kbd
-device usb-tablet

-nographic

-watchdog-action none

# exit instead of rebooting
-no-reboot

# have a way to check internals
-monitor telnet::45454,server,nowait

# output on console
-serial stdio

# some PCIe switch with ac97 behind it
-device pcie-root-port,id=root_port_for_switch1,chassis=1,slot=12
  -device x3130-upstream,id=upstream_port1,bus=root_port_for_switch1
    -device xio3130-downstream,id=downstream_port1,bus=upstream_port1,chassis=1,slot=20
      -device ac97,bus=downstream_port1

# NVME card
-device pcie-root-port,id=root_port_for_nvme1,chassis=1,slot=1
 -device nvme,serial=deadbeef,bus=root_port_for_nvme1

# Intel network card
-device pcie-root-port,id=root_port_for_igb,chassis=1,slot=2
  -device igb,bus=root_port_for_igb

# XHCI USB card
-device pcie-root-port,id=root_port_for_xhci,chassis=1,slot=3
  -device qemu-xhci,bus=root_port_for_xhci

# AC97
-device pcie-root-port,id=root_port_for_ac97,chassis=1,slot=97
  -device ac97,bus=root_port_for_ac97

# PCIe-PCI bridge with virtio-rng behind
-device pcie-root-port,id=root_port_for_pci,chassis=1
  -device pcie-pci-bridge,id=pci,bus=root_port_for_pci
    -device virtio-rng-pci,bus=pci,addr=8
)

echo "QEMU command line arguments:"
echo "${qemu_args[@]}" | sed -e "s/ -/\n-/g"
echo ""

echo "mode 100 31"  > disks/virtual/startup.nsh
echo "pci"         >> disks/virtual/startup.nsh
echo "$1"          >> disks/virtual/startup.nsh
echo "reset -c"    >> disks/virtual/startup.nsh

echo "EFI startup script:"
cat disks/virtual/startup.nsh
echo ""

# strip TF-A messages on system poweroff
timeout --foreground 1m ../code/qemu/build/qemu-system-aarch64 "${qemu_args[@]}" | grep -v "Node :"
}

for cpu in cortex-a57 cortex-a72 neoverse-n1 neoverse-v1 neoverse-n2 max
do
        printf "Run tests for %11b: " $cpu

        echo -n "BSA normal"
        boot-sbsa-ref "fs0:bsa.efi"            > logs/bsa-${cpu}.log
        echo -n "/v "
        boot-sbsa-ref "fs0:bsa.efi -v 1"       > logs/bsa-${cpu}-v1.log

        echo -n "BSA -sbsa"
        boot-sbsa-ref "fs0:bsa.efi -sbsa"      > logs/bsa-sbsa-${cpu}.log
        echo -n "/v "
        boot-sbsa-ref "fs0:bsa.efi -sbsa -v 1" > logs/bsa-sbsa-${cpu}-v1.log

        echo -n "SBSA level "
        for level in 4 5 6 7
        do
                echo -n $level
                boot-sbsa-ref "fs0:sbsa.efi -only -skip 861 -l ${level}"      > logs/sbsa-${cpu}-${level}.log
                echo -n "/v "
                boot-sbsa-ref "fs0:sbsa.efi -only -skip 861 -l ${level} -v 1" > logs/sbsa-${cpu}-${level}-v1.log
        done

        echo -n "future"
        boot-sbsa-ref "fs0:sbsa.efi -only -skip 861 -fr"      > logs/sbsa-${cpu}-future.log
        echo -n "/v "
        boot-sbsa-ref "fs0:sbsa.efi -only -skip 861 -fr -v 1" > logs/sbsa-${cpu}-future-v1.log

        echo -n "ACPI tables "
        boot-sbsa-ref "acpiview" > logs/acpiview-${cpu}.log

        echo -n "CPU info "
        boot-sbsa-ref "fs0:armcpuinfo.efi" > logs/cpuinfo-${cpu}.log

        echo -n "Linux "
        boot-sbsa-ref "fs0:\efi\debian\linux initrd=\efi\debian\tiny-initrd-show-cpuinfo.img printk.time=0" > logs/linux-${cpu}.log

        echo ""
done

rm disks/virtual/startup.nsh
