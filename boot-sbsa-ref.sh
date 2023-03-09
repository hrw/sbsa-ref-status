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
	echo "$3"        > disks/virtual/startup.nsh
	echo "reset -c" >> disks/virtual/startup.nsh
fi

./code/qemu/build/aarch64-softmmu/qemu-system-aarch64 \
-machine sbsa-ref \
-m 4096 \
-smp 4 \
-cpu $cpu \
\
-drive if=pflash,file=SBSA_FLASH0.fd,format=raw \
-drive if=pflash,file=SBSA_FLASH1.fd,format=raw \
\
\
-drive file=fat:rw:$PWD/disks/virtual/,format=raw \
\
-usb \
-device usb-kbd \
-device usb-tablet \
\
$extra_opts \
\
-watchdog-action none \
-no-reboot \
-monitor telnet::45454,server,nowait \
-serial stdio

if [ ! -z "$3" ]; then
	rm disks/virtual/startup.nsh
fi

exit

# here go any qemu arguments I may find useful at some time of testing

-drive if=ide,format=raw,file=/dev/sdc \
-drive if=ide,format=raw,file=disks/debian-usb.img \
-drive if=ide,format=raw,media=cdrom,file=disks/debian-bookworm-DI-alpha2-arm64-netinst.iso \
-drive file=disks/alpine-standard-3.17.2-aarch64.iso,format=raw,media=cdrom \

-drive if=ide,format=raw,file=disks/luv-live-image-gpt.img \

-cpu max,sve512=on \

-device pcie-root-port,id=root_port_1.1,chassis=1,slot=1  \
  -device nvme,serial=deadbeef,drive=nvme,bus=root_port_1.1 \
-device pcie-root-port,id=root_port_1.2,chassis=1,slot=2  \
  -device qemu-xhci,id=usb,bus=root_port_1.2 \
-device pcie-root-port,id=root_port_1.3,chassis=1,slot=3  \
  -device bochs-display,bus=root_port_1.3 \
-device pcie-root-port,id=root_port_1.4,chassis=1,slot=4  \
  -device e1000e,bus=root_port_1.4 \
-device pcie-root-port,id=root_port_1.5,chassis=1,slot=5  \
  -device pcie-pci-bridge,id=pci,bus=root_port_1.5 \
    -device virtio-rng-pci,bus=pci,addr=8 \
\
-device pcie-root-port,id=root_port_1.12,chassis=1,slot=12  \
  -device x3130-upstream,id=upstream_port1,bus=root_port_1.12 \
    -device xio3130-downstream,id=downstream_port1,bus=upstream_port1,chassis=1,slot=20 \
      -device ac97,bus=downstream_port1 \
\
-device pxb-pcie,id=pcie1,bus_nr=2 \
-device pcie-root-port,id=root_port_2.1,bus=pcie1,chassis=2,slot=1 \
  -device ahci,bus=root_port_2.1 \

\
-net bridge,br=virbr0,id=bridge \
-device e1000e \
