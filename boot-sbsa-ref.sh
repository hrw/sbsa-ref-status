#!/bin/bash

cpu="max"
extra_opts=""

if [ ! -z $1 ]; then
        cpu=$1
fi

if [ ! -z $2 ]; then
        extra_opts="-nographic"
fi

if [ ! -z "$3" ]; then
        echo "mode 100 31" > disks/virtual/startup.nsh
        echo "pci"        >> disks/virtual/startup.nsh
        echo "$3"         >> disks/virtual/startup.nsh
    if [ -z "$4" ]; then
        echo "reset -c"   >> disks/virtual/startup.nsh
    fi
fi

qemu_args=(

-machine sbsa-ref
-m 4096
-smp 4
-cpu $cpu

# firmware
-drive if=pflash,file=SBSA_FLASH0.fd,format=raw
-drive if=pflash,file=SBSA_FLASH1.fd,format=raw

# basic disk with EFI apps and generic Debian d-i
#-drive file=fat:rw:$PWD/disks/virtual/,format=raw

# full Debian installation
-drive format=qcow2,file=$PWD/../disks/full-debian.qcow2

# Debian install ISO
#-drive if=ide,file=$PWD/../disks/debian-bookworm.iso,format=raw,media=cdrom

# userspace networking
-net nic
-net user

# usb for graphical console
-usb
-device usb-kbd
-device usb-tablet

# any extra options set by script above
$extra_opts

-watchdog-action none

# exit instead of rebooting
-no-reboot

# have a way to check internals
-monitor telnet::45454,server,nowait

# output on console
-serial stdio

# --------------------------------------------------------------------------------------
# now some PCIe stuff I normally do not use
# --------------------------------------------------------------------------------------

# some PCIe switch with ac97 behind it
# -device pcie-root-port,id=root_port_for_switch1,chassis=1,slot=12
#   -device x3130-upstream,id=upstream_port1,bus=root_port_for_switch1
#     -device xio3130-downstream,id=downstream_port1,bus=upstream_port1,chassis=1,slot=20
#       -device ac97,bus=downstream_port1

# NVME card
# -device pcie-root-port,id=root_port_for_nvme1,chassis=1,slot=1
#   -device nvme,serial=deadbeef,drive=nvme,bus=root_port_for_nvme1

# PCIe-PCI bridge with virtio-rng behind
# -device pcie-root-port,id=root_port_for_pci,chassis=1,slot=2
#   -device pcie-pci-bridge,id=pci,bus=root_port_for_pci
#     -device virtio-rng-pci,bus=pci,addr=8

# another PCIe bus
# -device pxb-pcie,id=pxb1,bus_nr=2
#   -device pcie-root-port,id=root_port_for_ahci,bus=pxb1,chassis=2,slot=1
#     -device ahci,bus=root_port_for_ahci


# --------------------------------------------------------------------------------------
# some random disks/isos
# --------------------------------------------------------------------------------------

# direct use of USB pendrive
# -drive if=ide,format=raw,file=/dev/sdc

# -drive if=ide,format=raw,media=cdrom,file=disks/debian-bookworm-DI-alpha2-arm64-netinst.iso
# -drive file=disks/alpine-standard-3.17.2-aarch64.iso,format=raw,media=cdrom

# -drive if=ide,format=raw,file=disks/luv-live-image-gpt.img
)

./code/qemu/build/aarch64-softmmu/qemu-system-aarch64 ${qemu_args[@]}

if [ ! -z "$3" ]; then
        rm disks/virtual/startup.nsh
fi
